from db_utils import fetch_data
from supertrend import supertrend
import pandas as pd
# Set pandas options to display all rows
pd.set_option('display.max_rows', None)

def check_historical_buy_sell_signals(df):
    signals = []
    for current in range(1, len(df.index)):
        previous = current - 1

        if not df['in_uptrend'][previous] and df['in_uptrend'][current]:
            signals.append({'timestamp': df['timestamp'][current], 'signal': 'buy', 'price': df['close'][current]})
        
        if df['in_uptrend'][previous] and not df['in_uptrend'][current]:
            signals.append({'timestamp': df['timestamp'][current], 'signal': 'sell', 'price': df['close'][current]})

    return pd.DataFrame(signals)

def simulate_transactions(signals_df, trade_amount=200):
    current_amount = 1000
    btc_held = 0

    for index, signal in signals_df.iterrows():
        price = signal['price']
        if signal['signal'] == 'buy':
            if current_amount >= trade_amount:
                print("BUYING")
                current_amount -= trade_amount
                btc_held += trade_amount / price  # Buy BTC with fixed USD amount
                print("bought:", btc_held, "BTC")
                print("current amount:", current_amount, "USDT")
                print("-------------------")
            else:
                print("current amount is less than trade_amount:", current_amount, "USDT")
        
        if signal['signal'] == 'sell' and btc_held > 0:
            print("SELLING")
            sell_amount = btc_held * price  # Sell all BTC held
            current_amount += sell_amount
            print("current_amount", current_amount)
            btc_held = 0  # Reset BTC held after selling
            print("-------------------")


def apply_trading_strategy(data):
    # Apply your trading strategy to the historical data
    # and return buy/sell signals
    # For example, using Supertrend:
    df = supertrend(data)
    # print(df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'in_uptrend']])
    df = check_historical_buy_sell_signals(df)
    return df

def main():
    historical_data = fetch_data()
    strategy_data = apply_trading_strategy(historical_data)
    profit_loss = simulate_transactions(strategy_data)

if __name__ == "__main__":
    main()