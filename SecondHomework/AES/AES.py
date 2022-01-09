# -*- coding: cp936 -*-

from oracle import *
from Crypto.Util import strxor
import re


def main():
    CipherText = "9F0B13944841A832B2421B9EAF6D9836813EC9D944A5C8347A7CA69AA34D8DC0" \
                 "DF70E343C4000A2AE35874CE75E64C31"
    BlockCount = 2
    Division = len(CipherText) / (BlockCount + 1)
    CipherTextList = re.findall(".{" + str(Division) + "}", CipherText)

    Oracle_Connect()
    PlainText = []
    IVALUE = []
    for bc in range(0, BlockCount):  # 对两组密文分别求解
        print "-" * 60
        print "Now Detecting Block " + str(bc + 1) + "."
        IV = CipherTextList[bc]
        ivalue = []  # 将解密后的ciphertext初始化
        TempIV = "0" * 32  # 初始化 IV
        TempIV = re.findall('.{2}', TempIV)[::-1]
        padding = 1
        for l in range(16):
            print "-" * 60
            print "Now Detecting Last " + str(l + 1) + ' Byte In Block.'
            for ll in range(l):
                TempIV[ll] = hex(int(ivalue[ll], 16) ^ padding)[2:].zfill(2)  # 更新 TempIV

            for n in range(0, 256):  # 从0x00-0xFF遍历寻找符合条件的字节
                TempIV[l] = hex(n)[2:].zfill(2)
                data = "".join(TempIV[::-1]) + CipherTextList[bc + 1]
                print data
                ctext = [(int(data[i:i + 2], 16)) for i in range(0, len(data), 2)]
                Feedback = Oracle_Send(ctext, 2)
                if str(Feedback) == "1":
                    ivalue += [hex(n ^ padding)[2:].zfill(2)]
                    break
            print "-" * 60
            print "Now The Value of IV is: ", "".join(TempIV[::-1])
            print "The Temporary Ciphertext after Decryption is: ", "".join(ivalue[::-1])

            padding += 1
        ivalue = "".join(ivalue[::-1])
        IVALUE += [ivalue]
        # IV与CADe异或求明文
        plaintext = re.findall("[0-9a-f]+", str(hex(int(IV, 16) ^ int("".join(ivalue), 16))))[1].decode("hex")
        PlainText += [plaintext]
        print "Detecting Block", bc + 1, "Finished."
        print "The ivalue" + str(bc + 1) + " is:", ivalue
        print "The Plaintext" + str(bc + 1) + "is:", plaintext
        print "-" * 60
    Oracle_Disconnect()
    print "The Ciphertext after Decryption is: ", "".join(IVALUE)
    print "The Plaintext is:", "".join(PlainText)


if __name__ == '__main__':
    main()
