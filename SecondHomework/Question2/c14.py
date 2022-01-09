from random import randint

from c12 import *
from c8 import *


class HarderECBOracle(ECBOracle):
    def __init__(self, secret_padding):
        super(HarderECBOracle, self).__init__(secret_padding)
        self._random_prefix = Random.new().read(randint(0, 255))

    def encrypt(self, data):
        return encrypt_aes_128_ecb(self._random_prefix + data + self._secret_padding, self._key)


def get_next_byte(prefix_length, block_length, curr_decrypted_message, encryption_oracle):
    length_to_use = (block_length - prefix_length - (1 + len(curr_decrypted_message))) % block_length
    my_input = b"A" * length_to_use
    cracking_length = prefix_length + length_to_use + len(curr_decrypted_message) + 1
    real_ciphertext = encryption_oracle.encrypt(my_input)
    for i in range(256):
        fake_ciphertext = encryption_oracle.encrypt(my_input + curr_decrypted_message + bytes([i]))
        if fake_ciphertext[:cracking_length] == real_ciphertext[:cracking_length]:
            return bytes([i])
    return b""


def has_equal_block(ciphertext, block_length):
    for i in range(0, len(ciphertext) - 1, block_length):
        if ciphertext[i:i + block_length] == ciphertext[i + block_length:i + 2 * block_length]:
            return True
    return False


def find_prefix_length(encryption_oracle, block_length):
    ciphertext1 = encryption_oracle.encrypt(b"")
    ciphertext2 = encryption_oracle.encrypt(b"a")
    prefix_length = 0
    for i in range(0, len(ciphertext2), block_length):
        if ciphertext1[i:i + block_length] != ciphertext2[i:i + block_length]:
            prefix_length = i
            break
    for i in range(block_length):
        fake_input = bytes([0] * (2 * block_length + i))
        ciphertext = encryption_oracle.encrypt(fake_input)
        if has_equal_block(ciphertext, block_length):
            return prefix_length + block_length - i if i != 0 else prefix_length
    raise Exception("the oracle is not using ECB")


def byte_at_a_time_ecb_harder_decryption(encryption_oracle):
    block_length = find_block_length(encryption_oracle)
    ciphertext = encryption_oracle.encrypt(bytes([0] * 64))
    assert count_aes_ecb_repetitions(ciphertext) > 0
    prefix_length = find_prefix_length(encryption_oracle, block_length)
    mysterious_text_length = len(encryption_oracle.encrypt(b"")) - prefix_length
    secret_padding = b""
    for i in range(mysterious_text_length):
        secret_padding += get_next_byte(prefix_length, block_length, secret_padding, encryption_oracle)
    return secret_padding


def main():
    secret_padding = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
                               "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
                               "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
                               "YnkK")
    oracle = HarderECBOracle(secret_padding)
    discovered_secret_padding = byte_at_a_time_ecb_harder_decryption(oracle)
    print(pkcs7_unpad(discovered_secret_padding))


if __name__ == '__main__':
    main()