import json
import requests
import time
import smtplib
import constant
import itertools

from datetime import datetime
from auth import CoinbaseExchangeAuth
from serviceHandler import ServiceHandler
from MailHandler import MailHandler
from decimal import Decimal, ROUND_HALF_EVEN

class CryptoBot:
    def __init__(self):
        self.mailHandler = MailHandler()
        self.time = constant.FULL_TIME # Refresh time
        self.positive_tranding = False
        self.control_value = float(0) # Check value
        self.wallet_value = float(0) # bought / sold value
        self.actual_value = float(0) # Last BTC value
        self.maxBTCValue = float(0) # Max BTC Value 

    def update(self):
        serviceHandler = ServiceHandler( )
        wallet = serviceHandler.getWallet( )
        btc_value = serviceHandler.getBTCValue( )
        self.actual_value = float( btc_value["last"] )

        if wallet["currency"] == "BTC":
            if self.actual_value <= self.control_value:
                resp = self.sell( )
                self.control_value = self.actual_value
                self.mailHandler.addText(resp)

            elif self.maxBTCValue < self.actual_value:
                self.maxBTCValue = self.actual_value
                self.control_value += ( self.maxBTCValue - self.actual_value ) / 3
                self.positive_tranding = True
                          
        else:
            if self.actual_value <= self.control_value:
                self.control_value = self.actual_value
            
            else:
                counter = 0
                for _ in itertools.repeat(None, 3):
                    time.sleep(constant.PING_TIME)

                    ping_value = serviceHandler.getWallet( )
                    if float( ping_value["last"] ) > self.actual_value:
                        counter += 1
                        if counter == 3:
                            self.positive_tranding = True
                            self.actual_value = float( ping_value["last"] )
                    else:
                        counter = 0
                
                if self.positive_tranding == True:
                    resp = self.buy()
                    self.mailHandler.addText(resp)
                    self.wallet_value = self.maxBTCValue =self.actual_value              

    def buy(self):
        serviceHandler = ServiceHandler( )
        wallet = serviceHandler.getWallet( )
        btc_value = serviceHandler.getBTCValue( )
        self.actual_value = float( btc_value["last"] )
        self.wallet_value = self.maxBTCValue =self.actual_value

        print("Actual value: ", self.actual_value, " Buying...")
        response = serviceHandler.setOrder("buy", "BTC-EUR", round( wallet["available"] ) )
        return response

    def sell(self):
        serviceHandler = ServiceHandler( )
        wallet = serviceHandler.getWallet( )
        btc_value = serviceHandler.getBTCValue( )
        self.actual_value = float( btc_value["last"] )
        self.wallet_value = self.maxBTCValue =self.actual_value

        print("Actual value: ", self.actual_value, " Selling...")
        response = serviceHandler.setOrder("sell", "BTC-EUR", wallet["available"] )
        return response


#
# MAIN 
# 
crypto_bot = CryptoBot()
serviceHandler = ServiceHandler( )
wallet = serviceHandler.getWallet( )
if wallet["currency"] == "EUR":
   crypto_bot.buy() 

while True:
    crypto_bot.update()
    time.sleep(crypto_bot.time)
    print("Refreshing...")