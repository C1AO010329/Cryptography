import base64
from functools import partial
import itertools

letterFreqs = \
    {'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339,
     'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881,
     'g': 0.0158610, 'h': 0.0492888, 'i': 0.0558094,
     'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
     'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302,
     'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563,
     's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
     'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
     'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}  # 字母频率


def GetScore(ib):  # 计算输入文本的分值
    score = 0
    for b in ib:
        score += letterFreqs.get(chr(b).lower(), 0)
    return score


def SingleXOR(ib, KeyValue):  # 对每个字符和Key异或
    output = b""
    for ch in ib:
        output += bytes([ch ^ KeyValue])
    return output


def SingleXorBreak(ciphertext):  # 破解单字符异或
    choices = []
    for KeyChoice in range(256):
        PlaintextChoice = SingleXOR(ciphertext, KeyChoice)
        ScoreChoice = GetScore(PlaintextChoice)
        result = {
            "key": KeyChoice,
            "score": ScoreChoice,
            "plaintext": PlaintextChoice
        }
        choices.append(result)
    return sorted(choices, key=lambda c: c['score'], reverse=True)[0]


def HammingDistance(bstr1, bstr2):  # 汉明距离
    distance = 0
    for b1, b2 in zip(bstr1, bstr2):
        dis = b1 ^ b2
        distance += sum([1 for bit in bin(dis) if bit == "1"])
    return distance


def KeyXOR(plaintext, Key):
    ciphertext = b""
    i = 0
    for b in plaintext:
        ciphertext += bytes([b ^ Key[i]])
        i = i + 1 if i < len(Key) - 1 else 0
    return ciphertext


def KeyBreak(text):
    NorDistances = {}
    for KeySize in range(2, 30):
        Slices = [text[i:i + KeySize] for i in range(0, len(text), KeySize)][:4]
        TempDistance = 0
        SlicePair = itertools.combinations(Slices, 2)
        for (a, b) in SlicePair:
            TempDistance += HammingDistance(a, b)
        TempDistance /= 6
        NorDistance = TempDistance / KeySize  # 对汉明距离进行归一化
        NorDistances[KeySize] = NorDistance
    PossibleKeySize = sorted(NorDistances, key=NorDistances.get)[:3]  # 取最小的3个汉明距离所对应的KeySize
    PossiblePlaintext = []
    for i in PossibleKeySize:
        TempKey = b""
        for j in range(i):
            block = b""
            for k in range(j, len(text), i):
                block += bytes([text[k]])
            TempKey += bytes([SingleXorBreak(block)["key"]])
        PossiblePlaintext.append((KeyXOR(text, TempKey), TempKey))
    return max(PossiblePlaintext, key=lambda k: GetScore(k[0]))  # 选取分数最高，即最有可能是正确明文的那一组


if __name__ == '__main__':
    with open("H3.txt") as fp:
        text = base64.b64decode(fp.read())
    result = KeyBreak(text)
    print("Key=", result[1].decode())
    print("----------result----------")
    print(result[0].decode().rstrip())

"""
思路：
1. 猜测密钥长度KeySize，如从2-30
2. 计算两个字符串之间的汉明距离
3. 每次尝试KeySize时，从文件开头截取四个块，两两组合计算其汉明距离
4. 选取3个最小的汉明距离所对应的KeySize作为密钥长度备选
5. 知道KeySize大小后，将密文按KeySize大小切片，每片取第一个、第二个……组成新的块
6. 对新的块而言，解密思路类似作业第2题
7. 将每个单字符异或的Key拼接起来即为所要的最终的Key，将明文拼接即为完整明文
"""
