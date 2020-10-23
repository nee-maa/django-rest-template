import base64
import json
from io import BytesIO
from .aes import AESCipher
from .rsa import RSAEncryption

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != 'POST':
            return HttpResponseNotAllowed(permitted_methods=['post'])

        if "no_cipher" in request.GET.keys():
            return self.get_response(request)

        if request.body:
            __body = json.loads(request.body.decode())
            __key = __body.get("token")
            __encrypted_data = __body.get("data")

            if __key is None or __encrypted_data is None:
                return HttpResponseBadRequest(content=json.dumps({"text": "Bad request"}).encode())

            try:
                __decrypted_key = RSAEncryption(private_key_name='private.pem', public_key_name='public.pem').decrypt(__key)
                aes = AESCipher(__decrypted_key)
                __decrypted_data = aes.decrypt(__encrypted_data)
            except:
                return HttpResponseBadRequest(content=json.dumps({"text": "Bad request"}).encode())

            request._body = __decrypted_data.encode()

        response = self.get_response(request)

        if response.data:
            __enc_data = aes.encrypt(json.dumps(response.data))
            response.data = {"token": __key, "data": __enc_data}
            response._is_rendered = False
            response.render()
        return response
