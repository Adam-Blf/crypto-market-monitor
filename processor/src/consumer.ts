import { Kafka, Producer } from 'kafkajs';
import { Trade, Metrics } from './types';
import { addTrade, getTradesInWindow, getLastN } from './store';
import {
  computeVWAP,
  computeSMA,
  computeZScore,
  computePriceChange,
  computeHighLow,
  computeVolume,
} from './analytics';

const BROKERS = (process.env.KAFKA_BROKERS || 'localhost:9092').split(',');
const TOPIC_TRADES = process.env.KAFKA_TOPIC_TRADES || 'crypto-trades';
const TOPIC_METRICS = process.env.KAFKA_TOPIC_METRICS || 'crypto-metrics';
const GROUP_ID = process.env.KAFKA_GROUP_ID_PROCESSOR || 'processor-group';

const ANOMALY_THRESHOLD = 2.5;
const WINDOW_1M = 60_000;
const WINDOW_5M = 5 * 60_000;

const kafka = new Kafka({
  clientId: 'processor',
  brokers: BROKERS,
  retry: { retries: 10, initialRetryTime: 500 },
});

const consumer = kafka.consumer({ groupId: GROUP_ID });
const producer: Producer = kafka.producer();

function buildMetrics(trade: Trade): Metrics {
  const trades1m = getTradesInWindow(trade.symbol, WINDOW_1M);
  const trades5m = getTradesInWindow(trade.symbol, WINDOW_5M);
  const last20 = getLastN(trade.symbol, 20);

  const quantities1m = trades1m.map((t) => t.quantity);
  const zScore = computeZScore(quantities1m, trade.quantity);
  const { high, low } = computeHighLow(trades1m);

  return {
    symbol: trade.symbol,
    timestamp: Date.now(),
    vwap: computeVWAP(trades1m),
    sma20: computeSMA(last20.map((t) => t.price)),
    currentPrice: trade.price,
    priceChange1m: computePriceChange(trade.price, trades1m, WINDOW_1M),
    priceChange5m: computePriceChange(trade.price, trades5m, WINDOW_5M),
    volumeTotal1m: computeVolume(trades1m),
    tradeCount1m: trades1m.length,
    anomaly: Math.abs(zScore) > ANOMALY_THRESHOLD,
    anomalyScore: zScore,
    highPrice1m: high,
    lowPrice1m: low,
  };
}

export async function startConsumer(): Promise<void> {
  await producer.connect();
  await consumer.connect();
  await consumer.subscribe({ topic: TOPIC_TRADES, fromBeginning: false });

  await consumer.run({
    eachMessage: async ({ message }) => {
      if (!message.value) return;

      let trade: Trade;
      try {
        trade = JSON.parse(message.value.toString()) as Trade;
      } catch {
        process.stderr.write(`[DLQ] Failed to parse message: ${message.value.toString()}\n`);
        return;
      }

      addTrade(trade);
      const metrics = buildMetrics(trade);

      try {
        await producer.send({
          topic: TOPIC_METRICS,
          messages: [
            {
              key: trade.symbol,
              value: JSON.stringify(metrics),
            },
          ],
        });
      } catch (err) {
        process.stderr.write(`[DLQ] Failed to produce metrics for ${trade.symbol}: ${err}\n`);
      }
    },
  });
}

export async function stopConsumer(): Promise<void> {
  await consumer.disconnect();
  await producer.disconnect();
}
