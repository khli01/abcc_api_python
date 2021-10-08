import requests
import time
import json
import hmac
import hashlib
import urllib.parse
import base64

class RestApiAbcc:
    
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def get_timestamp(self):
        url = "https://api.abcc.com/api/v1/common/timestamp"
        output = requests.request("GET", url).text
        return output

    def get_markets(self):
        url = "https://api.abcc.com/api/v1/common/markets"
        output = requests.request("GET", url).text
        return output

    def get_depth(self, market):
        url = "https://api.abcc.com/api/v1/exchange/order_book"
        payload = {
            "market_code": market
        }
        output = requests.request("GET", url, params=payload).text
        return output

    def get_balance(self):
        url = "https://api.abcc.com/api/v1/members/me"
        timestamp = round(time.time(), 7)
        request_method = "GET|"
        request_endpoint = "/api/v1/members/me|"
        data = {
            "access_key": self.api_key,
            "tonce": timestamp
        }
        params_str = request_method+request_endpoint+urllib.parse.urlencode(data)
        signature = hmac.new(self.secret_key.encode(encoding="utf-8"), params_str.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest()
        data["signature"] = signature
        output = requests.get(url, params=data).text
        return output       

    def post_order(self, market, side, order_type, amount, price=None):
        url = "https://api.abcc.com/api/v1/exchange/orders"
        timestamp = round(time.time(), 7)
        request_method = "POST|"
        request_endpoint = "/api/v1/exchange/orders|"
        data = {
            "access_key": self.api_key,
            "market_code": market,
            "ord_type": order_type,
            "price": str(price),
            "side": side,
            "tonce": timestamp,
            "volume": str(amount)
        }
        params_str = request_method+request_endpoint+urllib.parse.urlencode(data)
        signature = hmac.new(self.secret_key.encode(encoding="utf-8"), params_str.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest()
        data["signature"] = signature
        output = requests.post(url, params=data).text
        return output   

    def query_orders(self):
        url = "https://api.abcc.com/api/v1/exchange/orders"
        timestamp = round(time.time(), 7)
        request_method = "GET|"
        request_endpoint = "/api/v1/exchange/orders|"
        data = {
            "access_key": self.api_key,
            "direction": "asc",
            "per_page": 5000,
            "tonce": timestamp
        }
        params_str = request_method+request_endpoint+urllib.parse.urlencode(data)
        signature = hmac.new(self.secret_key.encode(encoding="utf-8"), params_str.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest()
        data["signature"] = signature
        output = requests.get(url, params=data).text
        return output       

    def query_order(self, order_id):
        url = "https://api.abcc.com/api/v1/exchange/orders/{}".format(order_id)
        timestamp = round(time.time(), 7)
        request_method = "GET|"
        request_endpoint = "/api/v1/exchange/orders/{}|".format(order_id)
        data = {
            "access_key": self.api_key,
            "order_id": str(order_id),
            "tonce": timestamp
        }
        params_str = request_method+request_endpoint+urllib.parse.urlencode(data)
        signature = hmac.new(self.secret_key.encode(encoding="utf-8"), params_str.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest()
        data["signature"] = signature
        output = requests.get(url, params=data).text
        return output       

    def cancel_order(self, order_id):
        url = "https://api.abcc.com/api/v1/exchange/orders/{}/cancel".format(order_id)
        timestamp = round(time.time(), 7)
        request_method = "POST|"
        request_endpoint = "/api/v1/exchange/orders/{}/cancel|".format(order_id)
        data = {
            "access_key": self.api_key,
            "order_id": order_id,
            "tonce": timestamp
        }
        params_str = request_method+request_endpoint+urllib.parse.urlencode(data)
        signature = hmac.new(self.secret_key.encode(encoding="utf-8"), params_str.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest()
        data["signature"] = signature
        output = requests.post(url, params=data).text
        return output  
