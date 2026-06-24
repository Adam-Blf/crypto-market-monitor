#!/usr/bin/env node
'use strict';

import { spawn, execSync } from 'node:child_process';
import { existsSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..', '..');

// ANSI color helpers
const c = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  amber: '\x1b[33m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
  gray: '\x1b[90m',
  cyan: '\x1b[36m',
};

function log(prefix, color, msg) {
  const ts = new Date().toLocaleTimeString('fr-FR', { hour12: false });
  console.log(`${c.gray}${ts}${c.reset} ${color}${c.bold}[${prefix}]${c.reset} ${msg}`);
}

function banner() {
  console.log('');
  console.log(`${c.amber}${c.bold}  ██████ ███╗   ███╗███╗   ███╗${c.reset}`);
  console.log(`${c.amber}${c.bold} ██╔════╝████╗ ████║████╗ ████║${c.reset}`);
  console.log(`${c.amber}${c.bold} ██║     ██╔████╔██║██╔████╔██║${c.reset}`);
  console.log(`${c.amber}${c.bold} ██║     ██║╚██╔╝██║██║╚██╔╝██║${c.reset}`);
  console.log(`${c.amber}${c.bold} ╚██████╗██║ ╚═╝ ██║██║ ╚═╝ ██║${c.reset}`);
  console.log(`${c.amber}${c.bold}  ╚═════╝╚═╝     ╚═╝╚═╝     ╚═╝${c.reset}`);
  console.log('');
  console.log(`  ${c.bold}Crypto Market Monitor${c.reset}  ${c.gray}M1 EFREI - Real-Time Engineering${c.reset}`);
  console.log(`  ${c.gray}Adam Beloucif, Emilien Morice - 2025-2026${c.reset}`);
  console.log('');
}

function checkDocker() {
  try {
    execSync('docker info', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function checkDockerCompose() {
  try {
    execSync('docker compose version', { stdio: 'ignore' });
    return true;
  } catch {
    try {
      execSync('docker-compose --version', { stdio: 'ignore' });
      return true;
    } catch {
      return false;
    }
  }
}

function getComposeCmd() {
  try {
    execSync('docker compose version', { stdio: 'ignore' });
    return 'docker compose';
  } catch {
    return 'docker-compose';
  }
}

function ensureEnvFile() {
  const envFile = join(ROOT, '.env');
  const exampleFile = join(ROOT, '.env.example');
  if (!existsSync(envFile) && existsSync(exampleFile)) {
    const { readFileSync } = require('node:fs');
    writeFileSync(envFile, readFileSync(exampleFile));
    log('ENV', c.amber, 'Created .env from .env.example');
  }
}

function waitForService(url, maxAttempts = 30, intervalMs = 2000) {
  return new Promise((resolve, reject) => {
    let attempts = 0;
    const check = async () => {
      attempts++;
      try {
        const ctrl = new AbortController();
        const timeout = setTimeout(() => ctrl.abort(), 1500);
        const res = await fetch(url, { signal: ctrl.signal });
        clearTimeout(timeout);
        if (res.ok) { resolve(); return; }
      } catch {}
      if (attempts >= maxAttempts) {
        reject(new Error(`Service not ready after ${maxAttempts} attempts: ${url}`));
        return;
      }
      setTimeout(check, intervalMs);
    };
    check();
  });
}

async function openBrowser(url) {
  try {
    const { default: open } = await import('open');
    await open(url);
  } catch {
    // open not available when compiled with pkg - use platform fallback
    const platform = process.platform;
    const cmd = platform === 'win32' ? `start ${url}` :
                platform === 'darwin' ? `open ${url}` : `xdg-open ${url}`;
    try { execSync(cmd, { stdio: 'ignore' }); } catch {}
  }
}

function spinnerStep(label) {
  const frames = ['|', '/', '-', '\\'];
  let i = 0;
  const iv = setInterval(() => {
    process.stdout.write(`\r  ${c.amber}${frames[i++ % frames.length]}${c.reset} ${label}...`);
  }, 100);
  return () => {
    clearInterval(iv);
    process.stdout.write(`\r  ${c.green}OK${c.reset} ${label}           \n`);
  };
}

async function start() {
  banner();

  // 1. Prerequisites
  log('CHECK', c.blue, 'Verifying Docker...');
  if (!checkDocker()) {
    log('ERROR', c.red, 'Docker is not running. Start Docker Desktop and retry.');
    process.exit(1);
  }
  if (!checkDockerCompose()) {
    log('ERROR', c.red, 'docker compose not found. Install Docker Desktop >= 3.x.');
    process.exit(1);
  }
  log('CHECK', c.green, 'Docker OK');

  ensureEnvFile();

  const COMPOSE = getComposeCmd();

  // 2. Build and start
  log('STACK', c.amber, 'Building and starting services (first run may take 2-3 minutes)...');
  console.log('');

  const done = spinnerStep('Starting Kafka + services');

  await new Promise((resolve, reject) => {
    const proc = spawn(
      COMPOSE,
      ['up', '--build', '-d', '--remove-orphans'],
      { cwd: ROOT, shell: true, stdio: ['ignore', 'pipe', 'pipe'] }
    );

    proc.stderr.on('data', (data) => {
      const line = data.toString().trim();
      if (line) process.stdout.write(`  ${c.gray}${line}${c.reset}\n`);
    });

    proc.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`docker compose up exited with code ${code}`));
    });
  });

  done();

  // 3. Wait for API health
  const doneApi = spinnerStep('Waiting for API health');
  try {
    await waitForService('http://localhost:3001/api/health');
    doneApi();
  } catch (err) {
    process.stdout.write(`\r  ${c.amber}WARN${c.reset} API not yet ready, opening dashboard anyway\n`);
  }

  // 4. Open browser
  log('OPEN', c.cyan, 'Opening dashboard at http://localhost:8080');
  await openBrowser('http://localhost:8080');

  console.log('');
  console.log(`  ${c.bold}Services running:${c.reset}`);
  console.log(`  ${c.amber}-${c.reset} Dashboard    http://localhost:8080`);
  console.log(`  ${c.amber}-${c.reset} API          http://localhost:3001/api/health`);
  console.log(`  ${c.amber}-${c.reset} Kafka UI     http://localhost:8090`);
  console.log('');
  console.log(`  ${c.gray}Press Ctrl+C to stop all services.${c.reset}`);
  console.log('');

  // 5. Stream logs
  const logProc = spawn(COMPOSE, ['logs', '-f', '--tail=20'], {
    cwd: ROOT,
    shell: true,
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  logProc.stdout.on('data', (d) => {
    const lines = d.toString().split('\n');
    lines.forEach(l => { if (l.trim()) console.log(`  ${c.gray}${l}${c.reset}`); });
  });

  logProc.stderr.on('data', (d) => {
    const lines = d.toString().split('\n');
    lines.forEach(l => { if (l.trim()) console.log(`  ${c.gray}${l}${c.reset}`); });
  });

  // 6. Graceful shutdown
  const shutdown = async (signal) => {
    console.log('');
    log('STOP', c.amber, `Received ${signal} - stopping services...`);
    logProc.kill();
    const stop = spawn(COMPOSE, ['down'], { cwd: ROOT, shell: true, stdio: 'inherit' });
    stop.on('close', () => {
      log('STOP', c.green, 'All services stopped. Bye!');
      process.exit(0);
    });
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
}

start().catch((err) => {
  console.error(`\n  ${c.red}${c.bold}Fatal error:${c.reset} ${err.message}`);
  process.exit(1);
});
