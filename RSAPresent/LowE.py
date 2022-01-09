import binascii

import gmpy2


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def ChineseRemainder(items):
    N = 1
    for a, n in items:
        N *= n
        result = 0
    for a, n in items:
        m = N // n
        d, r, s = egcd(n, m)
        if d != 1:
            N = N // n
            continue
        result += a * s * m
    return result % N, N


def lowE():
    sessions = [{"c": int(S[3], 16), "n": int(F[3], 16)},
                {"c": int(S[8], 16), "n": int(F[8], 16)},
                {"c": int(S[12], 16), "n": int(F[12], 16)},
                {"c": int(S[16], 16), "n": int(F[16], 16)},
                {"c": int(S[20], 16), "n": int(F[20], 16)}]
    data = []
    for session in sessions:
        data += [(session['c'], session['n'])]
    x, y = ChineseRemainder(data)

    pt = gmpy2.iroot(gmpy2.mpz(x), 5)
    print(binascii.a2b_hex(hex(pt[0])[-16:]).decode('ascii'))

    return binascii.a2b_hex(hex(pt[0])[2:])



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
    plaintext = lowE()
