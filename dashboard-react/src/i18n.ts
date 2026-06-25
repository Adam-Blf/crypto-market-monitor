import { createContext, useContext, useState, useCallback } from 'react';
import type { LangCode } from './types';

const fr: Record<string, unknown> = {
  title: 'CRYPTO MONITOR',
  live: 'EN DIRECT',
  connecting: 'Connexion...',
  connected: 'Connecte',
  disconnected: 'Deconnecte',
  symbols: { label: 'Paires' },
  price: { current: 'Prix actuel', vwap: 'VWAP', sma20: 'SMA-20', high: 'Haut 1min', low: 'Bas 1min', lastUpdate: 'Derniere mise a jour' },
  stats: { volume: 'Volume (1min)', trades: 'Transactions (1min)', high: 'Haut (1min)', low: 'Bas (1min)', change1m: 'Var. 1min', change5m: 'Var. 5min' },
  chart: { price: 'Prix', sma20: 'SMA-20', priceTitle: 'Historique du prix', volume: 'Volume par paire (1min)', volume1m: 'Volume 1min', volumeTitle: 'Volume par paire (1min)', priceLabel: 'Prix', smaLabel: 'SMA20', noData: 'En attente de donnees...' },
  anomaly: { title: 'Alertes anomalies', empty: 'Aucune anomalie detectee', zscore: 'Score Z' },
  anomalies: { title: 'Alertes anomalies', empty: 'Aucune anomalie detectee', zscore: 'Score Z' },
  footer: { module: 'Ingenierie Temps Reel - M1 EFREI', authors: 'Adam Beloucif, Emilien Morice', demo: 'Mode demonstration', messages: 'messages' },
};

const en: Record<string, unknown> = {
  title: 'CRYPTO MONITOR',
  live: 'LIVE',
  connecting: 'Connecting...',
  connected: 'Connected',
  disconnected: 'Disconnected',
  symbols: { label: 'Pairs' },
  price: { current: 'Current price', vwap: 'VWAP', sma20: 'SMA-20', high: 'High 1min', low: 'Low 1min', lastUpdate: 'Last update' },
  stats: { volume: 'Volume (1min)', trades: 'Trades (1min)', high: 'High (1min)', low: 'Low (1min)', change1m: '1min chg', change5m: '5min chg' },
  chart: { price: 'Price', sma20: 'SMA-20', priceTitle: 'Price history', volume: 'Volume per pair (1min)', volume1m: 'Volume 1min', volumeTitle: 'Volume per pair (1min)', priceLabel: 'Price', smaLabel: 'SMA20', noData: 'Waiting for data...' },
  anomaly: { title: 'Anomaly alerts', empty: 'No anomaly detected', zscore: 'Z-Score' },
  anomalies: { title: 'Anomaly alerts', empty: 'No anomaly detected', zscore: 'Z-Score' },
  footer: { module: 'Real-Time Engineering - M1 EFREI', authors: 'Adam Beloucif, Emilien Morice', demo: 'Demo mode', messages: 'messages' },
};

const catalogs: Record<LangCode, Record<string, unknown>> = { fr, en };

function resolve(obj: Record<string, unknown>, key: string): string {
  const parts = key.split('.');
  let cur: unknown = obj;
  for (const p of parts) {
    if (cur == null || typeof cur !== 'object') return key;
    cur = (cur as Record<string, unknown>)[p];
  }
  return typeof cur === 'string' ? cur : key;
}

export interface I18nContext {
  lang: LangCode;
  t: (key: string) => string;
  setLang: (l: LangCode) => void;
}

export const I18nCtx = createContext<I18nContext>({
  lang: 'fr',
  t: (k) => k,
  setLang: () => undefined,
});

export function useI18n(): I18nContext {
  return useContext(I18nCtx);
}

export function useI18nProvider() {
  const stored = (localStorage.getItem('cmm-locale') as LangCode) || 'fr';
  const [lang, setLangState] = useState<LangCode>(stored);

  const t = useCallback((key: string) => resolve(catalogs[lang], key), [lang]);

  const setLang = useCallback((l: LangCode) => {
    localStorage.setItem('cmm-locale', l);
    setLangState(l);
  }, []);

  return { lang, t, setLang };
}
