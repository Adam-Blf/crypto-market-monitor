# ============================================================
# Crypto Market Monitor - All-in-one container
# Contains: Kafka (KRaft) + Ingester + Processor + API + Dashboard (nginx)
# Single command: docker run -p 8080:8080 -p 3001:3001 crypto-monitor
# ============================================================

FROM eclipse-temurin:17-jre-jammy

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    nginx \
    supervisor \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Apache Kafka 3.7 (KRaft mode)
ENV KAFKA_VERSION=3.7.1
ENV SCALA_VERSION=2.13
RUN curl -sL "https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" \
    | tar xz -C /opt \
    && mv "/opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION}" /opt/kafka

# Configure Kafka KRaft
RUN sed -i 's|log.dirs=/tmp/kraft-combined-logs|log.dirs=/var/kafka-data|g' \
    /opt/kafka/config/kraft/server.properties \
    && echo "auto.create.topics.enable=true" >> /opt/kafka/config/kraft/server.properties \
    && echo "log.retention.hours=1" >> /opt/kafka/config/kraft/server.properties

# Copy init script
COPY scripts/kafka-init.sh /kafka-init.sh
RUN chmod +x /kafka-init.sh

# ---- Build Ingester ----
WORKDIR /app/ingester
COPY ingester/package*.json ./
RUN npm ci
COPY ingester/ ./
RUN npm run build && npm prune --omit=dev

# ---- Build Processor ----
WORKDIR /app/processor
COPY processor/package*.json ./
RUN npm ci
COPY processor/ ./
RUN npm run build && npm prune --omit=dev

# ---- Build API ----
WORKDIR /app/api
COPY api/package*.json ./
RUN npm ci
COPY api/ ./
RUN npm run build && npm prune --omit=dev

# ---- Dashboard (nginx) ----
COPY dashboard/ /usr/share/nginx/html/
COPY dashboard/nginx.conf /etc/nginx/sites-available/default

# Remove default nginx site
RUN rm -f /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Supervisord config
COPY scripts/supervisord.conf /etc/supervisor/conf.d/crypto-monitor.conf
RUN mkdir -p /var/log/supervisor /var/kafka-data

# Set Kafka supervisor to use init script
RUN sed -i 's|command=/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/kraft/server.properties|command=/kafka-init.sh|g' \
    /etc/supervisor/conf.d/crypto-monitor.conf

WORKDIR /app

# Expose ports
EXPOSE 8080 3001

# Start all services via supervisord
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
