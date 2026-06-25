import { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, PointElement, LineElement,
  Tooltip, Legend, Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import type { Metrics } from '../types';
import { useI18n } from '../i18n';
import { formatPrice, formatTime } from '../utils';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler);

interface Props {
  history: Metrics[];
  symbol: string;
}

export function PriceChart({ history, symbol }: Props) {
  const { t, lang } = useI18n();

  const { labels, prices, sma20s } = useMemo(() => {
    const labels = history.map(m => formatTime(m.timestamp, lang));
    const prices = history.map(m => m.currentPrice);
    const sma20s = history.map(m => m.sma20 ?? null);
    return { labels, prices, sma20s };
  }, [history, lang]);

  const data = {
    labels,
    datasets: [
      {
        label: t('chart.price'),
        data: prices,
        borderColor: '#F59E0B',
        backgroundColor: 'rgba(245,158,11,0.06)',
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.3,
        fill: true,
        order: 1,
      },
      {
        label: t('chart.sma20'),
        data: sma20s,
        borderColor: '#8B5CF6',
        backgroundColor: 'transparent',
        borderWidth: 1.5,
        borderDash: [4, 4],
        pointRadius: 0,
        tension: 0.3,
        fill: false,
        order: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index' as const, intersect: false },
    plugins: {
      legend: {
        labels: { color: 'rgba(240,244,255,0.5)', font: { size: 11 }, boxWidth: 16 },
      },
      tooltip: {
        backgroundColor: '#111827',
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1,
        titleColor: 'rgba(240,244,255,0.5)',
        bodyColor: '#f0f4ff',
        callbacks: {
          label: (ctx: { dataset: { label?: string }; parsed: { y: number } }) =>
            `${ctx.dataset.label}: ${formatPrice(ctx.parsed.y, lang)}`,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'rgba(240,244,255,0.3)',
          font: { size: 10 },
          maxTicksLimit: 8,
          maxRotation: 0,
        },
        grid: { color: 'rgba(255,255,255,0.04)' },
      },
      y: {
        position: 'right' as const,
        ticks: {
          color: 'rgba(240,244,255,0.3)',
          font: { size: 10 },
          callback: (v: unknown) => formatPrice(v as number, lang),
        },
        grid: { color: 'rgba(255,255,255,0.04)' },
      },
    },
  };

  return (
    <div className="chart-card card">
      <div className="card-header">
        <span className="card-title">{t('chart.priceTitle')} · {symbol}</span>
        <span className="card-subtitle">{history.length} pts</span>
      </div>
      <div className="chart-container">
        {history.length > 1
          ? <Line data={data} options={options} />
          : <p className="anomaly-empty">{t('chart.noData')}</p>}
      </div>
    </div>
  );
}
