def pkcs7_padding(message,block_size):
    if len(message) == block_size:
        return message
    padding_thing = block_size - (len(message) % block_size)  # 填充内容、长度计算
    return message + bytes([padding_thing] * padding_thing)


def is_pkcs7_padded(bin_data):
    padding = bin_data[-bin_data[-1]:]
    return all(padding[b] == len(padding) for b in range(0, len(padding)))


def pkcs7_unpad(padded_message):
    if len(padded_message) == 0:
        raise Exception("the input must contain at least one byte!")
    if not is_pkcs7_padded(padded_message):
        return padded_message
    padded_len = padded_message[len(padded_message) - 1]
    return padded_message[:-padded_len]


def c9_main():
    message=b"YELLOW SUBMARINE"
    padded_message = pkcs7_padding(message, 20)
    print(padded_message)
    assert pkcs7_unpad(padded_message) == message


if __name__ == '__main__':
    c9_main()