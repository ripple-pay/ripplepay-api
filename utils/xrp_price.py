
import requests
import os
from dotenv import load_dotenv
import http.client

conn = http.client.HTTPSConnection("anyapi.io")
load_dotenv()


def get_xrp_price():
    url = os.getenv("MESSARI_XRP_ASSET_URL")
    response = requests.get(url=str(url))
    if response.status_code == 200:
        price = response.json()['data']['market_data']['price_usd']
        return {"status": True, "price": price}
    return {"status": False}


def get_usd_eur(usd_amount):
    currency_freak= os.getenv("CURRENCY_FREAK_API_KEY")
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={currency_freak}"
    res = requests.get(url=url)
    body = res.json()
    eur = float(usd_amount) * float(body["rates"]["EUR"])
    jpy = float(usd_amount)* float(body["rates"]["JPY"])
    return {"EUR":eur, "JPY": jpy}