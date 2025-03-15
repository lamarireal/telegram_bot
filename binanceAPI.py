from binance.client import Client
import requests
import os
from dotenv import load_dotenv

def get_client_binance():
    API_KEY = os.getenv("BINANCE_CLIENT_KEY")
    API_SECRET = os.getenv("BINANCE_SECRET_KEY")
    return Client(API_KEY, API_SECRET)

def get_balance(client):
    balance = client.get_asset_balance(asset='USDT')
    return balance

def get_price(client, symbol: str):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol.upper())
        return float(ticker['price'])
    except Exception as e:
        return f"Error: {e}"
    
def get_important_coin(client):

    symbol = ["BTCUSDT", "WLDUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]

    results = {}

    for s in symbol:
        try: 
            ticker = client.get_symbol_ticker(symbol=s.upper())
            results[s[:3]] = ticker['price']
        except Exception as e:
            return f"Error: {e}"
    return results