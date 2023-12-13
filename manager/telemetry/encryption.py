import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes
# import codecs


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = key

    def encrypt(self, message):
        key = base64.b64decode(self.key)
        iv = get_random_bytes(16)

        cipher = AES.new(key, AES.MODE_CBC, iv)

        length = AES.block_size - (len(message) % AES.block_size)
        message += chr(length) * length

        encrypted = cipher.encrypt(message.encode("utf-8"))

        iv_base64 = base64.b64encode(iv).decode("utf-8")
        encrypted_base64 = base64.b64encode(encrypted).decode("utf-8")
        # print(iv_base64 + ":" + encrypted_base64)
        return iv_base64 + ":" + encrypted_base64

    def decrypt(self, encrypted_message):
        encrypted_message = str(encrypted_message)
        iv, encrypted_data = encrypted_message.split(":")

        cipher = AES.new(
            base64.b64decode(self.key), AES.MODE_CBC, iv=base64.b64decode(iv)
        )

        decrypted_message = cipher.decrypt(base64.b64decode(encrypted_data))

        return decrypted_message.decode("utf-8")
