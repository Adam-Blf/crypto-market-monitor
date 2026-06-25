import { motion } from 'framer-motion';
import type { CryptoSymbol } from '../types';
import { SYMBOLS } from '../types';

const ICONS: Record<CryptoSymbol, string> = {
  'BTC-USDT': '/icons/bitcoin.svg',
  'ETH-USDT': '/icons/ethereum.svg',
  'BTC-USD': '/icons/coinbase.svg',
  'SOL-USDT': '/icons/solana.svg',
  'BNB-USDT': '/icons/bnb.svg',
  'XRP-USDT': '/icons/xrp.svg',
};

interface Props {
  current: CryptoSymbol;
  onChange: (s: CryptoSymbol) => void;
}

export function SymbolTabs({ current, onChange }: Props) {
  return (
    <nav className="symbol-tabs" role="tablist" aria-label="Paires de crypto-monnaies">
      {SYMBOLS.map(sym => (
        <button
          key={sym}
          className={`tab${current === sym ? ' active' : ''}`}
          role="tab"
          aria-selected={current === sym}
          data-symbol={sym}
          onClick={() => onChange(sym)}
        >
          <img src={ICONS[sym]} width={18} height={18} alt="" className="tab-icon-img" aria-hidden="true" />
          {sym}
          {current === sym && (
            <motion.span
              layoutId="tab-indicator"
              className="tab-active-indicator"
              initial={false}
              transition={{ type: 'spring', stiffness: 400, damping: 35 }}
            />
          )}
        </button>
      ))}
    </nav>
  );
}
