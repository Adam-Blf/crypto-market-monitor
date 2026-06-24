import 'dotenv/config';
import http from 'http';
import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import morgan from 'morgan';
import routes from './routes';
import { createWsServer } from './wsServer';
import { startKafkaConsumer, stopKafkaConsumer } from './kafka';
import { config } from './config';

const app = express();

// Middlewares de sécurité et de logging (main)
app.use(helmet({
  crossOriginEmbedderPolicy: false,
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      connectSrc: ["'self'", 'ws:', 'wss:'],
    },
  },
}));

app.use(cors({
  origin: config.CORS_ORIGIN,
  methods: ['GET'], // Ajustez si feat/api requiert POST/PUT/DELETE
  credentials: false,
}));

app.use(rateLimit({
  windowMs: config.RATE_LIMIT_WINDOW_MS,
  max: config.RATE_LIMIT_MAX,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' },
}));

app.use(morgan(config.NODE_ENV === 'production' ? 'tiny' : 'combined'));

app.use(express.json({ limit: '10kb' }));

// Routes de l'API
app.use('/api', routes);

// Gestion des erreurs et 404 (main)
app.use((_req: Request, res: Response) => {
  res.status(404).json({ error: 'Not found' });
});

app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error(err.stack);
  const status = (err as { status?: number }).status ?? 500;
  res.status(status).json({
    error: config.NODE_ENV === 'production' ? 'Internal server error' : err.message,
  });
});

// Initialisation des serveurs HTTP et WebSocket
const server = http.createServer(app);
createWsServer(server);

async function start(): Promise<void> {
  await startKafkaConsumer();
  server.listen(config.API_PORT, () => {
    console.log(`[api] Server running on http://localhost:${config.API_PORT}`);
    console.log(`[api] REST: http://localhost:${config.API_PORT}/api/metrics`);
    console.log(`[api] WS:   ws://localhost:${config.API_PORT}`);
    console.log(`[api] CORS origin: ${config.CORS_ORIGIN}`);
    console.log(`[api] Rate limit: ${config.RATE_LIMIT_MAX} req / ${config.RATE_LIMIT_WINDOW_MS}ms`);
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