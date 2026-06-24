import 'dotenv/config';
import http from 'http';
import express from 'express';
import cors from 'cors';
import routes from './routes';
import { createWsServer } from './wsServer';
import { startKafkaConsumer, stopKafkaConsumer } from './kafka';

const PORT = parseInt(process.env['API_PORT'] ?? '3001', 10);

const app = express();
app.use(cors());
app.use(express.json());
app.use('/api', routes);

const server = http.createServer(app);
createWsServer(server);

async function start(): Promise<void> {
  await startKafkaConsumer();
  server.listen(PORT, () => {
    console.log(`[api] Server running on http://localhost:${PORT}`);
    console.log(`[api] REST: http://localhost:${PORT}/api/metrics`);
    console.log(`[api] WS:   ws://localhost:${PORT}`);
  });
}

async function shutdown(): Promise<void> {
  console.log('[api] Shutting down...');
  await stopKafkaConsumer();
  server.close(() => process.exit(0));
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

start().catch((err) => {
  console.error('[api] Fatal startup error:', err);
  process.exit(1);
});
