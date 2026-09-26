import os
import time
import ccxt
from flask import Flask
from threading import Thread

# Render Uptime Ke Liye Flask Server
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta Symbol Checker Active!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Background Thread Mein Web Server Start Karein
Thread(target=run_web_server, daemon=True).start()

# Main Test Function
def check_delta_symbols():
    time.sleep(3)
    print("\n==========================================")
    print("🔍 FETCHING DELTA TESTNET MARKETS...")
    print("==========================================\n")
    
    API_KEY = os.environ.get('DELTA_API_KEY')
    API_SECRET = os.environ.get('DELTA_API_SECRET')

    try:
        exchange = ccxt.delta({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'urls': {
                'api': {
                    'public': 'https://api.testnet.delta.exchange',
                    'private': 'https://api.testnet.delta.exchange',
                }
            }
        })

        markets = exchange.load_markets()
        print("✅ Markets fetched successfully! Active BTC Symbols:\n")
        
        for symbol, market in markets.items():
            if 'BTC' in symbol and market.get('active'):
                print(f"Symbol: {symbol} | Product ID: {market.get('id')} | Type: {market.get('type')}")
                
    except Exception as e:
        print(f"❌ Error Fetching Markets: {e}")

if __name__ == '__main__':
    check_delta_symbols()
