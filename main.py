import time
import json
from data_fetcher import fetch_crypto, fetch_commodity, fetch_btcturk_balances
from ui_manager import UIManager

def main():
    ui = UIManager()
    
    # assets.json dosyasından varlık listesini oku
    try:
        with open('assets.json', 'r') as f:
            assets = json.load(f)
    except FileNotFoundError:
        print("Hata: assets.json dosyası bulunamadı!")
        return
    except json.JSONDecodeError:
        print("Hata: assets.json dosyası geçersiz JSON formatında!")
        return
    
    # Takip edilecek varlık listesi
    # symbol: BtcTurk cüzdanındaki isimle eşleşmeli

    try:
        prev_prices = {}
        while True:
            # 1. BtcTurk cüzdan verilerini çek
            my_wallet = fetch_btcturk_balances()
            
            processed_data = []
            
            # 2. Her bir varlık için fiyat, değişim ve bakiye hesapla
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

                # Fiyat değişimini hesapla
                previous_price = prev_prices.get(asset['ticker'])
                if price is not None and previous_price:
                    change_pct = ((price - previous_price) / previous_price) * 100
                else:
                    change_pct = None

                # Mevcut fiyatı kaydet
                if price is not None:
                    prev_prices[asset['ticker']] = price
                
                # Veriyi tabloya uygun formata getir
                processed_data.append({
                    "name": asset['name'],
                    "price": price,
                    "market": asset['market'],
                    "balance": amount,
                    "total_value": price * amount if price and amount else 0,
                    "change_pct": change_pct
                })
            
            # 3. UI üzerinden dashboard'u ekrana bas
            ui.render_dashboard(processed_data)
            
            # 60 saniye bekle ve döngüyü tekrarla
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n[!] Borsa asistanı kapatıldı. Kendine iyi bak kanka!")

if __name__ == "__main__":
    main()