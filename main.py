import time
import ccxt
from flask import Flask
from threading import Thread

# Flask App (Render Service Ko Active Rakhne Ke Liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Fast Auto-Trader Active!"

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
except Exception as e:
    print(f"Leverage Status: {e}")

def run_fast_bot():
    print("⚡ Fast Trading Bot Started...")
    while True:
        try:
            print("\nExecuting Instant Buy Order...")
            order = exchange.create_market_buy_order(SYMBOL, LOT_SIZE)
            print(f"Order Successful! Order ID: {order['id']}")
        except Exception as e:
            print(f"Order Error: {e}")
        
        # Har 5 minute (300 seconds) me order chalega
        time.sleep(300)

# Background Thread
Thread(target=run_fast_bot).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
