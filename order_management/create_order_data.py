import hashlib
import hmac
import json
import time

from get_current_market_data import get_current_market_data


def create_order_data(symbol, order_type, url, amount):
    fresh_data = get_current_market_data()
    public_key = "uHM6vrJgni8QtNo9QIh944t5Pi2xPAH7fGvZLnr0"
    secret_key = "aNsPFSVGiJX8Ib0FGJ3OEgACFTTJxGLpuweV1Y8Y"

    # generating relevant parameters
    nonce = str(int(time.time() * 1000))
    # generating HEX signature for the request
    new_body = {
        "symbol": symbol,
        "type": order_type,
        "amount": amount,
        "price": int(fresh_data[0][3])
    }
    request_body = json.loads(json.dumps(new_body))
    print("Body: " + str(request_body))

    signature_string = f"{url}{nonce}{json.dumps(new_body)}"
    signature_hex = hmac.new(bytes(secret_key, 'utf-8'), bytes(signature_string, 'utf-8'), digestmod=hashlib.sha384)

    # generating headers for the request
    order_headers = {'accept': 'application/json', 'content-type': 'application/json', 'kun-nonce': nonce,
                     'kun-apikey': public_key, 'kun-signature': signature_hex.hexdigest()}

    return order_headers, request_body, fresh_data
