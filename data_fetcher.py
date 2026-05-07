import os
import ccxt
import yfinance as yf
from dotenv import load_dotenv

# .env dosyasındaki anahtarları sisteme yükler
load_dotenv()

def fetch_crypto(symbol):
    try:
        exchange = ccxt.binance()
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except:
        return None

def fetch_commodity(ticker_symbol):
    try:
        asset = yf.Ticker(ticker_symbol)
        return asset.fast_info['last_price']
    except:
        return None

def fetch_btcturk_balances():
    """BtcTurk cüzdanındaki bakiyeleri çeker."""
    try:
        exchange = ccxt.btcturk({
            'apiKey': os.getenv('BTCTURK_API_KEY'),
            'secret': os.getenv('BTCTURK_API_SECRET'),
        })
        balance = exchange.fetch_balance()
        
        # DOĞRU YAPI: 'total' içindeki değerler zaten miktardır (float).
        # Onları doğrudan coin ismiyle eşleştiriyoruz.
        return {coin: amount for coin, amount in balance['total'].items() if amount > 0}
    
    except Exception as e:
        # Hata devam ederse burası bize daha net bilgi verir
        print(f"BtcTurk Bağlantı Hatası: {e}")
        return {}