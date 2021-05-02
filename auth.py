import hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import json

class CoinbaseExchangeAuth(AuthBase):
    def __init__(self):
        self.config = self.configuration()
        self.api_key = self.config["KEY"]
        self.secret_key = self.config["SECRET"]
        self.passphrase = self.config["PASSPHRASE"]

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
    
    def configuration(self):
        with open('config.json') as configFile:
            return json.load(configFile)