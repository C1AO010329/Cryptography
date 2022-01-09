from Crypto.Cipher.AES import block_size
from base64 import b64decode
from c7 import *
from c9 import *


def encrypt_aes_128_ecb(message, key):
    cipher_message = AES.new(key, AES.MODE_ECB)
    return cipher_message.encrypt(pkcs7_padding(message, AES.block_size))


def ez_xor(bin_data1, bin_data2):
    return bytes([b1 ^ b2 for b1, b2 in zip(bin_data1, bin_data2)])


def encrypt_aes_128_cbc(message, key, iv):
    ciphertext = b""
    p = iv
    for i in range(0, len(message), AES.block_size):
        temp_plaintext_block = pkcs7_padding(message[i: i + AES.block_size], AES.block_size)
        block_ciphertext_in = ez_xor(temp_plaintext_block, p)
        encrypted_block = encrypt_aes_128_ecb(block_ciphertext_in, key)
        ciphertext += encrypted_block
        p = encrypted_block

    return ciphertext


def decrypt_aes_128_cbc(data, key, iv, unpad=True):
    plaintext = b""
    p = iv
    for i in range(0, len(data), AES.block_size):
        temp_ciphertext_block = data[i:i + AES.block_size]
        decrypted_blcok = decrypt_aes_128_ecb(temp_ciphertext_block, key)
        plaintext += ez_xor(p, decrypted_blcok)
        p = temp_ciphertext_block

    return pkcs7_unpad(plaintext) if unpad else plaintext


def main():
    iv = b'\x00' * AES.block_size
    key = b"YELLOW SUBMARINE"
    with open("10.txt") as f:
        bin_data = b64decode(f.read())
    print(decrypt_aes_128_cbc(bin_data, key, iv).decode().rstrip())


if __name__ == '__main__':
    main()
