import ccxt

exchange = ccxt.delta({
    'apiKey': 'YOUR_DELTA_API_KEY',
    'secret': 'YOUR_DELTA_API_SECRET',
    'urls': {
        'api': {
            'public': 'https://api.testnet.delta.exchange',
            'private': 'https://api.testnet.delta.exchange',
        }
    }
})

# Market Products Fetch karke exact BTC Symbol check karein
markets = exchange.load_markets()
for symbol, market in markets.items():
    if 'BTC' in symbol and market.get('active'):
        print(f"Symbol: {symbol} | Product ID: {market.get('id')}")
