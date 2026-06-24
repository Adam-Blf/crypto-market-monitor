# Security

## Reporting vulnerabilities

Please report security issues privately via GitHub Security Advisories at:
https://github.com/Adam-Blf/crypto-market-monitor/security/advisories

## Security measures

- HTTP security headers via Helmet (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- Rate limiting: 200 requests per 15 minutes per IP on all REST endpoints
- CORS restricted to configured origin only (CORS_ORIGIN env var)
- No stack traces exposed in production HTTP responses
- Environment variables validated at startup with Zod schema - process exits on invalid config
- Docker containers run as non-root user (appuser in appgroup)
- Request body size limited to 10KB to prevent payload flooding
- Kafka topics use separate consumer groups per service (no cross-contamination)
- No secrets committed - enforced via .gitignore patterns (*.env.*, *secret*, *.token, ghp_*, sbp_*)

## Environment hardening checklist

Before deploying to production:

- [ ] Set CORS_ORIGIN to the exact dashboard URL (not a wildcard)
- [ ] Set NODE_ENV=production to suppress error details in HTTP responses
- [ ] Review RATE_LIMIT_MAX and RATE_LIMIT_WINDOW_MS for your traffic profile
- [ ] Ensure .env is never committed (check .gitignore)
- [ ] Use Docker secrets or a vault for KAFKA_BROKERS if Kafka is remote
- [ ] Enable TLS on Kafka listeners for production deployments
