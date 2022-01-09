import gmpy2
import binascii

def p1(n):
    B = pow(2,20)
    a = 2
    for i in range(2, B + 1):
        a = pow(a, i, n)
        d = gmpy2.gcd(a - 1, n)
        if (d >= 2) and (d <= (n - 1)):
            q = n // d
            n = q * d
    return d


def pollardResolve():
    index_list = [2, 6, 19]
    plaintext = []
    for i in range(3):
        N = int(F[index_list[i]], 16)
        c = int(S[index_list[i]], 16)
        e = int(T[index_list[i]], 16)
        p = p1(N)
        q = N // p
        framePhi = (p - 1) * (q - 1)
        d = gmpy2.invert(e, framePhi)
        m = gmpy2.powmod(c, d, N)
        plaintext.append(binascii.a2b_hex(hex(m)[2:]))
        print(f"Frame{index_list[i]}:{(binascii.a2b_hex(hex(m)[-16:])).decode('ascii')}")
    return plaintext


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
    plaintext = pollardResolve()