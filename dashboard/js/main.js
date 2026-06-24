'use strict';

/* ============================================================
   CONFIG
   ============================================================ */
const API_URL = 'http://localhost:3001';
const MAX_CHART_POINTS = 100;
const MAX_ANOMALIES    = 50;

/* ============================================================
   STATE
   ============================================================ */
const state = {
  currentSymbol : 'BTC-USDT',
  metrics       : {},   // symbol -> latest Metrics
  history       : {},   // symbol -> Metrics[] (ring buffer)
  anomalies     : [],   // Metrics[] newest first
  msgCount      : 0,
  msgCountStart : Date.now(),
  socket        : null,
};

/* ============================================================
   CHARTS
   ============================================================ */
let priceChart  = null;
let volumeChart = null;

const CHART_DEFAULTS = {
  plugins: {
    legend: {
      labels: {
        color: 'rgba(240,244,255,0.6)',
        font: { size: 11, family: 'Inter' },
        boxWidth: 12,
      },
    },
    tooltip: {
      backgroundColor: '#1a2236',
      borderColor: 'rgba(255,255,255,0.1)',
      borderWidth: 1,
      titleColor: 'rgba(240,244,255,0.9)',
      bodyColor : 'rgba(240,244,255,0.6)',
      cornerRadius: 8,
    },
  },
  scales: {
    x: {
      display: false,
      grid: { color: 'rgba(255,255,255,0.04)' },
    },
    y: {
      grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
      ticks: { color: 'rgba(240,244,255,0.45)', font: { size: 11 } },
    },
  },
  animation: { duration: 150 },
  responsive: true,
  maintainAspectRatio: false,
};

function initPriceChart() {
  const ctx = document.getElementById('priceChart').getContext('2d');
  const gradient = ctx.createLinearGradient(0, 0, 0, 280);
  gradient.addColorStop(0,   'rgba(0,245,160,0.18)');
  gradient.addColorStop(1,   'rgba(0,245,160,0)');

  priceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Price',
          data: [],
          borderColor: '#00f5a0',
          backgroundColor: gradient,
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 4,
          tension: 0.3,
          fill: true,
        },
        {
          label: 'SMA20',
          data: [],
          borderColor: 'rgba(59,130,246,0.7)',
          backgroundColor: 'transparent',
          borderWidth: 1.5,
          borderDash: [5, 3],
          pointRadius: 0,
          tension: 0.3,
          fill: false,
        },
      ],
    },
    options: {
      ...CHART_DEFAULTS,
      interaction: { mode: 'index', intersect: false },
    },
  });
}

function initVolumeChart() {
  const ctx = document.getElementById('volumeChart').getContext('2d');
  volumeChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['BTC-USDT', 'ETH-USDT', 'BTC-USD'],
      datasets: [
        {
          label: 'Volume (1m)',
          data: [0, 0, 0],
          backgroundColor: [
            'rgba(0,245,160,0.55)',
            'rgba(59,130,246,0.55)',
            'rgba(255,171,0,0.55)',
          ],
          borderColor: [
            '#00f5a0',
            '#3b82f6',
            '#ffab00',
          ],
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    },
    options: {
      ...CHART_DEFAULTS,
      scales: {
        ...CHART_DEFAULTS.scales,
        x: {
          display: true,
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: 'rgba(240,244,255,0.45)', font: { size: 11 } },
        },
      },
      plugins: {
        ...CHART_DEFAULTS.plugins,
        legend: { display: false },
      },
    },
  });
}

function pushToHistory(symbol, metrics) {
  if (!state.history[symbol]) state.history[symbol] = [];
  state.history[symbol].push(metrics);
  if (state.history[symbol].length > MAX_CHART_POINTS) {
    state.history[symbol].shift();
  }
}

function refreshPriceChart(symbol) {
  const history = state.history[symbol] || [];
  priceChart.data.labels                 = history.map(() => '');
  priceChart.data.datasets[0].data       = history.map(m => m.currentPrice);
  priceChart.data.datasets[1].data       = history.map(m => m.sma20);
  priceChart.update('none');
  document.getElementById('chartSymbolLabel').textContent = symbol;
}

function refreshVolumeChart() {
  const symbols = ['BTC-USDT', 'ETH-USDT', 'BTC-USD'];
  volumeChart.data.datasets[0].data = symbols.map(s =>
    state.metrics[s] ? state.metrics[s].volumeTotal1m : 0
  );
  volumeChart.update('none');
}

/* ============================================================
   FORMATTING HELPERS
   ============================================================ */
function formatPrice(n) {
  if (n == null || isNaN(n)) return '-';
  return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatVolume(n) {
  if (n == null || isNaN(n)) return '-';
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(2) + 'M';
  if (n >= 1_000)     return (n / 1_000).toFixed(2) + 'K';
  return n.toFixed(2);
}

function formatPct(n) {
  if (n == null || isNaN(n)) return '0.00%';
  const sign = n >= 0 ? '+' : '';
  return sign + n.toFixed(2) + '%';
}

function formatTime(ts) {
  return new Date(ts).toLocaleTimeString('en-US', { hour12: false });
}

/* ============================================================
   RENDER
   ============================================================ */
function renderMetrics(metrics) {
  const prevPrice = state.metrics[metrics.symbol]?.currentPrice;
  state.metrics[metrics.symbol] = metrics;

  if (metrics.symbol !== state.currentSymbol) return;

  document.getElementById('heroSymbol').textContent = metrics.symbol;

  const priceEl = document.getElementById('heroPrice');
  const priceStr = formatPrice(metrics.currentPrice);
  if (priceEl.textContent !== priceStr) {
    priceEl.textContent = priceStr;
    if (prevPrice != null) {
      const cls = metrics.currentPrice > prevPrice ? 'flash-up' : 'flash-down';
      priceEl.classList.remove('flash-up', 'flash-down');
      void priceEl.offsetWidth;
      priceEl.classList.add(cls);
    }
  }

  const badge1m = document.getElementById('changeBadge1m');
  badge1m.textContent = formatPct(metrics.priceChange1m);
  badge1m.className   = 'change-badge ' + (metrics.priceChange1m >= 0 ? 'positive' : 'negative');

  const badge5m = document.getElementById('changeBadge5m');
  badge5m.textContent = formatPct(metrics.priceChange5m);
  badge5m.className   = 'change-badge ' + (metrics.priceChange5m >= 0 ? 'positive' : 'negative');

  document.getElementById('vwapValue').textContent  = formatPrice(metrics.vwap);
  document.getElementById('sma20Value').textContent = formatPrice(metrics.sma20);
  document.getElementById('lastUpdate').textContent = formatTime(metrics.timestamp);

  document.getElementById('volume1m').textContent     = formatVolume(metrics.volumeTotal1m);
  document.getElementById('tradeCount1m').textContent = metrics.tradeCount1m ?? '-';
  document.getElementById('high1m').textContent        = formatPrice(metrics.highPrice1m);
  document.getElementById('low1m').textContent         = formatPrice(metrics.lowPrice1m);
}

function addAnomalyToFeed(metrics) {
  state.anomalies.unshift(metrics);
  if (state.anomalies.length > MAX_ANOMALIES) state.anomalies.pop();

  const list = document.getElementById('anomalyList');
  const empty = list.querySelector('.anomaly-empty');
  if (empty) empty.remove();

  const item = document.createElement('div');
  item.className = 'anomaly-item';
  item.innerHTML = `
    <div class="anomaly-item-header">
      <span class="anomaly-symbol">${metrics.symbol}</span>
      <span class="anomaly-time">${formatTime(metrics.timestamp)}</span>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;">
      <span class="anomaly-price">$${formatPrice(metrics.currentPrice)}</span>
      <span class="zscore-badge">z-score ${metrics.anomalyScore.toFixed(2)}</span>
    </div>
  `;
  list.prepend(item);

  if (list.children.length > MAX_ANOMALIES) {
    list.removeChild(list.lastChild);
  }

  document.getElementById('anomalyCount').textContent = state.anomalies.length;
  playAnomalyBeep();
}

function playAnomalyBeep() {
  try {
    const ac  = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.connect(gain);
    gain.connect(ac.destination);
    osc.frequency.value = 880;
    osc.type = 'sine';
    gain.gain.setValueAtTime(0.08, ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.25);
    osc.start();
    osc.stop(ac.currentTime + 0.25);
  } catch (_) { /* AudioContext not available */ }
}

/* ============================================================
   TAB SWITCHING
   ============================================================ */
function initTabs() {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      state.currentSymbol = tab.dataset.symbol;
      if (state.socket?.connected) {
        state.socket.emit('subscribe:symbol', state.currentSymbol);
      }
      const current = state.metrics[state.currentSymbol];
      if (current) renderMetrics(current);
      fetchHistoryAndRefreshChart(state.currentSymbol);
    });
  });
}

async function fetchHistoryAndRefreshChart(symbol) {
  try {
    const res  = await fetch(`${API_URL}/api/history/${symbol}?limit=${MAX_CHART_POINTS}`);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    if (Array.isArray(data)) {
      state.history[symbol] = data;
    }
  } catch (_) { /* server may not be ready */ }
  refreshPriceChart(symbol);
}

/* ============================================================
   SOCKET.IO
   ============================================================ */
function connectSocket() {
  const socket = io(API_URL, {
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    transports: ['websocket', 'polling'],
  });
  state.socket = socket;

  socket.on('connect', () => {
    setConnectionStatus(true);
    socket.emit('subscribe:symbol', state.currentSymbol);
    fetchHistoryAndRefreshChart(state.currentSymbol);
  });

  socket.on('disconnect', () => setConnectionStatus(false));
  socket.on('connect_error', () => setConnectionStatus(false));

  socket.on('metrics:update', (metrics) => {
    state.msgCount++;
    pushToHistory(metrics.symbol, metrics);
    renderMetrics(metrics);
    if (metrics.symbol === state.currentSymbol) {
      refreshPriceChart(state.currentSymbol);
    }
    refreshVolumeChart();
  });

  socket.on('anomaly:detected', (metrics) => {
    addAnomalyToFeed(metrics);
  });

  socket.on('server:stats', (stats) => {
    document.getElementById('footerStats').textContent =
      `${stats.connections ?? '-'} clients - ${stats.msgsPerSec ?? '-'} msg/s`;
  });
}

function setConnectionStatus(connected) {
  const dot   = document.getElementById('statusDot');
  const label = document.getElementById('statusLabel');
  if (connected) {
    dot.classList.add('connected');
    label.textContent = 'Connected';
  } else {
    dot.classList.remove('connected');
    label.textContent = 'Disconnected';
  }
}

/* ============================================================
   CLOCK
   ============================================================ */
function startClock() {
  const el = document.getElementById('clock');
  function tick() {
    el.textContent = new Date().toLocaleTimeString('en-US', { hour12: false });
  }
  tick();
  setInterval(tick, 1000);
}

/* ============================================================
   INIT
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initPriceChart();
  initVolumeChart();
  startClock();
  connectSocket();
});
