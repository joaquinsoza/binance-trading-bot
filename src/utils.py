from datetime import datetime

# Function to format timestamp
def format_timestamp(epoch_ms):
    return datetime.fromtimestamp(epoch_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Modify the print statement for KLINE
def print_kline(kline):
    print(f"KLINE: Time: {format_timestamp(kline['t'])}, "
          f"Open: {kline['o']}, High: {kline['h']}, Low: {kline['l']}, "
          f"Close: {kline['c']}, Volume: {kline['v']}")
    
# Modify the print statement for processed data
def print_processed_data(data):
    timestamp_formatted = data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    print(f"Processed Data: Time: {timestamp_formatted}, "
          f"Open: {data['open']}, High: {data['high']}, Low: {data['low']}, "
          f"Close: {data['close']}, Volume: {data['volume']}")
