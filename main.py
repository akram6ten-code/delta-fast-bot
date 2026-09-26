import time
import ccxt
from flask import Flask
from threading import Thread

# Flask Server (Render Web Service Ko Active Rakhne Ke Liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Fast Auto-Trader Active!"

def run_web_server():
    app.run(host='0.0.0.0', port=10000)

# Background Thread Mein Web Server Start Karein
Thread(target=run_web_server, daemon=True).start()

# Delta Testnet Setup
exchange = ccxt.delta({
    'apiKey': 'YOUR_DELTA_DEMO_API_KEY',
    'secret': 'YOUR_DELTA_DEMO_API_SECRET',
    'enableRateLimit': True,
})
exchange.set_sandbox_mode(True)  # Demo Account

SYMBOL = 'BTC/USD'
LEVERAGE = 25
LOT_SIZE = 10  # 10 Lots

# Set Leverage
try:
    exchange.set_leverage(LEVERAGE, SYMBOL)
    print(f"Leverage set to {LEVERAGE}x successfully.")
except Exception as e:
    print(f"Leverage Status: {e}")

# Main Fast Trading Loop
print("⚡ Fast Trading Bot Started...")
while True:
    try:
        print("\nExecuting Instant Buy Order...")
        order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
        print(f"Order Successful! Order ID: {order['id']}")
    except Exception as e:
        print(f"Order Error: {e}")
    
    # Har 5 minute (300 seconds) me loop chalega
    time.sleep(300)
