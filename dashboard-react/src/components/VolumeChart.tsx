import { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, BarElement, Tooltip, Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import type { Metrics } from '../types';
import { SYMBOLS } from '../types';
import { useI18n } from '../i18n';
import { formatVolume } from '../utils';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const COLORS: Record<string, string> = {
  'BTC-USDT': '#F59E0B',
  'ETH-USDT': '#8B5CF6',
  'BTC-USD': '#3b82f6',
  'SOL-USDT': '#14F195',
  'BNB-USDT': '#F0B90B',
  'XRP-USDT': '#00AAE4',
};

interface Props {
  metricsAll: Record<string, Metrics>;
}

export function VolumeChart({ metricsAll }: Props) {
  const { t } = useI18n();

  const { labels, volumes } = useMemo(() => ({
    labels: SYMBOLS,
    volumes: SYMBOLS.map(s => metricsAll[s]?.volumeTotal1m ?? 0),
  }), [metricsAll]);

  const data = {
    labels,
    datasets: [{
      label: t('chart.volume1m'),
      data: volumes,
      backgroundColor: SYMBOLS.map(s => `${COLORS[s]}33`),
      borderColor: SYMBOLS.map(s => COLORS[s]),
      borderWidth: 2,
      borderRadius: 6,
    }],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#111827',
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1,
        titleColor: 'rgba(240,244,255,0.5)',
        bodyColor: '#f0f4ff',
        callbacks: {
          label: (ctx: { parsed: { y: number } }) => formatVolume(ctx.parsed.y),
        },
      },
    },
    scales: {
      x: {
        ticks: { color: 'rgba(240,244,255,0.4)', font: { size: 11 } },
        grid: { display: false },
      },
      y: {
        ticks: {
          color: 'rgba(240,244,255,0.3)',
          font: { size: 10 },
          callback: (v: unknown) => formatVolume(v as number),
        },
        grid: { color: 'rgba(255,255,255,0.04)' },
      },
    },
  };

  return (
    <div className="volume-card card">
      <div className="card-header">
        <span className="card-title">{t('chart.volumeTitle')}</span>
      </div>
      <div className="chart-container chart-container--short">
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}
