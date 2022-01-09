plaintext = "The secret message is: When using a stream cipher, never use the key more than once"
ciphertext = "32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904"
ciphertext8 = "315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3"


def charListToHexList(charList):
    plainHexList = []
    for i in charList:
        plainHexList.append(hex(ord(i)))
    return plainHexList


if __name__ == '__main__':
    keyList = []
    plainList8 = []
    plaintext8 = ""
    plainList = list(plaintext)
    plainHexList = (charListToHexList(plainList))
    cipherHex = bytes.fromhex(ciphertext)
    cipherHex8 = bytes.fromhex(ciphertext8)

    for i in range(0, len(plainHexList)):
        keyList.append(cipherHex[i] ^ int(plainHexList[i], 16))
        plainList8.append(keyList[i] ^ cipherHex8[i])
    for i in range(0, len(plainList8)):
        plaintext8 += chr(plainList8[i])

    print("密钥（10进制ASCII码表示）：", keyList)
    print("第八组明文：" + plaintext8)
