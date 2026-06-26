import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { AlertConfig, CryptoSymbol } from '../types';
import { SYMBOLS } from '../types';

interface Props {
  alerts: AlertConfig[];
  updateAlert: (sym: CryptoSymbol, patch: Partial<AlertConfig>) => void;
  onClose: () => void;
  requestPermission: () => void;
}

export function AlertModal({ alerts, updateAlert, onClose, requestPermission }: Props) {
  const [activeTab, setActiveTab] = useState<CryptoSymbol>(SYMBOLS[0]);
  const current = alerts.find(a => a.symbol === activeTab) ?? { symbol: activeTab, enabled: false };

  const set = (patch: Partial<AlertConfig>) => updateAlert(activeTab, patch);

  return (
    <AnimatePresence>
      <motion.div
        className="alert-overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className="alert-modal card"
          initial={{ opacity: 0, scale: 0.94, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.94, y: 20 }}
          transition={{ type: 'spring', stiffness: 350, damping: 30 }}
          onClick={e => e.stopPropagation()}
        >
          <div className="alert-modal-header">
            <span className="card-title">Alertes prix</span>
            <button className="alert-close-btn" onClick={onClose} aria-label="Fermer">✕</button>
          </div>

          <div className="alert-notif-row">
            <span className="alert-notif-label">Notifications navigateur</span>
            <button className="alert-perm-btn" onClick={requestPermission}>
              {'Notification' in window && Notification.permission === 'granted'
                ? '✓ Activees'
                : 'Autoriser'}
            </button>
          </div>

          <div className="alert-symbol-tabs">
            {SYMBOLS.map(sym => (
              <button
                key={sym}
                className={`alert-sym-tab${activeTab === sym ? ' active' : ''}`}
                onClick={() => setActiveTab(sym)}
              >
                {sym.split('-')[0]}
              </button>
            ))}
          </div>

          <div className="alert-fields">
            <label className="alert-toggle-row">
              <span>Activer les alertes {activeTab}</span>
              <input
                type="checkbox"
                checked={current.enabled}
                onChange={e => set({ enabled: e.target.checked })}
                className="alert-checkbox"
              />
            </label>

            <div className="alert-field-group">
              <label className="alert-field-label">Prix au-dessus ($)</label>
              <input
                type="number"
                className="alert-input"
                placeholder="ex: 70000"
                value={current.priceAbove ?? ''}
                onChange={e => set({ priceAbove: e.target.value ? Number(e.target.value) : undefined })}
                disabled={!current.enabled}
              />
            </div>

            <div className="alert-field-group">
              <label className="alert-field-label">Prix en-dessous ($)</label>
              <input
                type="number"
                className="alert-input"
                placeholder="ex: 60000"
                value={current.priceBelow ?? ''}
                onChange={e => set({ priceBelow: e.target.value ? Number(e.target.value) : undefined })}
                disabled={!current.enabled}
              />
            </div>

            <div className="alert-field-group">
              <label className="alert-field-label">Anomalie z-score &gt;</label>
              <input
                type="number"
                className="alert-input"
                placeholder="ex: 2.5"
                step="0.1"
                value={current.zscoreAbove ?? ''}
                onChange={e => set({ zscoreAbove: e.target.value ? Number(e.target.value) : undefined })}
                disabled={!current.enabled}
              />
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
