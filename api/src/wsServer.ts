import { Server as HTTPServer } from 'http';
import { Server as SocketIOServer, Socket } from 'socket.io';
import { getLatest } from './store';
import { Metrics } from './types';

let io: SocketIOServer | null = null;
let messageCount = 0;
let lastMsgCountReset = Date.now();

export function createWsServer(httpServer: HTTPServer): SocketIOServer {
  io = new SocketIOServer(httpServer, {
    cors: { origin: '*', methods: ['GET', 'POST'] },
    transports: ['websocket', 'polling'],
  });

  io.on('connection', (socket: Socket) => {
    const initialData = getLatest();
    socket.emit('initial:state', { data: initialData, timestamp: Date.now() });

    socket.on('subscribe:symbol', (symbol: string) => {
      socket.join(`symbol:${symbol.toUpperCase()}`);
    });

    socket.on('unsubscribe:symbol', (symbol: string) => {
      socket.leave(`symbol:${symbol.toUpperCase()}`);
    });

    socket.on('disconnect', () => {
      // cleanup handled by socket.io automatically
    });
  });

  setInterval(() => {
    if (!io) return;
    const now = Date.now();
    const elapsed = (now - lastMsgCountReset) / 1000;
    const mps = elapsed > 0 ? messageCount / elapsed : 0;
    io.emit('server:stats', {
      connections: io.engine.clientsCount,
      messagesPerSecond: Math.round(mps * 100) / 100,
      uptime: process.uptime(),
      timestamp: now,
    });
    messageCount = 0;
    lastMsgCountReset = now;
  }, 10_000);

  return io;
}

export function broadcastMetrics(metrics: Metrics): void {
  if (!io) return;
  messageCount++;
  io.emit('metrics:update', metrics);
  io.to(`symbol:${metrics.symbol}`).emit('metrics:symbol', metrics);

  if (metrics.anomaly) {
    io.emit('anomaly:detected', metrics);
  }
}
