import os
import time
import ccxt
from flask import Flask
from threading import Thread

# 1. Flask App (Render Uptime Ke Liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Fast Auto-Trader Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Main Trading Function
def trading_bot():
    print("⚡ Trading Bot Process Initializing...")
    
    # Delta API Credentials
    API_KEY = os.environ.get('DELTA_API_KEY')
    API_SECRET = os.environ.get('DELTA_API_SECRET')

    if not API_KEY or not API_SECRET:
        print("❌ Error: API Keys Render Environment Variables mein nahi mili!")
        return

    exchange = ccxt.delta({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
    })
    
    # Demo/Testnet Enable
    exchange.set_sandbox_mode(True)

    SYMBOL = 'BTC/USD'
    LEVERAGE = 25
    LOT_SIZE = 10

    # Set Leverage
    try:
        exchange.set_leverage(LEVERAGE, SYMBOL)
        print(f"✅ Leverage {LEVERAGE}x set successfully.")
    except Exception as e:
        print(f"⚠️ Leverage Status: {e}")

    print("🚀 Loop Started: Executing trade every 5 minutes...")
    
    while True:
        try:
            print("\n🛒 Executing Instant Buy Order...")
            order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
            print(f"🎉 Order Successful! Order ID: {order['id']}")
        except Exception as e:
            print(f"❌ Order Error: {e}")
        
        # 5 minute wait
        time.sleep(300)

if __name__ == '__main__':
    # Trading Bot ko background thread mein start karein
    bot_thread = Thread(target=trading_bot, daemon=True)
    bot_thread.start()
    
    # Web server ko main thread par chalayein
    run_web_server()
