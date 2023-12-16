import psycopg2
import pandas as pd
import config

def fetch_data():
    conn = psycopg2.connect(**config.DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, open, high, low, close, volume FROM btcusdt_5m ORDER BY timestamp ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Convert to DataFrame and ensure numeric columns are of type float
    df = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    df[numeric_columns] = df[numeric_columns].astype(float)
    return df

def get_latest_timestamp():
    conn = psycopg2.connect(**config.DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT MAX(timestamp) FROM btcusdt_5m")
    latest_timestamp = cur.fetchone()[0]
    cur.close()
    conn.close()
    return latest_timestamp