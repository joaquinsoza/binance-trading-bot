from db_utils import fetch_data
from supertrend import supertrend
import pandas as pd
# Set pandas options to display all rows
pd.set_option('display.max_rows', None)

def calculate_ema(data, period):
    return data['close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def apply_combined_strategy(data):
    # Calculate EMAs
    data['ema20'] = calculate_ema(data, 20)
    data['ema50'] = calculate_ema(data, 50)
    data['ema100'] = calculate_ema(data, 100)
    data['ema200'] = calculate_ema(data, 200)

    # Calculate RSI
    data['rsi'] = calculate_rsi(data)
    # Apply Supertrend
    data = supertrend(data)
    # Add a column for Buy/Sell signals
    return data

def check_historical_buy_sell_signals(df):
    signals = []
    for current in range(1, len(df.index)):
        previous = current - 1

        # Buy condition: Supertrend turns positive, EMA20 is above EMA200, and RSI indicates oversold
        if not df['in_uptrend'][previous] and df['in_uptrend'][current] and df['ema20'][current] > df['ema200'][current]:
            signals.append({'timestamp': df['timestamp'][current], 'signal': 'buy', 'price': df['close'][current]})
            
        # Sell condition: Supertrend turns negative, EMA20 is below EMA200, and RSI indicates overbought
        if df['in_uptrend'][previous] and not df['in_uptrend'][current] and df['ema20'][current] < df['ema200'][current] and df['rsi'][current] > 45:
            signals.append({'timestamp': df['timestamp'][current], 'signal': 'sell', 'price': df['close'][current]})
            
    return pd.DataFrame(signals)

def simulate_transactions(signals_df, trade_amount=1000):
    in_position = False
    current_amount = 2000
    btc_held = 0
    transactions = []
    price_last_signal = 27059.26

    for index, signal in signals_df.iterrows():
        price = signal['price']
        timestamp = signal['timestamp']

        if signal['signal'] == 'buy' and not in_position:
            if current_amount >= trade_amount:
                btc_bought = trade_amount / price
                btc_held += btc_bought
                current_amount -= trade_amount
                in_position = True
                transactions.append({
                    'timestamp': timestamp,
                    'type': 'buy',
                    'price': price,
                    'price_last_signal': price_last_signal, 
                    'amount_usdt': trade_amount,
                    'btc_held': btc_held,
                    'current_amount': current_amount
                })
        
        elif signal['signal'] == 'sell' and btc_held > 0:
            sell_amount = btc_held * price
            current_amount += sell_amount
            btc_held = 0
            in_position = False
            transactions.append({
                    'timestamp': timestamp,
                    'type': 'sell',
                    'price': price,
                    'price_last_signal': price_last_signal, 
                    'amount_usdt': sell_amount,
                    'btc_held': btc_held,
                    'current_amount': current_amount
                })
        price_last_signal = price
    
    return pd.DataFrame(transactions)

def simulate_transactions_margin(signals_df, trade_amount=500, leverage=10, stop_loss_percent=0.1):
    in_position = False
    account_balance = 1000  # Initial account balance
    btc_held = 0
    transactions = []
    liquidated = False
    buy_price = 0  # Price at which BTC was bought

    for index, signal in signals_df.iterrows():
        if liquidated:
            break

        price = signal['price']
        timestamp = signal['timestamp']
        liquidation_price = buy_price * (1 - (1 / leverage))  # Simplified liquidation price
        stop_loss_price = buy_price * (1 - stop_loss_percent)  # Stop loss threshold

        if signal['signal'] == 'buy' and not in_position:
            if account_balance >= trade_amount:
                btc_bought = (trade_amount * leverage) / price
                btc_held += btc_bought
                account_balance -= trade_amount
                buy_price = price  # Update buy price
                in_position = True
                transactions.append({
                    'timestamp': timestamp, 'type': 'buy', 'price': price, 
                    'btc_held': btc_held, 'account_balance': account_balance,
                    'liquidation_price': liquidation_price
                })
        
        elif signal['signal'] == 'sell' and btc_held > 0:
            if price <= liquidation_price:
                print("LIQUIDATED!")
                # Liquidation occurs
                account_balance = 0
                btc_held = 0
                in_position = False
                liquidated = True
                transactions.append({
                    'timestamp': timestamp, 'type': 'liquidation', 'price': price, 
                    'btc_held': 0, 'account_balance': 0,
                    'liquidation_price': liquidation_price
                })
            else:
                # Regular sell
                position_value = btc_held * price  # Total value of BTC held at current price
                profit = position_value - (trade_amount * leverage - trade_amount)  # Profit from the leveraged trade
                account_balance += profit  # Return the initial investment plus profit
                btc_held = 0
                in_position = False
                transactions.append({
                    'timestamp': timestamp, 'type': 'sell', 'price': price, 
                    'btc_held': btc_held, 'account_balance': account_balance,
                    'liquidation_price': liquidation_price
                })

    return pd.DataFrame(transactions)



def apply_trading_strategy(data):
    # Apply your trading strategy to the historical data
    # and return buy/sell signals
    # For example, using Supertrend:
    df = apply_combined_strategy(data)
    # print(df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'in_uptrend']])
    df = check_historical_buy_sell_signals(df)
    return df

def main():
    historical_data = fetch_data()
    signals_df = apply_trading_strategy(historical_data)
    print(signals_df)
    results_df = simulate_transactions_margin(signals_df)
    print(results_df)

if __name__ == "__main__":
    main()