import hashlib
import hmac
import json
import time


def create_request_headers(url, body):
    public_key = "uHM6vrJgni8QtNo9QIh944t5Pi2xPAH7fGvZLnr0"
    secret_key = "aNsPFSVGiJX8Ib0FGJ3OEgACFTTJxGLpuweV1Y8Y"

    # generating relevant parameters
    nonce = str(int(time.time() * 1000))
    # generating HEX signature for the request
    request_body = json.loads(json.dumps(body))
    print("Body: " + str(request_body))

    signature_string = f"{url}{nonce}{json.dumps(body)}"
    signature_hex = hmac.new(bytes(secret_key, 'utf-8'), bytes(signature_string, 'utf-8'), digestmod=hashlib.sha384)

    # generating headers for the request
    order_headers = {'accept': 'application/json', 'content-type': 'application/json', 'kun-nonce': nonce,
                     'kun-apikey': public_key, 'kun-signature': signature_hex.hexdigest()}

    return order_headers
