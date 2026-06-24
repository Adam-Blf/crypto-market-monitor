# Architecture

## Overview

The system is split into four independent services communicating via Apache Kafka and HTTP/WebSocket.

```
Binance WebSocket (BTC/USDT, ETH/USDT)
Coinbase WebSocket (BTC-USD)
         |
         v
   [Ingester Service]          Node.js + TypeScript
         |  produce
         v
   [Apache Kafka]              crypto-trades topic
         |  consume
         v
   [Processor Service]         VWAP, SMA20, z-score anomaly
         |  produce
         v
   [Apache Kafka]              crypto-metrics topic
         |  consume
         v
   [API Server]                Express + Socket.IO
         |  REST + WebSocket
         v
   [Dashboard]                 HTML/CSS/JS + Chart.js
```

## Design decisions

### Why Kafka between ingestion and processing

The Binance stream emits multiple events per second. Without a buffer, slow processing or consumer crashes would cause data loss. Kafka decouples the two layers - ingestion keeps writing at market speed, processing reads at its own pace.

This also allows multiple consumers on the same stream (e.g., a future alert service could consume `crypto-trades` independently without any change to the ingester).

### Why the API layer must not read Kafka directly

The dashboard must never be a Kafka consumer. Kafka clients are stateful, require offset management, and are not designed for browser-facing workloads. The API layer aggregates data (ring buffers per symbol), handles reconnections, and delivers formatted updates over Socket.IO. This separation guarantees that adding more dashboard clients does not add Kafka consumer pressure.

### KRaft mode (no Zookeeper)

Kafka 3.7+ supports KRaft (Kafka Raft) for internal metadata management. This removes the Zookeeper dependency, simplifying deployment to a single container with a single volume.

### Analytics

| Metric | Method | Window |
|--------|--------|--------|
| VWAP | sum(price * qty) / sum(qty) | 1 minute |
| SMA-20 | mean of last 20 prices | last 20 trades |
| Anomaly | z-score > 2.5 on quantity | 1 minute |
| Price change 1m | (current - first in window) / first | 1 minute |
| Price change 5m | (current - first in window) / first | 5 minutes |

Z-score: `(value - mean) / std`. A trade quantity with z-score above 2.5 is flagged as anomalous (large whale trade).

## Data flow

### Ingester

```
WebSocket message (Binance/Coinbase)
  -> parse JSON
  -> normalize to Trade { exchange, symbol, price, quantity, timestamp, tradeId, side, value }
  -> Kafka produce to crypto-trades, key = symbol
```

### Processor

```
Kafka consume from crypto-trades
  -> add to in-memory store (circular buffer, max 1000/symbol, 10min TTL)
  -> compute Metrics snapshot
  -> Kafka produce to crypto-metrics, key = symbol
```

### API

```
Kafka consume from crypto-metrics
  -> update latestMetrics[symbol]
  -> append to history ring buffer (max 200/symbol)
  -> if anomaly: push to anomalies ring buffer (max 50)
  -> Socket.IO emit metrics:update to subscribed clients
  -> Socket.IO emit anomaly:detected if flagged
```

### Dashboard

```
Socket.IO connect -> receive initial:state (all latestMetrics)
Socket.IO on metrics:update -> update DOM, update chart
Socket.IO on anomaly:detected -> prepend to anomaly feed + AudioContext beep
Tab click -> emit subscribe:symbol -> API sends targeted updates
REST GET /api/history/:symbol -> load 100 points for chart on tab switch
```

## File structure

```
crypto-market-monitor/
- ingester/
  - src/
    - types.ts       Trade interface, exchange event types
    - producer.ts    kafkajs producer, symbol partitioning, exp backoff
    - binance.ts     BTC/USDT + ETH/USDT stream, auto-reconnect
    - coinbase.ts    market_trades channel, BTC-USD + ETH-USD
    - index.ts       entry point, graceful shutdown
  - package.json
  - tsconfig.json
  - Dockerfile

- processor/
  - src/
    - types.ts       Trade + Metrics interfaces
    - store.ts       circular buffer, 10min eviction
    - analytics.ts   pure functions: VWAP, SMA, z-score, price change, high/low
    - consumer.ts    kafkajs consumer, wires store + analytics + producer
    - index.ts       entry point, graceful shutdown
  - package.json
  - tsconfig.json
  - Dockerfile

- api/
  - src/
    - types.ts       Metrics interface
    - store.ts       latestMetrics, history ring buffers, anomaly list
    - routes.ts      GET /api/health, /api/metrics, /api/metrics/:symbol, /api/history/:symbol, /api/anomalies
    - wsServer.ts    Socket.IO setup, rooms, initial state push
    - kafka.ts       kafkajs consumer for crypto-metrics
    - index.ts       Express + HTTP + Socket.IO, graceful shutdown
  - package.json
  - tsconfig.json
  - Dockerfile

- dashboard/
  - index.html       layout, CDN imports
  - css/main.css     dark theme, flash animations, chart containers
  - js/main.js       Socket.IO client, Chart.js, state management
  - nginx.conf
  - Dockerfile

- docker-compose.yml  full stack with Kafka, Kafka UI, all 4 services
- package.json        npm workspaces (ingester, processor, api)
- .env.example
```
