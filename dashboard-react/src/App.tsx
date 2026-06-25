import { useState } from 'react';
import { I18nCtx, useI18nProvider } from './i18n';
import { useSocket } from './hooks/useSocket';
import type { CryptoSymbol } from './types';
import { Header } from './components/Header';
import { SymbolTabs } from './components/SymbolTabs';
import { HeroCard } from './components/HeroCard';
import { StatsRow } from './components/StatsRow';
import { PriceChart } from './components/PriceChart';
import { VolumeChart } from './components/VolumeChart';
import { AnomalyFeed } from './components/AnomalyFeed';
import { Footer } from './components/Footer';

function Dashboard() {
  const [currentSymbol, setCurrentSymbol] = useState<CryptoSymbol>('BTC-USDT');
  const { connected, demoMode, metrics, history, anomalies, serverStats, msgCount } = useSocket(currentSymbol);

  const currentMetrics = metrics[currentSymbol];
  const currentHistory = history[currentSymbol] ?? [];

  return (
    <>
      <div className="efrei-accent-bar" />
      <Header connected={connected} demoMode={demoMode} />
      <main className="main">
        <SymbolTabs current={currentSymbol} onChange={setCurrentSymbol} />
        <HeroCard symbol={currentSymbol} metrics={currentMetrics} />
        <StatsRow metrics={currentMetrics} />
        <div className="charts-grid">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <PriceChart history={currentHistory} symbol={currentSymbol} />
            <VolumeChart metricsAll={metrics} />
          </div>
          <AnomalyFeed anomalies={anomalies} />
        </div>
      </main>
      <Footer serverStats={serverStats} msgCount={msgCount} demoMode={demoMode} />
    </>
  );
}

export default function App() {
  const i18n = useI18nProvider();
  return (
    <I18nCtx.Provider value={i18n}>
      <Dashboard />
    </I18nCtx.Provider>
  );
}
