import os
import json
import psycopg
import logfire

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "erp_flow")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres_secure_password")

CONN_STRING = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg.connect(CONN_STRING)

def cache_get(key: str):
    """Retrieve value from the PostgreSQL UNLOGGED cache table."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT value FROM cache WHERE key = %s AND ttl > now();",
                    (key,)
                )
                row = cur.fetchone()
                if row:
                    logfire.info("Cache hit for key: {key}", key=key)
                    return row[0]
    except Exception as e:
        logfire.error("Failed to query cache database: {error}", error=str(e))
    return None

def cache_set(key: str, value: dict, expire_interval: str = "1 hour"):
    """Insert or update a value in the PostgreSQL UNLOGGED cache table."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = f"""
                INSERT INTO cache (key, value, ttl)
                VALUES (%s, %s, now() + interval '{expire_interval}')
                ON CONFLICT (key) DO UPDATE
                SET value = EXCLUDED.value, ttl = EXCLUDED.ttl;
                """
                cur.execute(query, (key, json.dumps(value)))
                conn.commit()
                logfire.info("Cache saved for key: {key}", key=key)
    except Exception as e:
        logfire.error("Failed to set cache database: {error}", error=str(e))

def publish_event(channel: str, message: dict):
    """Publish an event to a PostgreSQL LISTEN/NOTIFY channel."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                payload = json.dumps(message)
                # Use standard escape identifiers or parameters
                cur.execute(f"NOTIFY {channel}, %s;", (payload,))
                conn.commit()
                logfire.info("Published event on channel {channel}: {payload}", channel=channel, payload=payload)
    except Exception as e:
        logfire.error("Failed to publish event: {error}", error=str(e))
