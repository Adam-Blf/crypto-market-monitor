import { z } from 'zod';

const envSchema = z.object({
  KAFKA_BROKERS: z.string().default('localhost:9092'),
  KAFKA_TOPIC_METRICS: z.string().default('crypto-metrics'),
  KAFKA_GROUP_ID_API: z.string().default('api-group'),
  API_PORT: z.coerce.number().int().min(1).max(65535).default(3001),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  CORS_ORIGIN: z.string().default('http://localhost:8080'),
  RATE_LIMIT_WINDOW_MS: z.coerce.number().default(15 * 60 * 1000),
  RATE_LIMIT_MAX: z.coerce.number().default(200),
});

const result = envSchema.safeParse(process.env);

if (!result.success) {
  console.error('Invalid environment configuration:', result.error.format());
  process.exit(1);
}

export const config = result.data;
