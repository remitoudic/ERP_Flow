#!/bin/bash
set -e

# Create a separate database for Temporal to isolate its event-sourcing records
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE temporal;
    GRANT ALL PRIVILEGES ON DATABASE temporal TO "$POSTGRES_USER";
EOSQL

# Create high-performance cache tables using UNLOGGED to eliminate WAL overhead
# This matches our architecture design to replace Redis caching with native Postgres.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE UNLOGGED TABLE IF NOT EXISTS cache (
        key VARCHAR(255) PRIMARY KEY,
        value JSONB NOT NULL,
        ttl TIMESTAMPTZ NOT NULL DEFAULT (now() + interval '1 hour')
    );

    CREATE INDEX IF NOT EXISTS idx_cache_ttl ON cache(ttl);
EOSQL
