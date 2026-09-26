import os
import time
import ccxt
from flask import Flask
from threading import Thread

# 1. Flask App (Render Web Service Health Check)
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Auto-Trader Bot Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Main Trading Logic
def start_bot():
    time.sleep(3)
    print("\n==========================================")
    print("⚡ DELTA TESTNET BOT INITIALIZING ⚡")
    print("==========================================\n")

    API_KEY = os.environ.get('DELTA_API_KEY')
    API_SECRET = os.environ.get('DELTA_API_SECRET')

    if not API_KEY or not API_SECRET:
        print("❌ CRITICAL ERROR: Environment Variables DELTA_API_KEY / DELTA_API_SECRET missing!")
        return

    # Direct CCXT Delta Setup
    exchange = ccxt.delta({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
    })
    
    # Delta Testnet Enable
    exchange.set_sandbox_mode(True)

    # UI Dashboard wala Exact Symbol: BTCUSD
    SYMBOL = 'BTCUSD'
    LOT_SIZE = 10  # 10 Lots (0.01 BTC)

    # Set Leverage
    try:
        exchange.set_leverage(25, SYMBOL)
        print("✅ Leverage set to 25x successfully.")
    except Exception as e:
        print(f"⚠️ Leverage Status: {e}")

    print("\n🚀 Executing Trading Loop (Every 5 Minutes)...")

    while True:
        try:
            print("\n🛒 Sending Market Buy Order...")
            order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
            print(f"🎉 SUCCESS! Order Placed. Order ID: {order.get('id', 'N/A')}")
        except Exception as e:
            # Agar BTCUSD fail ho toh fallback symbol BTC/USD:BTC try karein
            try:
                order = exchange.create_market_buy_order('BTC/USD:BTC', LOT_SIZE)
                print(f"🎉 SUCCESS! Order Placed (Fallback Symbol). Order ID: {order.get('id', 'N/A')}")
            except Exception as err:
                print(f"❌ TRADE ERROR: {err}")

        # 5 minutes wait
        time.sleep(300)

if __name__ == '__main__':
    # Flask Server Background Thread
    server_thread = Thread(target=run_web_server, daemon=True)
    server_thread.start()

    # Main Bot Thread
    start_bot()
