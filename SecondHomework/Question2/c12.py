from Crypto import Random

from c10 import *


class ECBOracle:
    def __init__(self, secret_padding):
        self._key = Random.new().read(AES.key_size[0])
        self._secret_padding = secret_padding

    def encrypt(self, data):
        return encrypt_aes_128_ecb(data + self._secret_padding, self._key)


def find_block_length(encryption_oracle):
    my_text = b""
    ciphertext = encryption_oracle.encrypt(my_text)
    initial_len = len(ciphertext)
    new_len = initial_len

    while new_len == initial_len:
        my_text += b"A"
        ciphertext = encryption_oracle.encrypt(my_text)
        new_len = len(ciphertext)

    return new_len - initial_len
