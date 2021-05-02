import json
import requests
import math
from auth import CoinbaseExchangeAuth
from decimal import Decimal, ROUND_HALF_EVEN

class ServiceHandler():
    def __init__(self):
        self.auth = CoinbaseExchangeAuth( )
        self.config = self.configuration()
        self.serviceUrl = self.config["SERVICEURL"]

    def configuration(self):
        with open('config.json') as configFile:
            return json.load(configFile)

    def getCurrency(self, id):
        request = requests.get(self.serviceUrl + 'currencies/' + id , auth=self.auth)
        if request.status_code == 200:
            return request.json()

    def getWallet(self):
        request = requests.get(self.serviceUrl + 'accounts/all', auth=self.auth)
        if request.status_code == 200:
            for account in request.json():
                if account["currency"] == "BTC":
                    btc_available = round( float( account["available"] ) )
                    if btc_available > 0:
                        wallet = {"currency":account["currency"], "available":btc_available}

                elif account["currency"] == "USDC" and float( account["available"] ) > 0:
                    wallet = {"currency": account["currency"], "available": float( account["available"] )}
                    return wallet

    def getBTCValue(self):
        request = requests.get(self.serviceUrl + 'products/BTC-EUR/stats', auth=self.auth)
        if request.status_code == 200:
            return request.json()

    def setOrder(self, side, product_id, available):
        order = {
            "funds": available,
            "side": side,
            "product_id": product_id,
            "type": "market"
        }
        r = requests.post(self.serviceUrl + "orders", json=order, auth=self.auth)
        if r.status_code == 200:
            print("Order:", r["id"], r["side"], r["status"])
        else:
            print("Request error:", available, side, product_id)
        return r