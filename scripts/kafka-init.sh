#!/bin/bash
# Initialize Kafka KRaft mode (runs once on first start)

KAFKA_DIR=/opt/kafka
LOG_DIR=/var/kafka-data

mkdir -p "$LOG_DIR"

# Generate cluster UUID if not already done
if [ ! -f "$LOG_DIR/.initialized" ]; then
  echo "Initializing Kafka KRaft cluster..."
  CLUSTER_ID=$("$KAFKA_DIR/bin/kafka-storage.sh" random-uuid)
  "$KAFKA_DIR/bin/kafka-storage.sh" format \
    --config "$KAFKA_DIR/config/kraft/server.properties" \
    --cluster-id "$CLUSTER_ID"
  touch "$LOG_DIR/.initialized"
  echo "Kafka KRaft initialized with cluster ID: $CLUSTER_ID"
fi

echo "Starting Kafka..."
exec "$KAFKA_DIR/bin/kafka-server-start.sh" "$KAFKA_DIR/config/kraft/server.properties"
