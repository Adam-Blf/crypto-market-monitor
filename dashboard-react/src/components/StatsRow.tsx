import { motion } from 'framer-motion';
import type { Metrics } from '../types';
import { useI18n } from '../i18n';
import { formatPrice, formatVolume } from '../utils';

interface Props {
  metrics: Metrics | undefined;
}

const stagger = {
  animate: { transition: { staggerChildren: 0.07 } },
};

const cardVariant = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3, ease: 'easeOut' } },
};

export function StatsRow({ metrics }: Props) {
  const { t, lang } = useI18n();

  const cards = [
    { label: t('stats.volume'), value: formatVolume(metrics?.volumeTotal1m), cls: '' },
    { label: t('stats.trades'), value: String(metrics?.tradeCount1m ?? '-'), cls: '' },
    { label: t('stats.high'), value: formatPrice(metrics?.highPrice1m, lang), cls: 'positive' },
    { label: t('stats.low'), value: formatPrice(metrics?.lowPrice1m, lang), cls: 'negative' },
  ];

  return (
    <motion.div
      className="stats-row"
      role="region"
      aria-label="Statistiques du marche"
      variants={stagger}
      initial="initial"
      animate="animate"
    >
      {cards.map(c => (
        <motion.div key={c.label} className="stat-card card" variants={cardVariant}>
          <div className="stat-label">{c.label}</div>
          <div className={`stat-value${c.cls ? ' ' + c.cls : ''}`}>{c.value}</div>
        </motion.div>
      ))}
    </motion.div>
  );
}
