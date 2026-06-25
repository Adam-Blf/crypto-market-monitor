import { motion, AnimatePresence } from 'framer-motion';
import type { AnomalyEvent } from '../types';
import { useI18n } from '../i18n';
import { formatPrice, formatTime } from '../utils';

interface Props {
  anomalies: AnomalyEvent[];
}

export function AnomalyFeed({ anomalies }: Props) {
  const { t, lang } = useI18n();

  return (
    <div className="anomaly-card card" role="region" aria-label="Flux d'anomalies">
      <div className="card-header">
        <span className="card-title">{t('anomaly.title')}</span>
        {anomalies.length > 0 && (
          <motion.span
            className="anomaly-count-badge"
            aria-live="polite"
            key={anomalies.length}
            initial={{ scale: 1.4 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 500, damping: 20 }}
          >
            {anomalies.length}
          </motion.span>
        )}
      </div>
      <div className="anomaly-list" role="list">
        {anomalies.length === 0 ? (
          <p className="anomaly-empty">{t('anomaly.empty')}</p>
        ) : (
          <AnimatePresence initial={false}>
            {anomalies.map((a, i) => (
              <motion.div
                key={`${a.symbol}-${a.timestamp}-${i}`}
                className="anomaly-item"
                role="listitem"
                initial={{ opacity: 0, x: 20, height: 0 }}
                animate={{ opacity: 1, x: 0, height: 'auto' }}
                exit={{ opacity: 0, x: -20, height: 0 }}
                transition={{ duration: 0.25, ease: 'easeOut' }}
              >
                <div className="anomaly-item-header">
                  <span className="anomaly-symbol">{a.symbol}</span>
                  <span className="anomaly-time">{formatTime(a.timestamp, lang)}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                  <span className="anomaly-price">{formatPrice(a.currentPrice, lang)}</span>
                  <span className="zscore-badge">z={a.anomalyScore.toFixed(2)}</span>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}
