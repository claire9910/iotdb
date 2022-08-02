/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * <p>http://www.apache.org/licenses/LICENSE-2.0
 *
 * <p>Unless required by applicable law or agreed to in writing, software distributed under the
 * License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.iotdb.db.service.thrift.handler;

import org.apache.iotdb.db.service.metrics.MetricsService;
import org.apache.iotdb.db.service.metrics.enums.Metric;
import org.apache.iotdb.db.service.metrics.enums.Tag;
import org.apache.iotdb.db.service.thrift.impl.TSServiceImpl;
import org.apache.iotdb.metrics.utils.MetricLevel;

import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.server.ServerContext;
import org.apache.thrift.server.TServerEventHandler;
import org.apache.thrift.transport.TTransport;

public class RPCServiceThriftHandler implements TServerEventHandler {
  private TSServiceImpl serviceImpl;

  public RPCServiceThriftHandler(TSServiceImpl serviceImpl) {
    this.serviceImpl = serviceImpl;
  }

  @Override
  public ServerContext createContext(TProtocol arg0, TProtocol arg1) {
    MetricsService.getInstance()
        .getMetricManager()
        .getOrCreateGauge(
            Metric.THRIFT_CONNECTIONS.toString(), MetricLevel.CORE, Tag.NAME.toString(), "RPC")
        .incr(1L);
    return null;
  }

  @Override
  public void deleteContext(ServerContext arg0, TProtocol arg1, TProtocol arg2) {
    // release query resources.
    serviceImpl.handleClientExit();
    MetricsService.getInstance()
        .getMetricManager()
        .getOrCreateGauge(
            Metric.THRIFT_CONNECTIONS.toString(), MetricLevel.CORE, Tag.NAME.toString(), "RPC")
        .decr(1L);
  }

  @Override
  public void preServe() {
    // nothing
  }

  @Override
  public void processContext(ServerContext arg0, TTransport arg1, TTransport arg2) {
    // nothing
  }
}
