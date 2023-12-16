from btcusdt_5m_websocket import binance_ws
from functools import partial
from utils import print_kline 
from utils import print_processed_data
import config
import asyncio
import datetime
import psycopg2
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

async def process_and_save_data(json_message, strategy):
    try:
        kline = json_message['k']
        print_kline(kline)

        if kline['x']:  # Check if the candlestick is closed
            processed_data = {
                'timestamp': datetime.datetime.fromtimestamp(kline['T'] / 1000.0),
                'open': kline['o'],
                'high': kline['h'],
                'low': kline['l'],
                'close': kline['c'],
                'volume': kline['v']
            }
            print_processed_data(processed_data)
            await save_to_database(processed_data)
            strategy()
    except Exception as e:
        logging.error(f"Data processing error: {e}")

async def save_to_database(data):
    try:
        conn = psycopg2.connect(**config.DATABASE_CONFIG)
        cur = conn.cursor()

        # Assuming data contains fields like timestamp, open, close, etc.
        cur.execute("""
            INSERT INTO btcusdt_5m (timestamp, open, high, low, close, volume) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['timestamp'], data['open'], data['high'], data['low'], data['close'], data['volume']))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")
        # Optionally, re-raise the exception or handle it as needed

async def start_5m_data_collection(strategy):
    strategy_func = partial(process_and_save_data, strategy=strategy)
    await binance_ws(strategy_func)

if __name__ == '__main__':
    asyncio.run(start_5m_data_collection())
