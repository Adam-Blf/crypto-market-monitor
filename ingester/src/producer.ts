import { Kafka, Producer, Partitioners } from 'kafkajs';
import { Trade } from './types';

const BROKERS = (process.env.KAFKA_BROKERS ?? 'localhost:9092').split(',');
const TOPIC = process.env.KAFKA_TOPIC_TRADES ?? 'crypto-trades';

const kafka = new Kafka({
  clientId: 'crypto-ingester',
  brokers: BROKERS,
  retry: {
    initialRetryTime: 300,
    retries: 10,
    factor: 2,
    maxRetryTime: 30_000,
  },
});

let producer: Producer | null = null;
let connected = false;

const SYMBOL_PARTITIONS: Record<string, number> = {
  'BTC-USDT': 0,
  'ETH-USDT': 1,
  'BTC-USD': 2,
  'ETH-USD': 3,
};

export async function connectProducer(): Promise<void> {
  producer = kafka.producer({
    createPartitioner: Partitioners.DefaultPartitioner,
    allowAutoTopicCreation: true,
  });

  await producer.connect();
  connected = true;
  console.log('[producer] connected to Kafka brokers:', BROKERS.join(', '));
}

export async function sendTrade(trade: Trade): Promise<void> {
  if (!producer || !connected) {
    throw new Error('Producer not connected');
  }

  const partition = SYMBOL_PARTITIONS[trade.symbol] ?? 0;

  await producer.send({
    topic: TOPIC,
    messages: [
      {
        key: trade.symbol,
        value: JSON.stringify(trade),
        partition,
        timestamp: trade.timestamp.toString(),
      },
    ],
  });
}

export async function disconnectProducer(): Promise<void> {
  if (producer && connected) {
    await producer.disconnect();
    connected = false;
    console.log('[producer] disconnected');
  }
}
