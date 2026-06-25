import { Server as HTTPServer } from 'http';
import { Server as SocketIOServer, Socket } from 'socket.io';
import { getLatest } from './store';
import { Metrics } from './types';

let io: SocketIOServer | null = null;

// Compteur de messages pour le calcul du debit (msg/s affiché dans le footer du dashboard)
let messageCount = 0;
let lastMsgCountReset = Date.now();

export function createWsServer(httpServer: HTTPServer): SocketIOServer {
  io = new SocketIOServer(httpServer, {
    // CORS large en dev - a restreindre en prod avec la vraie origine
    cors: { origin: '*', methods: ['GET', 'POST'] },
    transports: ['websocket', 'polling'],
  });

  io.on('connection', (socket: Socket) => {
    // Envoyer l'etat courant immediatement a la connexion pour eviter l'ecran vide
    const initialData = getLatest();
    socket.emit('initial:state', { data: initialData, timestamp: Date.now() });

    // Rooms par symbole: chaque client s'abonne aux paires qui l'interessent
    // On evite d'envoyer toutes les metriques a tout le monde
    socket.on('subscribe:symbol', (symbol: string) => {
      socket.join(`symbol:${symbol.toUpperCase()}`);
    });

    socket.on('unsubscribe:symbol', (symbol: string) => {
      socket.leave(`symbol:${symbol.toUpperCase()}`);
    });

    socket.on('disconnect', () => {
      // Socket.IO gere le cleanup des rooms automatiquement a la deconnexion
    });
  });

  // Stats serveur emises toutes les 10s vers tous les clients connectes
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

  // Broadcast global pour le VolumeChart (compare toutes les paires)
  io.emit('metrics:update', metrics);

  // Broadcast specifique a la room du symbole pour le PriceChart
  io.to(`symbol:${metrics.symbol}`).emit('metrics:symbol', metrics);

  if (metrics.anomaly) {
    io.emit('anomaly:detected', metrics);
  }
}
