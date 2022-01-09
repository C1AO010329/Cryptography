# coding=utf-8


import base64
import re

from Crypto.Cipher import AES
from Crypto.Hash import SHA


def odd_even_verify(ka):  # 调整奇偶校验位
    k = []
    for i in ka:
        if bin(int(i, 16) >> 1).count('1') % 2 == 0:  # 若1的个数为偶数
            k += [hex(1 + (int(i, 16) >> 1 << 1))[2:].zfill(2)]  # 调整为奇数
        else:
            k += [hex((int(i, 16) >> 1 << 1))[2:].zfill(2)]  # 不动
    return ''.join(k)


def get_sha1(d):
    h = SHA.new()
    h.update(d)  # 计算d的sha1
    return h.hexdigest()[:32]  # 获取sha1的前32位


def main():
    c = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6' \
        '+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI '  # C由文档中获取
    c = base64.b64decode(c)
    code = '12345678<8<<<1110182<1111167<<<<<<<<<<<<<<<4'
    code_no = code[:9]
    code_verify = code[9]
    nation = code[10:13]
    birth = code[13:19]
    birth_verify = code[19]
    sex = code[20]
    date_end = code[21:27]
    date_end_verify = code[27]
    other = code[28:]
    # 按照文件提取code中机读区对应的信息
    info = code_no + code_verify + birth + birth_verify + date_end + date_end_verify  # 得到机读区信息
    k_seed = get_sha1(info)  # 获取k_seed
    d = (k_seed + '0' * 7 + '1').decode('hex')  # 连接k_seed和c
    key = get_sha1(d)  # 获取key的sha1
    k1 = odd_even_verify(re.findall('.{2}', key[:16]))  # 对前半后半分别进行奇偶校验位的调整
    k2 = odd_even_verify(re.findall('.{2}', key[16:]))
    key = k1 + k2  # 再将密钥key拼接起来
    print 'The key is:', key
    ciphertext = AES.new(key.decode('hex'), AES.MODE_CBC, ('0' * 32).decode('hex'))
    print 'The M is:', ciphertext.decrypt(c)


if __name__ == '__main__':
    main()
