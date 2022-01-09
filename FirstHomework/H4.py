import hashlib
import itertools
import datetime

starttime = datetime.datetime.now()
hash1 = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"
searchList = [['Q', 'q'], ['W', 'w'], ['I', 'i'], ['N', 'n'], ['5', '%'], ['8', '('], ['0', '='], ['*', '+']]


def encryptSha(str):
    sha = hashlib.sha1(str.encode("utf-8"))
    encrypts = sha.hexdigest()
    return encrypts


if __name__ == '__main__':
    zeroStr = "00000000"
    str4 = ""
    zeroList = list(zeroStr)
    for a in range(0, 2):
        zeroList[0] = searchList[0][a]
        for b in range(0, 2):
            zeroList[1] = searchList[1][b]
            for c in range(0, 2):
                zeroList[2] = searchList[2][c]
                for d in range(0, 2):
                    zeroList[3] = searchList[3][d]
                    for e in range(0, 2):
                        zeroList[4] = searchList[4][e]
                        for f in range(0, 2):
                            zeroList[5] = searchList[5][f]
                            for g in range(0, 2):
                                zeroList[6] = searchList[6][g]
                                for h in range(0, 2):
                                    zeroList[7] = searchList[7][h]
                                    finStr = "".join(zeroList)
                                    for i in itertools.permutations(finStr, 8):
                                        str4 = encryptSha("".join(i))
                                        if str4 == hash1:
                                            print("".join(i))
                                            endtime = datetime.datetime.now()
                                            print("time: " + str(endtime - starttime))
