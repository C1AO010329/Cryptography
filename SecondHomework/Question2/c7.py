from Crypto.Cipher import AES
from c9 import *


def decrypt_aes_128_ecb(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return pkcs7_unpad(cipher.decrypt(data))