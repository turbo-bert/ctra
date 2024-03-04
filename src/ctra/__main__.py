import requests
import json
import time
import urllib.parse
import hashlib
import hmac
import base64
import os

import rich
from rich.pretty import pprint as PP
from rich.console import Console
from rich.table import Table
CONSOLE = Console()

api_url = "https://api.kraken.com"

api_sec = open(os.getenv("KRAKEN_API_SEC"),'r').read().strip().split("\n")[0]
api_key = open(os.getenv("KRAKEN_API_KEY"),'r').read().strip().split("\n")[0]


def gks(urlpath, data, secret):
    """Get Kraken Signatur."""
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce'])+postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def get_zeur_balance():
    return float(kraken_POST_auth(uri_path="/0/private/Balance", data={}, api_key=api_key, api_sec=api_sec).json()["result"]["ZEUR"])


def order_xeth(eth_float, validate=False):
    res = kraken_POST_auth(uri_path="/0/private/AddOrder", data={
        "ordertype": "market",
        "type": "buy",
        "volume": str(eth_float),
        "pair": "XETHZEUR",
        "validate": validate
    }, api_key=api_key, api_sec=api_sec).json()
    return res


def sell_xeth(eth_float, validate=False):
    res = kraken_POST_auth(uri_path="/0/private/AddOrder", data={
        "ordertype": "market",
        "type": "sell",
        "volume": str(eth_float),
        "pair": "XETHZEUR",
        "validate": validate
    }, api_key=api_key, api_sec=api_sec).json()
    return res


def get_xeth_balance():
    return float(kraken_POST_auth(uri_path="/0/private/Balance", data={}, api_key=api_key, api_sec=api_sec).json()["result"]["XETH"])


def get_balance():
    return kraken_POST_auth(uri_path="/0/private/Balance", data={}, api_key=api_key, api_sec=api_sec).json()


def get_xeth_price():
    x = requests.get("https://api.kraken.com/0/public/Ticker?pair=XETHZEUR")
    eur = float(x.json()["result"]["XETHZEUR"]["a"][0])
    return(eur)


def kraken_POST_auth(uri_path, data, api_key, api_sec):
    anonce = str(int(1000*time.time()))
    data["nonce"] = anonce
    headers={}
    headers["API-Key"] = api_key
    headers["API-Sign"] = gks(uri_path, data, api_sec)
    req = requests.post((api_url+uri_path), headers=headers, data=data)
    return req


def eur2eth(eur_float):
    xeth_price = get_xeth_price()
    print("price=%f" % xeth_price)
    return int(float(eur_float) / xeth_price * 1000000)/1000000.0


#res1 = get_xeth_price()
#print(json.dumps(res1, indent=4))
###print(eur2eth(5))
###print(get_balance())
# res2 = get_xeth_balance()
# print(json.dumps(res2, indent=4))
# print(res1*res2)

# res = order_xeth(0.004, validate=True)
# print(json.dumps(res, indent=4))


# x = requests.get("https://api.kraken.com/0/public/Ticker?pair=XETHZEUR")
# eur = float(x.json()["result"]["XETHZEUR"]["a"][0])
# print(eur)

# if eur < 3000:
#     print("buy!")
# elif eur > 3700:
#     print("sell!")
# else:
#     print("nothing!")

##PP(get_balance())
PP(get_xeth_price())
#PP(eur2eth(20))
##PP(order_xeth(0.011895))
#PP(sell_xeth(0.011880))
