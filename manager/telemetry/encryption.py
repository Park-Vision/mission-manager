import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes
# import codecs

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = key

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    # def decrypt(self, enc: str):
    #     parts = enc.split(':')
    #     iv = base64.b64decode(parts[0])
    #     encrypted_bytes = base64.b64decode(parts[1])
        
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return AESCipher._unpad(cipher.decrypt(encrypted_bytes)).decode('utf-8')

    def decrypt(self, encrypted_message):
        encrypted_message = str(encrypted_message)
        iv, encrypted_data = encrypted_message.split(':')

        cipher = AES.new(base64.b64decode(self.key), AES.MODE_CBC, iv=base64.b64decode(iv))

        decrypted_message = cipher.decrypt(base64.b64decode(encrypted_data))

        return decrypted_message.decode('utf-8')


    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]