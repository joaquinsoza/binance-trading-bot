# init_database.py

import psycopg2
import config

def initialize_database():
    conn = psycopg2.connect(**config.DATABASE_CONFIG)
    cur = conn.cursor()

    # Check if the table already exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_tables
            WHERE schemaname = 'public' AND tablename  = 'btcusdt_5m'
        );
    """)
    table_exists = cur.fetchone()[0]

    if table_exists:
        print("Table 'btcusdt_5m' already exists.")
    else:
        print("Creating table 'btcusdt_5m'.")

        # Create table for BTC/USDT 5-minute intervals with a unique constraint on timestamp
        cur.execute("""
            CREATE TABLE btcusdt_5m (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL UNIQUE,
                open NUMERIC NOT NULL,
                high NUMERIC NOT NULL,
                low NUMERIC NOT NULL,
                close NUMERIC NOT NULL,
                volume NUMERIC NOT NULL
            )
        """)
        print("Table 'btcusdt_5m' created.")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    initialize_database()
