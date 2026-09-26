import os
import time
import ccxt
from flask import Flask
from threading import Thread

# 1. Flask Health Check App
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Auto-Trader is Running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Main Trading Function
def start_trading():
    time.sleep(5)
    print("\n==========================================")
    print("⚡ TRADING BOT INITIALIZING ⚡")
    print("==========================================\n")

    API_KEY = os.environ.get('DELTA_API_KEY')
    API_SECRET = os.environ.get('DELTA_API_SECRET')

    if not API_KEY or not API_SECRET:
        print("❌ ERROR: API Keys missing in Render Environment Variables!")
        return

    # CCXT Native Testnet Config (Bina custom URL ke)
    exchange = ccxt.delta({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
    })
    exchange.set_sandbox_mode(True)  # Native Demo/Testnet URL load karega

    SYMBOL = 'BTC/USD'
    LOT_SIZE = 10

    # Leverage setup
    try:
        exchange.set_leverage(25, SYMBOL)
        print("✅ Leverage set to 25x.")
    except Exception as e:
        print(f"⚠️ Leverage info: {e}")

    print("\n🚀 Starting Trading Loop...")
    while True:
        try:
            print("\n🛒 Executing Market Buy Order...")
            order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
            print(f"🎉 SUCCESS! Order Placed. Order ID: {order.get('id', 'N/A')}")
        except Exception as e:
            print(f"❌ TRADE ERROR: {e}")

        # Har 5 minute (300 seconds)
        time.sleep(300)

if __name__ == '__main__':
    # Flask app ko background thread mein start karo
    server_thread = Thread(target=run_web_server, daemon=True)
    server_thread.start()

    # Trading loop run karo
    start_trading()
