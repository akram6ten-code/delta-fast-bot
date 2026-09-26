import os
import time
import ccxt
import pandas as pd
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Delta SuperTrend Auto-Trader Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


# --- SUPERTREND CALCULATION FUNCTION ---
def calculate_supertrend(df, period=10, multiplier=3):
    high = df['high']
    low = df['low']
    close = df['close']

    # Average True Range (ATR)
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()

    # Basic Upper & Lower Bands
    hl2 = (high + low) / 2
    basic_upper = hl2 + (multiplier * atr)
    basic_lower = hl2 - (multiplier * atr)

    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()

    for i in range(1, len(df)):
        if basic_upper.iloc[i] < final_upper.iloc[i-1] or close.iloc[i-1] > final_upper.iloc[i-1]:
            final_upper.iloc[i] = basic_upper.iloc[i]
        else:
            final_upper.iloc[i] = final_upper.iloc[i-1]

        if basic_lower.iloc[i] > final_lower.iloc[i-1] or close.iloc[i-1] < final_lower.iloc[i-1]:
            final_lower.iloc[i] = basic_lower.iloc[i]
        else:
            final_lower.iloc[i] = final_lower.iloc[i-1]

    # SuperTrend Direction
    supertrend = pd.Series(index=df.index, dtype='float64')
    direction = pd.Series(index=df.index, dtype='int64')

    for i in range(1, len(df)):
        if close.iloc[i] > final_upper.iloc[i-1]:
            direction.iloc[i] = 1  # 1 = Bullish (Green)
        elif close.iloc[i] < final_lower.iloc[i-1]:
            direction.iloc[i] = -1  # -1 = Bearish (Red)
        else:
            direction.iloc[i] = direction.iloc[i-1] if i > 0 else 1
            
        supertrend.iloc[i] = final_lower.iloc[i] if direction.iloc[i] == 1 else final_upper.iloc[i]

    df['supertrend'] = supertrend
    df['trend'] = direction
    return df


# --- TRADING BOT MAIN LOGIC ---
def start_bot():
    time.sleep(3)
    print("\n==========================================", flush=True)
    print("⚡ DELTA BITCOIN SUPERTREND BOT INITIALIZING ⚡", flush=True)
    print("==========================================\n", flush=True)

    API_KEY = os.environ.get('DELTA_API_KEY')
    API_SECRET = os.environ.get('DELTA_API_SECRET')

    if not API_KEY or not API_SECRET:
        print("❌ ERROR: API Keys missing in Render Environment Variables!", flush=True)
        return

    exchange = ccxt.delta({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'urls': {
            'api': {
                'public': 'https://cdn-ind.testnet.deltaex.org',
                'private': 'https://cdn-ind.testnet.deltaex.org',
            }
        }
    })

    SYMBOL = 'BTCUSD'
    LOT_SIZE = 10
    TIMEFRAME = '15m'  # 15-minute candles

    # Leverage set to 25x
    try:
        exchange.set_leverage(25, SYMBOL)
        print("✅ Leverage set to 25x successfully.", flush=True)
    except Exception as e:
        print(f"⚠️ Leverage Status: {e}", flush=True)

    current_position = None  # Tracks 'BUY', 'SELL', or None

    print("\n🚀 Starting SuperTrend Order Loop...", flush=True)

    while True:
        try:
            # 1. Fetch OHLCV Candle Data (15-Min)
            ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=50)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # 2. Calculate SuperTrend (10, 3)
            df = calculate_supertrend(df, period=10, multiplier=3)
            latest_trend = df['trend'].iloc[-1]
            last_close = df['close'].iloc[-1]

            trend_status = "GREEN (BULLISH)" if latest_trend == 1 else "RED (BEARISH)"
            print(f"\n📊 [15m Candle] Price: {last_close} | SuperTrend: {trend_status}", flush=True)

            # 3. Execution Logic
            # SCENARIO A: SuperTrend turns GREEN (1)
            if latest_trend == 1:
                if current_position == 'SELL':
                    print("🔄 Exit Trigger: Closing Previous SELL Position...", flush=True)
                    exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
                    print("✅ Closed SELL position.", flush=True)
                    current_position = None

                if current_position != 'BUY':
                    print("🛒 BUY Signal (Green): Placing Market Buy Order (10 Lots)...", flush=True)
                    order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
                    current_position = 'BUY'
                    print(f"🎉 SUCCESS! BUY Order Placed. Order ID: {order.get('id', 'N/A')}", flush=True)
                else:
                    print("⏳ Holding BUY Position (No Action Needed).", flush=True)

            # SCENARIO B: SuperTrend turns RED (-1)
            elif latest_trend == -1:
                if current_position == 'BUY':
                    print("🔄 Exit Trigger: Closing Previous BUY Position...", flush=True)
                    exchange.create_market_sell_order(SYMBOL, LOT_SIZE)
                    print("✅ Closed BUY position.", flush=True)
                    current_position = None

                if current_position != 'SELL':
                    print("🔻 SELL Signal (Red): Placing Market Sell Order (10 Lots)...", flush=True)
                    order = exchange.create_market_sell_order(SYMBOL, LOT_SIZE)
                    current_position = 'SELL'
                    print(f"🎉 SUCCESS! SELL Order Placed. Order ID: {order.get('id', 'N/A')}", flush=True)
                else:
                    print("⏳ Holding SELL Position (No Action Needed).", flush=True)

        except Exception as e:
            print(f"❌ TRADE ERROR: {e}", flush=True)

        # Har 1 minute baad candle update check karega
        time.sleep(60)


if __name__ == '__main__':
    server_thread = Thread(target=run_web_server, daemon=True)
    server_thread.start()

    start_bot()
