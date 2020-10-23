import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


class RSAEncryption:
    def __init__(self, private_key_name=None, public_key_name=None, generate_new=False):
        if generate_new:
            self.generate_key(1024)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            with open("{}/{}".format(current_directory, private_key_name), 'r') as file:
                self.private_key = file.read()

            with open("{}/{}".format(current_directory, public_key_name), 'r') as file:
                self.public_key = file.read()

            self.rsa_private_key = PKCS1_OAEP.new(RSA.importKey(self.private_key))
            self.rsa_public_key = PKCS1_OAEP.new(RSA.importKey(self.public_key))

    def generate_key(self, bs):
        key = RSA.generate(bs)
        self.private_key = key.export_key('PEM')
        self.public_key = key.publickey().exportKey('PEM')
        with open('public.pem', 'w') as file:
            file.write(self.public_key.decode())

        with open('private.pem', 'w') as file:
            file.write(self.private_key.decode())

        self.rsa_private_key = PKCS1_OAEP.new(RSA.importKey(self.private_key))
        self.rsa_public_key = PKCS1_OAEP.new(RSA.importKey(self.public_key))

        return self.rsa_public_key, self.rsa_private_key

    def encrypt(self, plain_text):
        return base64.b64encode(self.rsa_public_key.encrypt(plain_text.encode())).decode()

    def decrypt(self, encrypted_message):
        return self.rsa_private_key.decrypt(base64.b64decode(encrypted_message.encode())).decode()
