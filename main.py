import os
import time
import ccxt
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Perpetual Bot Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def start_bot():
    time.sleep(2)
    print("\n==========================================")
    print("⚡ DELTA BITCOIN PERPETUAL BOT INITIALIZING ⚡")
    print("==========================================\n")

    API_KEY = os.environ.get('DELTA_API_KEY')
    API_SECRET = os.environ.get('DELTA_API_SECRET')

    if not API_KEY or not API_SECRET:
        print("❌ ERROR: API Keys missing in Render Environment Variables!")
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

    SYMBOL = 'BTC/USD:BTC'
    LOT_SIZE = 10

    try:
        exchange.set_leverage(25, SYMBOL)
        print("✅ Leverage set to 25x successfully.")
    except Exception as e:
        print(f"⚠️ Leverage Status: {e}")

    print("\n🚀 Starting Order Execution Loop...")

    while True:
        try:
            print("\n🛒 Sending Market Buy Order...")
            order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
            print(f"🎉 SUCCESS! Order Placed. Order ID: {order.get('id', 'N/A')}")
        except Exception as e:
            print(f"❌ TRADE ERROR: {e}")

        time.sleep(300)

if __name__ == '__main__':
    # Web server ko daemon thread me chalayein
    server_thread = Thread(target=run_web_server, daemon=True)
    server_thread.start()

    # Bot logic execute karein
    start_bot()
