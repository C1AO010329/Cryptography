import binascii
import gmpy2


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


# 共模攻击
def sameMod():
    index1 = 0
    index2 = 0
    for i in range(21):
        for j in range(i + 1, 21):
            if F[i] == F[j]:
                index1, index2 = i, j
    n = int(F[index1], 16)
    e1 = int(T[index1], 16)
    e2 = int(T[index2], 16)
    c1 = int(S[index1], 16)
    c2 = int(S[index2], 16)
    s = egcd(e1, e2)
    s1 = s[1]
    s2 = s[2]
    if s1 < 0:
        s1 = - s1
        c1 = gmpy2.invert(c1, n)
    elif s2 < 0:
        s2 = - s2
        c2 = gmpy2.invert(c2, n)

    m = pow(c1, s1, n) * pow(c2, s2, n) % n

    print(m)
    print(binascii.a2b_hex(hex(m)[2:]))
    result = binascii.a2b_hex(hex(m)[2:])
    return result


if __name__ == "__main__":
    F = []
    S = []
    T = []
    for i in range(21):
        with open("./Data/Frame" + str(i), "r") as f:
            tmp = f.read()
            F.append(tmp[0:256])
            T.append(tmp[256:512])
            S.append(tmp[512:768])
    # 共模攻击
    plaintext = sameMod()
    print(plaintext)
