from db_utils import get_latest_timestamp
import ccxt
import psycopg2
import datetime
import config

def fetch_ohlcv(exchange, symbol, timeframe, limit):
    return exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

def fetch_all_ohlcv(exchange, symbol, timeframe, since, limit=1000):
    all_ohlcv = []
    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        print(ohlcv)
        if len(ohlcv) == 1:
            break
        all_ohlcv += ohlcv
        since = ohlcv[-1][0]  # Update 'since' to the timestamp of the last data point
        print("Getting data from",datetime.datetime.fromtimestamp(since/1000))
    return all_ohlcv

def save_to_database(data):
    conn = psycopg2.connect(**config.DATABASE_CONFIG)
    cur = conn.cursor()

    for entry in data:
        timestamp = datetime.datetime.fromtimestamp(entry[0] / 1000.0)
        cur.execute("""
            INSERT INTO btcusdt_5m (timestamp, open, high, low, close, volume) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
        """, (timestamp, entry[1], entry[2], entry[3], entry[4], entry[5]))

    conn.commit()
    cur.close()
    conn.close()

def fetch_historical_data():
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    timeframe = '5m'
    since = exchange.parse8601('2023-10-01T00:00:00Z')  # starting date
    print("starting date", datetime.datetime.fromtimestamp(since/1000))

    latest_timestamp = get_latest_timestamp()
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

    if latest_timestamp is not None:
        delta = now - latest_timestamp
        intervals_missing = int(delta.total_seconds() / 300)
        print("intervals_missing:", intervals_missing)

        if intervals_missing > 0:
            ohlcv = fetch_ohlcv(exchange, symbol, timeframe, min(intervals_missing, 1000))
            save_to_database(ohlcv)
        else:
            print("No new data to fetch. Database is up-to-date.")
    else:
        # Default value for initial population
        ohlcv = fetch_all_ohlcv(exchange, symbol, timeframe, since, 1000)
        save_to_database(ohlcv)


if __name__ == '__main__':
    fetch_historical_data()
