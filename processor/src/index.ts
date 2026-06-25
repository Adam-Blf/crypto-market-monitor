import 'dotenv/config';
import { startConsumer, stopConsumer } from './consumer';

async function main(): Promise<void> {
  console.log('[processor] Starting...');

  try {
    await startConsumer();
    console.log('[processor] Consumer running, processing crypto-trades...');
  } catch (err) {
    console.error('[processor] Failed to start:', err);
    process.exit(1);
  }
}

async function shutdown(): Promise<void> {
  console.log('[processor] Shutting down gracefully...');
  try {
    await stopConsumer();
    console.log('[processor] Consumer disconnected.');
  } catch (err) {
    console.error('[processor] Error during shutdown:', err);
  }
  process.exit(0);
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

main();
