import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';
import { updateMetrics } from './store';
import { broadcastMetrics } from './wsServer';
import { Metrics } from './types';

const brokers = (process.env['KAFKA_BROKERS'] ?? 'localhost:9092').split(',');
const topic = process.env['KAFKA_TOPIC_METRICS'] ?? 'crypto-metrics';
const groupId = process.env['KAFKA_GROUP_ID_API'] ?? 'api-group';

const kafka = new Kafka({
  clientId: 'crypto-api',
  brokers,
  retry: { retries: 10, initialRetryTime: 300, factor: 1.5 },
});

let consumer: Consumer | null = null;

export async function startKafkaConsumer(): Promise<void> {
  consumer = kafka.consumer({ groupId, sessionTimeout: 30_000 });

  await consumer.connect();
  await consumer.subscribe({ topic, fromBeginning: false });

  await consumer.run({
    eachMessage: async ({ message }: EachMessagePayload) => {
      if (!message.value) return;
      try {
        const metrics: Metrics = JSON.parse(message.value.toString());
        updateMetrics(metrics);
        broadcastMetrics(metrics);
      } catch (err) {
        console.error('[kafka] Failed to parse metrics message:', err);
      }
    },
  });

  console.log(`[kafka] Consumer connected, subscribed to ${topic}`);
}

export async function stopKafkaConsumer(): Promise<void> {
  if (consumer) {
    await consumer.disconnect();
    consumer = null;
  }
}
