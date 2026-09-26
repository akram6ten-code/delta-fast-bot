import os
import time
import ccxt
from flask import Flask
from threading import Thread

# 1. Flask App Setup (Render Uptime Check Ke Liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Fast Auto-Trader Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    # Werkzeug logger quiet kar rahe hain taaki logs me sirf trades dikhein
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# 2. Main Trading Bot Function
def trading_bot():
    # Render server boot hone ka 5 second wait karein
    time.sleep(5)
    print("\n==========================================")
    print("⚡ FAST TRADING BOT INITIALIZED ⚡")
    print("==========================================\n")
    
    API_KEY = os.environ.get('DELTA_API_KEY')
    API_SECRET = os.environ.get('DELTA_API_SECRET')

    if not API_KEY or not API_SECRET:
        print("❌ CRITICAL ERROR: Delta API Keys Render Environment Variables mein nahi mili!")
        print("Kripya Render Dashboard -> Environment mein DELTA_API_KEY aur DELTA_API_SECRET set karein.\n")
        return

    try:
        exchange = ccxt.delta({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'enableRateLimit': True,
        })
        exchange.set_sandbox_mode(True)  # Demo/Testnet Account Mode
        print("✅ Delta Exchange Connected in Demo Mode.")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    SYMBOL = 'BTC/USD'
    LEVERAGE = 25
    LOT_SIZE = 10

    # Set Leverage
    try:
        exchange.set_leverage(LEVERAGE, SYMBOL)
        print(f"✅ Leverage successfully set to {LEVERAGE}x.")
    except Exception as e:
        print(f"⚠️ Leverage Notice: {e}")

    print("\n🚀 Starting Fast Trading Loop (Execution every 300 seconds)...")
    
    while True:
        try:
            print("\n🛒 Executing Instant Buy Order...")
            order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
            print(f"🎉 SUCCESS! Market Order Placed. Order ID: {order.get('id', 'N/A')}")
        except Exception as e:
            print(f"❌ TRADE FAILED! Error Details: {e}")
        
        # 5 Minute Interval (300 seconds)
        time.sleep(300)

if __name__ == '__main__':
    # Web server ko background thread me start karein
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Trading bot ko main execution thread par chalayein
    trading_bot()
