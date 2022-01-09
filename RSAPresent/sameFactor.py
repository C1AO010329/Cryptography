import binascii
import gmpy2


def sameFactor():
    index = []
    for i in range(21):
        for j in range(i + 1, 21):
            if int(F[i], 16) == int(F[j], 16):
                continue
            prime = gmpy2.gcd(int(F[i], 16), int(F[j], 16))
            if prime != 1:
                index.append(i)
                index.append(j)
                frameP = prime
    frameQ1 = int(F[index[0]], 16) // frameP
    frameQ18 = int(F[index[1]], 16) // frameP

    framePhi1 = (frameP - 1) * (frameQ1 - 1)
    framePhi18 = (frameP - 1) * (frameQ18 - 1)

    frameD1 = gmpy2.invert(int(T[index[0]], 16), framePhi1)
    frameD18 = gmpy2.invert(int(T[index[1]], 16), framePhi18)

    plaintext1 = gmpy2.powmod(int(S[index[0]], 16), frameD1, int(F[index[0]], 16))
    plaintext18 = gmpy2.powmod(int(S[index[1]], 16), frameD18, int(F[index[1]], 16))

    fin1 = binascii.a2b_hex(hex(plaintext1)[-16:]).decode('ascii')
    fin18 = binascii.a2b_hex(hex(plaintext18)[-16:]).decode('ascii')

    print('Frame', index[0], ':', fin1, sep='')
    print('Frame', index[1], ':', fin18, sep='')

    return 0


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
    plaintext = sameFactor()
