import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("SUPABASE_CONNECTION_STRING")

def run_db_init():
    """
    Directly connects to Postgres to initialize the schema.
    This bypasses the Supabase API entirely.
    """
    
    sql_commands = """
    -- 1. Enable UUID support
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- 2. News Table
    CREATE TABLE IF NOT EXISTS news (
        news_id TEXT PRIMARY KEY,
        event TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        content TEXT,
        link TEXT UNIQUE,
        is_read BOOLEAN DEFAULT FALSE,
        published TEXT,
        type TEXT DEFAULT 'news',
        timestamp DOUBLE PRECISION,
        location JSONB DEFAULT '{"name": null, "lat": null, "lon": null}',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- 3. Alerts Table
    CREATE TABLE IF NOT EXISTS alerts (
        alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        event TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        content TEXT,
        actions JSONB DEFAULT '[]'::jsonb NOT NULL,
        sources JSONB DEFAULT '[]'::jsonb NOT NULL,
        location JSONB DEFAULT '{"name": null, "lat": null, "lon": null}'::jsonb NOT NULL,
        is_read BOOLEAN DEFAULT false NOT NULL,
        is_active BOOLEAN DEFAULT true NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
        updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
    );

    -- 4. Indexes
    CREATE INDEX IF NOT EXISTS idx_alerts_location_name ON alerts ((location->>'name'));
    CREATE INDEX IF NOT EXISTS idx_alerts_is_active ON alerts (is_active);

    -- 5. Auto-update Timestamp Logic
    CREATE OR REPLACE FUNCTION update_modified_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ language 'plpgsql';

    -- 6. Apply Trigger to Alerts
    DROP TRIGGER IF EXISTS update_alerts_modtime ON alerts;
    CREATE TRIGGER update_alerts_modtime
        BEFORE UPDATE ON alerts
        FOR EACH ROW
        EXECUTE PROCEDURE update_modified_column();
    """

    conn = None
    try:
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True 
        
        with conn.cursor() as cur:
            cur.execute(sql_commands)
            
        print("Supabase schema (tables, triggers, and indexes) initialized.")
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_db_init()