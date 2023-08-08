
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_xrp_price():
    url = os.getenv("MESSARI_XRP_ASSET_URL")
    response = requests.get(url=str(url))
    if response.status_code == 200:
        price = response.json()['data']['market_data']['price_usd']
        return {"status": True, "price": price}
    return {"status": False}
  
    

    