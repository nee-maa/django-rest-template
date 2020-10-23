import base64
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:

    @staticmethod
    def generate_random_key():
        return base64.b64encode(Random.new().read(32)).decode()

    def __init__(self, key):
        self.bs = 16
        self.key = base64.b64decode(key.encode())

    def encrypt(self, message):
        message = self._pad(message.encode())
        iv = Random.new().read(AES.block_size)

        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(message)).decode('utf-8')

    def decrypt(self, enc, iv=None):
        enc = base64.b64decode(enc)
        if not iv:
            iv = enc[:AES.block_size]
            enc = enc[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode('UTF-8')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
