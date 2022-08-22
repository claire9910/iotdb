/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.iotdb.db.doublelive;

import org.apache.iotdb.rpc.IoTDBConnectionException;
import org.apache.iotdb.session.pool.SessionPool;
import org.apache.iotdb.tsfile.utils.Pair;

import org.slf4j.Logger;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.concurrent.BlockingQueue;

import static org.apache.iotdb.db.service.basic.ServiceProvider.DOUBLE_LIVE_LOGGER;

public class OperationSyncConsumer implements Runnable {
  private static final Logger LOGGER = DOUBLE_LIVE_LOGGER;

  private final BlockingQueue<Pair<ByteBuffer, OperationSyncPlanTypeUtils.OperationSyncPlanType>>
      OperationSyncQueue;
  private final SessionPool operationSyncSessionPool;
  private final OperationSyncLogService dmlLogService;

  public OperationSyncConsumer(
      BlockingQueue<Pair<ByteBuffer, OperationSyncPlanTypeUtils.OperationSyncPlanType>>
          OperationSyncQueue,
      SessionPool operationSyncSessionPool,
      OperationSyncLogService dmlLogService) {
    this.OperationSyncQueue = OperationSyncQueue;
    this.operationSyncSessionPool = operationSyncSessionPool;
    this.dmlLogService = dmlLogService;
  }

  @Override
  public void run() {
    while (true) {
      Pair<ByteBuffer, OperationSyncPlanTypeUtils.OperationSyncPlanType> head;
      ByteBuffer headBuffer;
      OperationSyncPlanTypeUtils.OperationSyncPlanType headType;
      try {
        head = OperationSyncQueue.take();
        headBuffer = head.left;
        headType = head.right;
      } catch (InterruptedException e) {
        LOGGER.error("OperationSyncConsumer been interrupted: ", e);
        continue;
      }

      headBuffer.position(0);
      boolean transmitStatus = false;
      try {
        headBuffer.position(0);
        transmitStatus = operationSyncSessionPool.operationSyncTransmit(headBuffer);
      } catch (IoTDBConnectionException connectionException) {
        // warn IoTDBConnectionException and do serialization
        LOGGER.warn(
            "OperationSyncConsumer can't transmit because network failure", connectionException);
      } catch (Exception e) {
        // The PhysicalPlan has internal error, reject transmit
        LOGGER.error("OperationSyncConsumer can't transmit", e);
        continue;
      }

      if (!transmitStatus) {
        try {
          // must set buffer position to limit() before serialization
          headBuffer.position(headBuffer.limit());
          dmlLogService.acquireLogWriter();
          dmlLogService.write(headBuffer);
        } catch (IOException e) {
          LOGGER.error("OperationSyncConsumer can't serialize physicalPlan", e);
        } finally {
          dmlLogService.releaseLogWriter();
        }
      }
    }
  }
}
