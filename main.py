import os
import time
import ccxt
from flask import Flask
from threading import Thread

# Flask Server (Render Web Service ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Fast Auto-Trader Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web_server, daemon=True).start()

# Render Environment Variables se Keys fetch kar raha hai
API_KEY = os.environ.get('DELTA_API_KEY')
API_SECRET = os.environ.get('DELTA_API_SECRET')

exchange = ccxt.delta({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
})
exchange.set_sandbox_mode(True)  # Demo Account

SYMBOL = 'BTC/USD'
LEVERAGE = 25
LOT_SIZE = 10

try:
    exchange.set_leverage(LEVERAGE, SYMBOL)
    print(f"Leverage set to {LEVERAGE}x successfully.")
except Exception as e:
    print(f"Leverage Status: {e}")

print("⚡ Fast Trading Bot Started...")
while True:
    try:
        print("\nExecuting Instant Buy Order...")
        order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
        print(f"Order Successful! Order ID: {order['id']}")
    except Exception as e:
        print(f"Order Error: {e}")
    
    time.sleep(300)
