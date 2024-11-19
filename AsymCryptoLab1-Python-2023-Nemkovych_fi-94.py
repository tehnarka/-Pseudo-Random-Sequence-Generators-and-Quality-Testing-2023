import math
import random
import collections
import pandas as pd
from datetime import datetime
import numpy as np

########################################################################   Lehmers

def decimalToBinary32(n):
    n = bin(n).replace("0b", "")
    if len(n) < 32:
        n = (32 - len(n))*'0' + n
    return n

def lehmer(n, type):
    lst = []
    a = 2 ** 16 + 1
    m = 2 ** 32
    c = 119
    x_0 = random.randint(1, m)
    for i in range(0, int(n/8) + 1):
        x_i = (a * x_0 + c) % m
        x_0 = x_i
        lst.append(x_i)
    i = 0
    if type == 'low':
        while i < len(lst):
            lst[i] = decimalToBinary32(lst[i])
            lst[i] = lst[i][24:32]
            i += 1
    else:
        while i < len(lst):
            lst[i] = decimalToBinary32(lst[i])
            lst[i] = lst[i][0:8]
            i += 1
    lst1 = []
    i = 0
    while i < len(lst):
        j = 0
        while j < 8:
            lst1.append(int(lst[i][j]))
            j += 1
        i += 1
    while len(lst1) > n:
        lst1.pop()
    return lst1


########################################################################   L20-89

def L20(n):
    lst = []
    for i in range(0, 20):
        lst.append(random.randint(0, 1))
    t = 20
    while t < n:
        lst.append(lst[t-3] ^ lst[t-5] ^ lst[t-9] ^ lst[t-20])
        t += 1
    return lst


def L89(n):
    lst = []
    for i in range(0, 89):
        lst.append(random.randint(0, 1))
    t = 89
    while t < n:
        lst.append(lst[t-38] ^ lst[t-89])
        t += 1
    return lst



########################################################################   Geffe

def Geffe(n):
    lst = []

    l11 = []
    for i in range(0, 11):
        l11.append(random.randint(0, 1))

    l9 = []
    for i in range(0, 9):
        l9.append(random.randint(0, 1))
    l9.append(l9[0] ^ l9[1] ^ l9[3] ^ l9[4])
    l9.append(l9[1] ^ l9[2] ^ l9[4] ^ l9[5])

    l10 = []
    for i in range(0, 10):
        l10.append(random.randint(0, 1))
    l10.append(l10[0] ^ l10[3])

    i = 11
    while i < n + 11:
        l11.append(l11[i-11] ^ l11[i-9])
        l9.append(l9[i - 9] ^ l9[i - 8] ^ l9[i - 6] ^ l9[i - 5])
        l10.append(l10[i - 10] ^ l10[i - 7])

        if l10[i] == 0:
            lst.append(l9[i])
        else:
            lst.append(l11[i])
        i += 1

    return lst


########################################################################   Volfram

def Volfram(n):
    lst = []
    temp = []
    for i in range(0, 32):
        temp.append(random.randint(0, 1))
    lst += temp
    while len(lst) <= n:
        temp_left = collections.deque(temp)
        temp_left.rotate(-1)
        temp_left = list(temp_left)
        temp_right = collections.deque(temp)
        temp_right.rotate(1)
        temp_right = list(temp_right)
        temp = [temp[i] or temp_right[i] for i in range(len(temp))]
        temp = [temp_left[i] ^ temp[i] for i in range(len(temp))]
        lst.append(temp[-1])
    return lst


########################################################################   Librarian
# only latin texts
def Librarian(n, text):
    lst = []
    if n > 8 * len(text):
        return 'Error! Text doesn`t have enough bits'
    for i in range(0, int(n/8)):
        temp = ''.join(format(ord(text[i]), '08b'))
        lst += list(temp)
    for i in range(0, len(lst)):
        lst[i] = int(lst[i])
    return lst


########################################################################   BM bit and byte

def BM(n, type):
    lst = []
    n1 = n
    p = hex(0xCEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3)         #len = 66
    a = hex(0x5B88C41246790891C095E2878880342E88C79974303BD0400B090FE38A688356)
    q = hex(0x675215CC3E227D3216C056CFA8F8822BB486F788641E85E0DE77097E1DB049F1)
    p = int(p, 16)          #93466510612868436543809057926265637055082661966786875228460721852868821292003      len = 77
    a = int(a, 16)          #41402113656871763270073938229168765778879686959780184368336806110280536326998
    q = int(q, 16)          #46733255306434218271904528963132818527541330983393437614230360926434410646001

    t = random.randint(1, p - 1)
    if type == 'bit':
        for i in range(0, n):
            if t < (p-1)/2:
                lst.append(1)
            else:
                lst.append(0)
            t = pow(a, t, p)
    else:
        n += 8 - (n % 8)
        n = int(n/8)
        for i in range(0, n):
            k = int((256*t)/(p-1))
            k = bin(k).replace("0b", "")
            if len(k) < 8:
                k = (8 - len(k)) * '0' + k
            k = list(k)
            lst += k
            t = pow(a, t, p)
    while len(lst) > n1:
        lst.pop()
    i = 0
    while i < len(lst):
        lst[i] = int(lst[i])
        i += 1
    return lst          #speed: 0:04:05.391167 for 1000000 bits and 0:00:30.111060 for 125000 bytes(1000000 bits)



########################################################################   BBS bit and byte

def BBS(n, type):
    lst = []
    p = hex(0xD5BBB96D30086EC484EBA3D7F9CAEB07)         #284100283511244958272321698211826428679
    q = hex(0x425D2B9BFDB25B9CF6C416CC6E37B59C1F)       #22582480853028265529707582510375286184991
    p = int(p, 16)
    q = int(q, 16)

    pq = p * q
    r = random.randint(2, pq - 1)
    if type == 'bit':
        for i in range(0, n):
            r = pow(r, 2, pq)
            r_i = bin(r).replace("0b", "")
            lst.append(int(r_i[-1]))
    else:
        for i in range(0, n):
            r = pow(r, 2, pq)
            r_i = bin(r).replace("0b", "")
            for j in range(0, 8):
                lst.append(int(r_i[-1-j]))
    while len(lst) > n:
        lst.pop()
    return lst



########################################################################   criterias
#Z_(1-alfa):=   1.28, when alfa = 0.1;  1.64, when alfa = 0.05;     2.32, when alfa = 0.01

def Equality(seq, alfa):
    m = int(len(seq)/8)
    n_j = int(m/256)
    freq = [0] * 256
    allbytes = []
    for i in range(0, 256):
        var = bin(i).replace("0b", "")
        if len(var) < 8:
            var = (8 - len(var))*'0' + var
        allbytes.append(var)

    i = 0
    while len(seq) % 8 != 0:
        seq.pop()
    while i < len(seq):         #пошук частот байтів
        byte = []
        for j in range(0, 8):
            byte.append(seq[i+j])
        byte = str(byte).replace(",", "")
        byte = byte.replace(" ", "")
        byte = byte.replace("[", "")
        byte = byte.replace("]", "")
        byte = int('0b' + byte, 2)
        freq[byte] += 1
        i += 8

    hee = 0
    for i in range(0, 256):
        hee += ((freq[i] - n_j) ** 2) / n_j

    if alfa == 0.01:
        alfa = 2.32
    if alfa == 0.1:
        alfa = 1.28
    if alfa == 0.05:
        alfa = 1.64
    hee_alfa = math.sqrt(510) * alfa + 255
    if hee <= hee_alfa:
        return 1, hee, hee_alfa
    else:
        return 0, hee, hee_alfa


def Independence(seq, alfa):
    m = int(len(seq)/8)
    n = int(m / 2)
    cols = [i for i in range(0, 256)]
    labs = [i for i in range(0, 256)]
    df = pd.DataFrame(0, columns=cols, index=labs)

    allbytes = []
    for i in range(0, 256):
        var = bin(i).replace("0b", "")
        if len(var) < 8:
            var = (8 - len(var))*'0' + var
        allbytes.append(var)

    while (len(seq) % 16) != 0:
        seq.pop()
    i = 0
    while i < len(seq):         #пошук частот біграм байтів
        byte1 = []
        for j in range(0, 8):
            byte1.append(seq[i+j])
        byte1 = str(byte1).replace(",", "")
        byte1 = byte1.replace(" ", "")
        byte1 = byte1.replace("[", "")
        byte1 = byte1.replace("]", "")
        byte1 = int('0b' + byte1, 2)

        byte2 = []
        for j in range(8, 16):
            byte2.append(seq[i+j])
        byte2 = str(byte2).replace(",", "")
        byte2 = byte2.replace(" ", "")
        byte2 = byte2.replace("[", "")
        byte2 = byte2.replace("]", "")
        byte2 = int('0b' + byte2, 2)

        df.iat[byte1, byte2] += 1
        i += 16

    colsum = df.sum(axis=1)
    rowsum = df.sum(axis=0)
    hee = 0
    for i in range(0, 256):
        for j in range(0, 256):
            hee += ((df.iat[i, j]) ** 2) / (colsum[i] * rowsum[j])
    hee = n * (hee - 1)
    if alfa == 0.01:
        alfa = 2.32
    if alfa == 0.1:
        alfa = 1.28
    if alfa == 0.05:
        alfa = 1.64
    hee_alfa = math.sqrt(2) * 255 * alfa + 255 ** 2
    if hee <= hee_alfa:
        return 1, hee, hee_alfa
    else:
        return 0, hee, hee_alfa


def Uniformity(seq, alfa):
    r = 20
    m = int(len(seq)/8)
    m_ = int(m / r)            # r = 25
    cols = [i for i in range(0, 25)]
    labs = [i for i in range(0, 256)]
    df = pd.DataFrame(0, columns=cols, index=labs)

    for i in range(0, r):
        for j in range(0, m_):
            byte = []
            for k in range(0, 8):
                byte.append(seq[8 * i * m_ + 8 * j + k])
            byte = str(byte).replace(",", "")
            byte = byte.replace(" ", "")
            byte = byte.replace("[", "")
            byte = byte.replace("]", "")
            byte = int('0b' + byte, 2)
            df.iat[byte, i] += 1
    hee = 0
    rowsum = df.sum(axis=1)
    for i in range(0, r):
        for j in range(0, 256):
            hee += ((df.iat[j, i]) ** 2) / (m_ * rowsum[i])
    hee = m * (hee - 1)
    if alfa == 0.01:
        alfa = 2.32
    if alfa == 0.1:
        alfa = 1.28
    if alfa == 0.05:
        alfa = 1.64
    hee_alfa = math.sqrt(510*(r-1)) * alfa + 6120
    if hee <= hee_alfa:
        return 1, hee, hee_alfa
    else:
        return 0, hee, hee_alfa



########################################################################   visualization

df_res = pd.DataFrame(columns=['Рівномірність', 'Незалежність', 'Однорідність'],
                  index=['alfa = 0.1', 'alfa = 0.05', 'alfa = 0.01'])

df_hees = pd.DataFrame(columns=['Рівномірність', 'Незалежність', 'Однорідність'],
                  index=['alfa = 0.1', 'alfa = 0.05', 'alfa = 0.01'])

df_hees_alfa = pd.DataFrame(columns=['Рівномірність', 'Незалежність', 'Однорідність'],
                  index=['alfa = 0.1', 'alfa = 0.05', 'alfa = 0.01'])

df_time = pd.DataFrame(columns=['Рівномірність', 'Незалежність', 'Однорідність'],
                  index=['alfa = 0.1', 'alfa = 0.05', 'alfa = 0.01'])


def cleanupdf():
    df_res[:] = pd.DataFrame(0, columns=df_res.columns, index=df_res.index)
    df_time[:] = pd.DataFrame(0, columns=df_res.columns, index=df_res.index)
    df_hees[:] = pd.DataFrame(0, columns=df_res.columns, index=df_res.index)
    df_hees_alfa[:] = pd.DataFrame(0, columns=df_res.columns, index=df_res.index)

def dfs(a):
    df_time.iat[0, 0] = a[9]
    df_time.iat[0, 1] = a[12]
    df_time.iat[0, 2] = a[15]
    df_time.iat[1, 0] = a[10]
    df_time.iat[1, 1] = a[13]
    df_time.iat[1, 2] = a[16]
    df_time.iat[2, 0] = a[11]
    df_time.iat[2, 1] = a[14]
    df_time.iat[2, 2] = a[17]

    df_res.iat[0, 0] = a[0][0]
    df_res.iat[0, 1] = a[3][0]
    df_res.iat[0, 2] = a[6][0]
    df_res.iat[1, 0] = a[1][0]
    df_res.iat[1, 1] = a[4][0]
    df_res.iat[1, 2] = a[7][0]
    df_res.iat[2, 0] = a[2][0]
    df_res.iat[2, 1] = a[5][0]
    df_res.iat[2, 2] = a[8][0]

    df_hees.iat[0, 0] = a[0][1]
    df_hees.iat[0, 1] = a[3][1]
    df_hees.iat[0, 2] = a[6][1]
    df_hees.iat[1, 0] = a[1][1]
    df_hees.iat[1, 1] = a[4][1]
    df_hees.iat[1, 2] = a[7][1]
    df_hees.iat[2, 0] = a[2][1]
    df_hees.iat[2, 1] = a[5][1]
    df_hees.iat[2, 2] = a[8][1]

    df_hees_alfa.iat[0, 0] = a[0][2]
    df_hees_alfa.iat[0, 1] = a[3][2]
    df_hees_alfa.iat[0, 2] = a[6][2]
    df_hees_alfa.iat[1, 0] = a[1][2]
    df_hees_alfa.iat[1, 1] = a[4][2]
    df_hees_alfa.iat[1, 2] = a[7][2]
    df_hees_alfa.iat[2, 0] = a[2][2]
    df_hees_alfa.iat[2, 1] = a[5][2]
    df_hees_alfa.iat[2, 2] = a[8][2]

def Cryterias(seq):
    start_time = datetime.now()
    a1 = Equality(seq, 0.1)
    ta1 = datetime.now() - start_time
    start_time = datetime.now()
    a2 = Equality(seq, 0.05)
    ta2 = datetime.now() - start_time
    start_time = datetime.now()
    a3 = Equality(seq, 0.01)
    ta3 = datetime.now() - start_time
    start_time = datetime.now()
    b1 = Independence(seq, 0.1)
    tb1 = datetime.now() - start_time
    start_time = datetime.now()
    b2 = Independence(seq, 0.05)
    tb2 = datetime.now() - start_time
    start_time = datetime.now()
    b3 = Independence(seq, 0.01)
    tb3 = datetime.now() - start_time
    start_time = datetime.now()
    c1 = Uniformity(seq, 0.1)
    tc1 = datetime.now() - start_time
    start_time = datetime.now()
    c2 = Uniformity(seq, 0.05)
    tc2 = datetime.now() - start_time
    start_time = datetime.now()
    c3 = Uniformity(seq, 0.01)
    tc3 = datetime.now() - start_time
    a = [a1, a2, a3, b1, b2, b3, c1, c2, c3, ta1, ta2, ta3, tb1, tb2, tb3, tc1, tc2, tc3]
    return a

def showcase():
    print('\n\nTable of results(1 if the sequence passed the criterion, otherwise 0)')
    print(df_res)
    print('\nTable of the time spent to find the criterion:')
    print(df_time)
    print('\nTable of Хі_Square values:')
    print(df_hees)
    print('\nTable of Хі_Alpha_Square values:')
    print(df_hees_alfa)
    print('\n')

def cleanupstr(lst):
    lst = str(lst)
    lst = lst.replace(",", "")
    lst = lst.replace(" ", "")
    lst = lst.replace("[", "")
    lst = lst.replace("]", "")
    return lst

def SeqToTxt(seq):
    seq = cleanupstr(seq)
    txt = open('seq.txt', 'w')
    txt.write(seq)

print('Congratulations! To start work, enter `1`')
continuer = input()
while continuer != 0:
    print('Choose exactly which sequence you want to check for quality criteria:\n'
          '1) automatically generated by the program - enter 1\n'
          '2) from an external text file - enter 2\n')

    continuer = int(input())

    print('Enter the desired sequence length as a decimal integer')
    length = int(input())

    if continuer == 1:

        print('Choose which algorithm you want to generate the sequence:\n'
              '1) LehmerLow - enter 1\n'
              '2) LehmerHigh - enter 2\n'
              '3) L20 - enter 3\n'
              '4) L89 - enter 4\n'
              '5) Geffe - enter 5\n'
              '6) Librarian - enter 6\n'
              '7) Volfram - enter 7\n'
              '8) Blum-Mikali-bits - enter 8\n'
              '9) Blum-Mikali-bytes - enter 9\n'
              '10) BBS-bits - enter 10\n'
              '11) BBS-bytes - enter 11\n'
              )

        alg_numb = int(input())

        if alg_numb == 1:
            aa = lehmer(length, 'lov')
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 2:
            aa = lehmer(length, 'high')
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 3:
            aa = L20(length)
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 4:
            aa = L89(length)
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 5:
            aa = Geffe(length)
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 6:
            print('\nPay attention! The algorithm can create sequences only from letters of the Latin alphabet.'
                  'enter the name of the text file without .txt\n')
            text = str(input())
            text = open(text + '.txt', 'r')
            text = str(text.read())
            a = Cryterias(Librarian(length, text))
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 7:
            aa = Volfram(length)
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 8:
            aa = BM(length, 'bit')
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 9:
            aa = BM(length, 'byte')
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 10:
            aa = BBS(length, 'bit')
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()

        if alg_numb == 11:
            aa = BBS(length, 'byte')
            SeqToTxt(aa)
            a = Cryterias(aa)
            dfs(a)
            showcase()
            cleanupdf()


    if continuer == 2:
        print('enter the name of the text file without the suffix .txt\n'
              '! Note: The file must be in the same folder as the program !')

        text = str(input())
        text = open(text + '.txt', 'r')
        text = list(text.read())
        i = 0
        if length > len(text):
            print('Error! A sequence of length', len(text), 'does not contain the desired number of bits:', length)
            break
        while i < length:
            while text[i] != '0' and text[i] != '1':
                text.pop(i)
                i -=1
            if length > len(text):
                print('Error! A sequence of length', len(text), 'does not contain the desired number of bits:', length)
                break
            text[i] = int(text[i])
            i += 1

        a = Cryterias(text)
        dfs(a)
        showcase()
        cleanupdf()

    print('\nDo you want to continue the algorithm? If so, then enter 1, if not, then 0')
    continuer = int(input())
    print('-----------------------------------------------------------------\n')

# start_time = datetime.now()
# lehmer(1000000, 'low')
# print(datetime.now() - start_time, "lehmer(1000000, 'low')")
# start_time = datetime.now()
#
# lehmer(1000000, 'high')
# print(datetime.now() - start_time, "lehmer(1000000, 'high')")
# start_time = datetime.now()
#
# L20(1000000)
# print(datetime.now() - start_time, "L20(1000000)")
# start_time = datetime.now()
#
# L89(1000000)
# print(datetime.now() - start_time, "L89(1000000)")
# start_time = datetime.now()
#
# Geffe(1000000)
# print(datetime.now() - start_time, "Geffe(1000000)")
# start_time = datetime.now()
#
# Volfram(1000000)
# print(datetime.now() - start_time, "Volfram(1000000)")
# start_time = datetime.now()
#
# BM(1000000, 'bit')
# print(datetime.now() - start_time, "BM(1000000, 'bit')")
# start_time = datetime.now()
#
# BM(1000000, 'byte')
# print(datetime.now() - start_time, "BM(1000000, 'byte')")
#
# BBS(1000000, 'bit')
# print(datetime.now() - start_time, "BBS(1000000, 'bit')")
# start_time = datetime.now()
#
# BBS(1000000, 'byte')
# print(datetime.now() - start_time, "BBS(1000000, 'byte')")

# start_time = datetime.now()
# a = open('2mb.txt', 'r')
# a = a.read()
# a = Librarian(1000000, a)
# print(len(a), type(a), type(a[0]), a[:10])
# print(datetime.now() - start_time, "Librarian")
# a = Cryterias(a)
# dfs(a)
# showcase()
# cleanupdf()