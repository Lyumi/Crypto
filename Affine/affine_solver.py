from collections import Counter
import re


def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def list2int(str):
    arr = []

    for chr in str:
        if chr == ' ':
            arr.append(26)
        elif chr == ',':
            arr.append(27)
        elif chr == '.':
            arr.append(28)
        else:
            arr.append(ord(chr)-0x41)
    return arr

def int2list(arr):
    result = ''
    for i in arr:
        if i == 26:
            result+=' '
        elif i == 27:
            result+=','
        elif i == 28:
            result+='.'
        else:
            result+=chr(i+0x41)
    return result

def decrypt(arr, a,b):
    list = []
    for x in range(len(arr)):
        list.append(modinv(a,29)*(arr[x]-b)%29)
    return int2list(list)

encrypted = open('input.text','r').readline()

list = list2int(encrypted)
print(list)

res = []
for a in range(1, 29):
    for b in range(1, 29):
        for i in range(len(list)):
            res = decrypt(list, a, b)

        if res.find("SOLUTION") > 0:
            print('Decrpyted!')
            print(' ')
            print(int2list(list))
        else:
            print('('+str(a)+','+str(b)+') '+'wrong!')
