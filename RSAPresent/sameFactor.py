import binascii
import gmpy2


def sameFactor():
    plaintexts = []
    index = []
    for i in range(21):
        for j in range(i + 1, 21):
            if int(F[i], 16) == int(F[j], 16):
                continue
            prime = gmpy2.gcd(int(F[i], 16), int(F[j], 16))
            if prime != 1:
                print((F[i], F[j]))
                print((i, j))
                index.append(i)
                index.append(j)
                frameP = prime
    frameQ1 = int(F[index[0]], 16) // frameP
    frameQ18 = int(F[index[1]], 16) // frameP
    print(frameP)
    print(frameQ1, frameQ18)

    framePhi1 = (frameP - 1) * (frameQ1 - 1)
    framePhi18 = (frameP - 1) * (frameQ18 - 1)

    frameD1 = gmpy2.invert(int(T[index[0]], 16), framePhi1)
    frameD18 = gmpy2.invert(int(T[index[1]], 16), framePhi18)

    plaintext1 = gmpy2.powmod(int(S[index[0]], 16), frameD1, int(F[index[0]], 16))
    plaintext18 = gmpy2.powmod(int(S[index[1]], 16), frameD18, int(F[index[1]], 16))

    fin1 = binascii.a2b_hex(hex(plaintext1)[2:])
    fin18 = binascii.a2b_hex(hex(plaintext18)[2:])

    plaintexts.append(fin1)
    plaintexts.append(fin18)

    return plaintexts


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
    print(plaintext)
