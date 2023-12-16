from db_utils import fetch_data

def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])
    return data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

def atr(data, period):
    data['tr'] = tr(data)
    return data['tr'].rolling(period).mean()

def supertrend(df, period=7, atr_multiplier=3):
    # Calculate HL2, ATR and set initial upperband, lowerband, in_uptrend
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1
        if df.iloc[current]['close'] > df.iloc[previous]['upperband']:
            df.at[current, 'in_uptrend'] = True
        elif df.iloc[current]['close'] < df.iloc[previous]['lowerband']:
            df.at[current, 'in_uptrend'] = False
        else:
            df.at[current, 'in_uptrend'] = df.at[previous, 'in_uptrend']
            if df.at[current, 'in_uptrend']:
                df.at[current, 'lowerband'] = max(df.iloc[current]['lowerband'], df.iloc[previous]['lowerband'])
            else:
                df.at[current, 'upperband'] = min(df.iloc[current]['upperband'], df.iloc[previous]['upperband'])
    return df

in_position = False

def check_buy_sell_signals(df):
    global in_position

    print("checking for buy and sell signals")
    print(df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'in_uptrend']].tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("changed to uptrend, buy")
        # if not in_position:
        #     order = exchange.create_market_buy_order('BTC/USDT', 0.05)
        #     print(order)
        #     in_position = True
        # else:
        #     print("already in position, nothing to do")
    
    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        print("changed to downtrend, sell")
        # if in_position:
        #     order = exchange.create_market_sell_order('BTC/USDT', 0.05)
        #     print(order)
        #     in_position = False
        # else:
        #     print("You aren't in position, nothing to sell")

def supertrend_strategy():
    df = fetch_data()
    df = supertrend(df)
    check_buy_sell_signals(df)

if __name__ == '__main__':
    supertrend_strategy()
