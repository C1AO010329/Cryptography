import binascii

import gmpy2
import math


def fermat(n):
    B = math.factorial(2 ** 14)
    v = 0
    i = 0
    u0 = gmpy2.iroot(n, 2)[0] + 1
    while i <= (B - 1):
        u = (u0 + i) * (u0 + i) - n
        if gmpy2.is_square(u):
            v = gmpy2.isqrt(u)
            break
        i += 1
    p = u0 + i + v
    return p


def fermatResolve():
    for i in range(10, 14):
        N = int(F[i], 16)
        p = fermat(N)



if __name__ == "__main__":
    F = []
    S = []
    T = []
    with open("./Data/Frame10", "r") as f:
        tmp = f.read()
        F.append(tmp[0:256])
        T.append(tmp[256:512])
        S.append(tmp[512:768])
    p = 9686924917554805418937638872796017160525664579857640590160320300805115443578184985934338583303180178582009591634321755204008394655858254980766008932978699
    n = int(F[0], 16)
    c = int(S[0], 16)
    e = int(T[0], 16)
    q = n // p
    framePhi10 = (p - 1) * (q - 1)
    d = gmpy2.invert(e, framePhi10)
    m = gmpy2.powmod(c, d, n)
    final_plain = binascii.a2b_hex(hex(m)[-16:]).decode("ascii")
    print(f"Frame10:{final_plain}")

