import os
import time
import ccxt
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Auto-Trader Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def start_bot():
    time.sleep(2)
    print("\n==========================================", flush=True)
    print("⚡ DELTA BITCOIN BOT INITIALIZING ⚡", flush=True)
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

    try:
        exchange.set_leverage(25, SYMBOL)
        print("✅ Leverage set to 25x successfully.", flush=True)
    except Exception as e:
        print(f"⚠️ Leverage Status: {e}", flush=True)

    print("\n🚀 Starting Order Execution Loop (Every 5 minutes)...", flush=True)

    while True:
        try:
            print("\n🛒 Sending Market Buy Order...", flush=True)
            order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
            print(f"🎉 SUCCESS! Order Placed. Order ID: {order.get('id', 'N/A')}", flush=True)
        except Exception as e:
            print(f"❌ TRADE ERROR: {e}", flush=True)

        time.sleep(300)

if __name__ == '__main__':
    # Start web server thread
    server_thread = Thread(target=run_web_server, daemon=True)
    server_thread.start()

    # Start main trading process
    start_bot()
