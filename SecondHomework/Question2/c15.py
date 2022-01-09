def is_pkcs7_padded(bin_data):
    padding = bin_data[-bin_data[-1]:]
    return all(padding[b] == len(padding) for b in range(0, len(padding)))