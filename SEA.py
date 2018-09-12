from sys import argv

LETTER_SIZE = 9


def bit_at_position(integer, position):
    return (integer >> (position)) & 1


def connect_bits(arr):
    result = 0
    for c in arr:
        ic = ord(c)
        result <<= ic.bit_length()
        result |= ic * 0xff
    return result

def encrypt(p, k,offset):
    encrypted = 0
    kl = k.bit_length()
    for i in range(p.bit_length()):
        pb = bit_at_position(p, i)
        kb = bit_at_position(k, (i+offset) % kl) 
        if kb == 0 and pb != kb:
            encrypted += pow(3, i) ^ kb
        elif pb == kb:
            encrypted += pow(3, i) << 1
    return encrypted


def decrypt(c, k,offset):
    decrypted = 0
    encrypted = thr(c)
    kl = k.bit_length()
    for i in range(encrypted.__len__()):
        if encrypted[i] == 2:
            decrypted += bit_at_position(k, (i+offset) % kl) << i
        elif encrypted[i] == 1:
            decrypted += (1 << i) ^ bit_at_position(k, (i+offset) % kl)
    return decrypted


def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]


def encrypt_text(p, k):
    result = []
    kk = connect_bits(k)
    for i in range(p.__len__()):
        enc = thr(encrypt(ord(p[i]), kk,i))
        ext = [0]*(LETTER_SIZE % len(enc))
        enc.extend(ext)
        result.extend(enc)
    return dec(result)


def decrypt_text(c, k):
    result = ""
    kk = connect_bits(k)
    encrypted = chunks(thr(c), LETTER_SIZE)
    for i in range(encrypted.__len__()):
        result += chr(decrypt(dec(encrypted[i]), kk,i))
    return result


def dec(arr):
    result = 0
    for i in range(len(arr)):
        if arr[i] != 0:
            to_add = pow(3, i)
            if arr[i] > 1:
                to_add <<= 1
            result += to_add
    return result


def thr(i):
    result = []
    while i > 0:
        result.append(i % 3)
        i //= 3
    return result


if argv[1] == '-e':
    plain = input("Podaj tekst do zaszyfrowania:\t")
    print(encrypt_text(plain, input("Podaj haslo:\t")))
elif argv[1] == '-d':
    cipher = int(input("Podaj tekst do odszyfrowania:\t"))
    print(decrypt_text(cipher, input("Podaj haslo:\t")))
