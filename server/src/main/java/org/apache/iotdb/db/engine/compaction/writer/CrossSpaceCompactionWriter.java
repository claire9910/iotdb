/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.iotdb.db.engine.compaction.writer;

import org.apache.iotdb.db.conf.IoTDBDescriptor;
import org.apache.iotdb.db.engine.storagegroup.TsFileResource;
import org.apache.iotdb.db.query.control.FileReaderManager;
import org.apache.iotdb.db.rescon.SystemInfo;
import org.apache.iotdb.tsfile.file.metadata.TimeseriesMetadata;
import org.apache.iotdb.tsfile.read.common.block.column.Column;
import org.apache.iotdb.tsfile.read.common.block.column.TimeColumn;
import org.apache.iotdb.tsfile.write.chunk.AlignedChunkWriterImpl;
import org.apache.iotdb.tsfile.write.writer.TsFileIOWriter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

public class CrossSpaceCompactionWriter extends AbstractCompactionWriter {
  // target fileIOWriters
  private List<TsFileIOWriter> fileWriterList = new ArrayList<>();

  // source tsfiles
  private List<TsFileResource> seqTsFileResources;
  private List<TsFileResource> targetTsFileResources;

  // Each sub task has its corresponding seq file index.
  // The index of the array corresponds to subTaskId.
  private int[] seqFileIndexArray = new int[subTaskNum];

  // device end time in each source seq file
  private final long[] currentDeviceEndTime;

  // whether each target file is empty or not
  private final boolean[] isEmptyFile;

  // whether each target file has device data or not
  private final boolean[] isDeviceExistedInTargetFiles;

  // current chunk group header size
  private int chunkGroupHeaderSize;

  private AtomicLong[] startTimeForCurDeviceForEachFile;
  private AtomicLong[] endTimeForCurDeviceForEachFile;
  private AtomicBoolean[] hasCurDeviceForEachFile;
  private AtomicLong[][] startTimeForEachDevice = new AtomicLong[subTaskNum][];
  private AtomicLong[][] endTimeForEachDevice = new AtomicLong[subTaskNum][];

  public CrossSpaceCompactionWriter(
      List<TsFileResource> targetResources, List<TsFileResource> seqFileResources)
      throws IOException {
    this.targetTsFileResources = targetResources;
    currentDeviceEndTime = new long[seqFileResources.size()];
    isEmptyFile = new boolean[seqFileResources.size()];
    isDeviceExistedInTargetFiles = new boolean[targetResources.size()];
    startTimeForCurDeviceForEachFile = new AtomicLong[targetResources.size()];
    endTimeForCurDeviceForEachFile = new AtomicLong[targetResources.size()];
    hasCurDeviceForEachFile = new AtomicBoolean[targetResources.size()];
    long memorySizeForEachWriter =
        (long)
            (SystemInfo.getInstance().getMemorySizeForCompaction()
                / IoTDBDescriptor.getInstance().getConfig().getConcurrentCompactionThread()
                * IoTDBDescriptor.getInstance()
                    .getConfig()
                    .getChunkMetadataSizeProportionInCompaction()
                / targetResources.size());
    for (int i = 0; i < targetResources.size(); i++) {
      this.fileWriterList.add(
          new TsFileIOWriter(targetResources.get(i).getTsFile(), true, memorySizeForEachWriter));
      isEmptyFile[i] = true;
      startTimeForCurDeviceForEachFile[i] = new AtomicLong(Long.MAX_VALUE);
      endTimeForCurDeviceForEachFile[i] = new AtomicLong(Long.MIN_VALUE);
      hasCurDeviceForEachFile[i] = new AtomicBoolean(false);
    }
    this.seqTsFileResources = seqFileResources;
    for (int i = 0, size = targetResources.size(); i < subTaskNum; ++i) {
      startTimeForEachDevice[i] = new AtomicLong[size];
      endTimeForEachDevice[i] = new AtomicLong[size];
      for (int j = 0; j < size; ++j) {
        startTimeForEachDevice[i][j] = new AtomicLong(Long.MAX_VALUE);
        endTimeForEachDevice[i][j] = new AtomicLong(Long.MIN_VALUE);
      }
    }
  }

  @Override
  public void startChunkGroup(String deviceId, boolean isAlign) throws IOException {
    this.deviceId = deviceId;
    this.isAlign = isAlign;
    this.seqFileIndexArray = new int[subTaskNum];
    checkIsDeviceExistAndGetDeviceEndTime();
    for (int i = 0; i < fileWriterList.size(); i++) {
      chunkGroupHeaderSize = fileWriterList.get(i).startChunkGroup(deviceId);
    }
  }

  @Override
  public void endChunkGroup() throws IOException {
    for (int i = 0; i < seqTsFileResources.size(); i++) {
      TsFileIOWriter targetFileWriter = fileWriterList.get(i);
      if (isDeviceExistedInTargetFiles[i]) {
        targetFileWriter.endChunkGroup();
      } else {
        targetFileWriter.truncate(targetFileWriter.getPos() - chunkGroupHeaderSize);
      }
      isDeviceExistedInTargetFiles[i] = false;
    }
    for (int i = 0, size = targetTsFileResources.size(); i < size; ++i) {
      for (int j = 0; j < subTaskNum; ++j) {
        targetTsFileResources
            .get(i)
            .updateStartTime(deviceId, startTimeForEachDevice[j][i].getAndSet(Long.MAX_VALUE));
        targetTsFileResources
            .get(i)
            .updateEndTime(deviceId, endTimeForEachDevice[j][i].getAndSet(Long.MIN_VALUE));
      }
    }
    deviceId = null;
  }

  @Override
  public void endMeasurement(int subTaskId) throws IOException {
    flushChunkToFileWriter(fileWriterList.get(seqFileIndexArray[subTaskId]), subTaskId);
    seqFileIndexArray[subTaskId] = 0;
  }

  @Override
  public void write(long timestamp, Object value, int subTaskId) throws IOException {
    checkTimeAndMayFlushChunkToCurrentFile(timestamp, subTaskId);
    writeDataPoint(timestamp, value, subTaskId);
    int fileIndex = seqFileIndexArray[subTaskId];
    startTimeForEachDevice[subTaskId][fileIndex].accumulateAndGet(timestamp, Math::min);
    endTimeForEachDevice[subTaskId][fileIndex].accumulateAndGet(timestamp, Math::max);
    if (measurementPointCountArray[subTaskId] % 10 == 0) {
      checkChunkSizeAndMayOpenANewChunk(
          fileWriterList.get(seqFileIndexArray[subTaskId]), subTaskId);
    }
    isDeviceExistedInTargetFiles[seqFileIndexArray[subTaskId]] = true;
    isEmptyFile[seqFileIndexArray[subTaskId]] = false;
  }

  @Override
  public void write(
      TimeColumn timestamps, Column[] columns, String device, int subTaskId, int batchSize)
      throws IOException {
    // todo control time range of target tsfile
    checkTimeAndMayFlushChunkToCurrentFile(timestamps.getStartTime(), subTaskId);
    AlignedChunkWriterImpl chunkWriter = (AlignedChunkWriterImpl) this.chunkWriters[subTaskId];
    chunkWriter.write(timestamps, columns, batchSize);
    int fileIndex = seqFileIndexArray[subTaskId];
    startTimeForEachDevice[subTaskId][fileIndex].accumulateAndGet(
        timestamps.getStartTime(), Math::min);
    endTimeForEachDevice[subTaskId][fileIndex].accumulateAndGet(timestamps.getEndTime(), Math::max);
    checkChunkSizeAndMayOpenANewChunk(fileWriterList.get(seqFileIndexArray[subTaskId]), subTaskId);
    isDeviceExistedInTargetFiles[seqFileIndexArray[subTaskId]] = true;
    isEmptyFile[seqFileIndexArray[subTaskId]] = false;
  }

  @Override
  public void endFile() throws IOException {
    for (int i = 0; i < isEmptyFile.length; i++) {
      fileWriterList.get(i).endFile();
      // delete empty target file
      if (isEmptyFile[i]) {
        fileWriterList.get(i).getFile().delete();
      }
    }
  }

  @Override
  public void close() throws IOException {
    for (TsFileIOWriter targetWriter : fileWriterList) {
      if (targetWriter != null && targetWriter.canWrite()) {
        targetWriter.close();
      }
    }
    fileWriterList = null;
    seqTsFileResources = null;
  }

  @Override
  public List<TsFileIOWriter> getFileIOWriter() {
    return fileWriterList;
  }

  private void checkTimeAndMayFlushChunkToCurrentFile(long timestamp, int subTaskId)
      throws IOException {
    int fileIndex = seqFileIndexArray[subTaskId];
    // if timestamp is later than the current source seq tsfile, than flush chunk writer
    while (timestamp > currentDeviceEndTime[fileIndex]) {
      if (fileIndex != seqTsFileResources.size() - 1) {
        flushChunkToFileWriter(fileWriterList.get(fileIndex), subTaskId);
        seqFileIndexArray[subTaskId] = ++fileIndex;
      } else {
        // If the seq file is deleted for various reasons, the following two situations may occur
        // when selecting the source files: (1) unseq files may have some devices or measurements
        // which are not exist in seq files. (2) timestamp of one timeseries in unseq files may
        // later than any seq files. Then write these data into the last target file.
        return;
      }
    }
  }

  private void checkIsDeviceExistAndGetDeviceEndTime() throws IOException {
    int fileIndex = 0;
    while (fileIndex < seqTsFileResources.size()) {
      if (seqTsFileResources.get(fileIndex).getTimeIndexType() == 1) {
        // the timeIndexType of resource is deviceTimeIndex
        currentDeviceEndTime[fileIndex] = seqTsFileResources.get(fileIndex).getEndTime(deviceId);
      } else {
        long endTime = Long.MIN_VALUE;
        Map<String, TimeseriesMetadata> deviceMetadataMap =
            FileReaderManager.getInstance()
                .get(seqTsFileResources.get(fileIndex).getTsFilePath(), true)
                .readDeviceMetadata(deviceId);
        for (Map.Entry<String, TimeseriesMetadata> entry : deviceMetadataMap.entrySet()) {
          long tmpStartTime = entry.getValue().getStatistics().getStartTime();
          long tmpEndTime = entry.getValue().getStatistics().getEndTime();
          if (tmpEndTime >= tmpStartTime && endTime < tmpEndTime) {
            endTime = tmpEndTime;
          }
        }
        currentDeviceEndTime[fileIndex] = endTime;
      }

      fileIndex++;
    }
  }

  @Override
  public void updateStartTimeAndEndTime(String device, long time, int subTaskId) {
    int fileIndex = seqFileIndexArray[subTaskId];
    // using synchronized will lead to significant performance loss,
    // so we use atomic long here to accelerate
    startTimeForCurDeviceForEachFile[fileIndex].accumulateAndGet(time, Math::min);
    endTimeForCurDeviceForEachFile[fileIndex].accumulateAndGet(time, Math::max);
    hasCurDeviceForEachFile[fileIndex].set(true);
  }
}
