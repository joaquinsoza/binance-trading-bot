import asyncio
from init_database import initialize_database
from fetch_historical_data import fetch_historical_data
from btcusdt_5m_data_collector import start_5m_data_collection
from supertrend import supertrend_strategy

def main():
    # Initialize database
    initialize_database()

    # Fetch historical data
    fetch_historical_data()

    # Run asynchronous tasks
    asyncio.run(start_5m_data_collection(supertrend_strategy))

if __name__ == "__main__":
    main()
