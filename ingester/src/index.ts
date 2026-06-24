import 'dotenv/config';
import { connectProducer, disconnectProducer } from './producer';
import { startBinanceClient } from './binance';
import { startCoinbaseClient } from './coinbase';

let shutdownInProgress = false;

async function main(): Promise<void> {
  console.log('[ingester] starting crypto market data ingester...');

  await connectProducer();

  startBinanceClient();
  startCoinbaseClient();

  console.log('[ingester] all clients started, consuming live market data');
}

async function shutdown(): Promise<void> {
  if (shutdownInProgress) return;
  shutdownInProgress = true;

  console.log('[ingester] graceful shutdown initiated...');
  try {
    await disconnectProducer();
    console.log('[ingester] shutdown complete');
  } catch (err) {
    console.error('[ingester] shutdown error:', err);
  }
  process.exit(0);
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

main().catch((err) => {
  console.error('[ingester] fatal startup error:', err);
  process.exit(1);
});
