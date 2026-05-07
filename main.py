import time
from data_fetcher import fetch_crypto, fetch_commodity, fetch_btcturk_balances
from ui_manager import UIManager

def main():
    ui = UIManager()
    
    # Takip edilecek varlık listesi
    # symbol: BtcTurk cüzdanındaki isimle eşleşmeli
    assets = [
        {"name": "Bitcoin (BTC)", "ticker": "BTC/USDT", "type": "crypto", "market": "Binance", "symbol": "BTC"},
        {"name": "Ethereum (ETH)", "ticker": "ETH/USDT", "type": "crypto", "market": "Binance", "symbol": "ETH"},
        {"name": "Solana (SOL)", "ticker": "SOL/USDT", "type": "crypto", "market": "Binance", "symbol": "SOL"},
        {"name": "Tether (USDT)", "ticker": "USDT/USDC", "type": "crypto", "market": "Binance", "symbol": "USDT"},
        {"name": "Gold (XAU)", "ticker": "GC=F", "type": "commodity", "market": "COMEX", "symbol": "XAU"}
    ]

    try:
        while True:
            # 1. BtcTurk cüzdan verilerini çek
            my_wallet = fetch_btcturk_balances()
            
            processed_data = []
            
            # 2. Her bir varlık için fiyat ve bakiye hesapla
            for asset in assets:
                # USDT sabitlemesi (1 USDT her zaman 1 dolardır)
                if asset['symbol'] == 'USDT':
                    price = 1.0
                elif asset['type'] == 'crypto':
                    price = fetch_crypto(asset['ticker'])
                else:
                    price = fetch_commodity(asset['ticker'])
                
                # Cüzdan eşleştirmesi (Miktar)
                amount = my_wallet.get(asset['symbol'], 0)
                
                # Veriyi tabloya uygun formata getir
                processed_data.append({
                    "name": asset['name'],
                    "price": price,
                    "market": asset['market'],
                    "balance": amount,
                    "total_value": price * amount if price and amount else 0
                })
            
            # 3. UI üzerinden dashboard'u ekrana bas
            ui.render_dashboard(processed_data)
            
            # 60 saniye bekle ve döngüyü tekrarla
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n[!] Borsa asistanı kapatıldı. Kendine iyi bak kanka!")

if __name__ == "__main__":
    main()