from datetime import datetime
import json


def log(message, extra=None):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
    }

    if extra:
        entry.update(extra)

    with open("logs.jsonl", "a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
        file.flush()


def log_crypto_snapshot(asset, price, amount=None):
    if price is None:
        return

    log(
        "Crypto data fetched",
        {
            "asset": {
                "name": asset.get("name"),
                "ticker": asset.get("ticker"),
                "market": asset.get("market"),
            },
            "price_usdt": round(float(price), 2),
            "balance": amount,
        },
    )