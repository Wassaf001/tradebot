import requests

def get_usd_price(symbol="BTC-USDT"):
    """
    Fetch the latest price for the given symbol from OKX REST API.
    """
    url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
    try:
        resp = requests.get(url, timeout=3)
        data = resp.json()
        price = float(data['data'][0]['last'])
        return price
    except Exception:
        return None

def get_fee_rate(fee_tier='default', taker=True):
    """
    Return fee rate based on tier (from OKX docs).
    """
    if fee_tier == 'VIP':
        return 0.0005 if taker else 0.0002
    return 0.0008 if taker else 0.0006