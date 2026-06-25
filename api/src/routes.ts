import { Router, Request, Response } from 'express';
import { getLatest, getHistory, getAnomalies } from './store';

const router = Router();

router.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', uptime: process.uptime(), timestamp: Date.now() });
});

router.get('/metrics', (_req: Request, res: Response) => {
  res.json({ data: getLatest(), timestamp: Date.now() });
});

router.get('/metrics/:symbol', (req: Request, res: Response) => {
  const data = getLatest(req.params.symbol);
  if (!data) {
    res.status(404).json({ error: 'Symbol not found', symbol: req.params.symbol });
    return;
  }
  res.json({ data, timestamp: Date.now() });
});

router.get('/history/:symbol', (req: Request, res: Response) => {
  const limit = Math.min(parseInt(req.query['limit'] as string ?? '100', 10), 200);
  const data = getHistory(req.params.symbol, limit);
  res.json({ data, symbol: req.params.symbol.toUpperCase(), count: data.length, timestamp: Date.now() });
});

router.get('/anomalies', (req: Request, res: Response) => {
  const limit = Math.min(parseInt(req.query['limit'] as string ?? '20', 10), 50);
  const data = getAnomalies(limit);
  res.json({ data, count: data.length, timestamp: Date.now() });
});

export default router;
