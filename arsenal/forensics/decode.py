import re
import base64
from urllib.parse import unquote


# A1 - text si bytes
s = "Salut"
b = s.encode()

print(b, b[0])
print(b.hex())

refacut = bytes.fromhex(b.hex())
print(refacut)


# A2 - recunoasterea stratului
def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if len(s) % 2 == 0 and re.fullmatch(r"[0-9A-Fa-f]+", s):
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"

    return "necunoscut"


print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))


# A3 - decodarea stratului
def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)

    elif strat == "hex":
        rezultat = bytes.fromhex(s)

    elif strat == "url":
        rezultat = unquote(s).encode()

    else:
        rezultat = s.encode()

    return strat, rezultat


print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("%2Fetc"))


# A4 - mai multe straturi
def citibil(b):
    return all(32 <= c < 127 for c in b)


val = open("probe/mesaj.txt").read().strip()
for _ in range(8):
    strat, b = desfa(val)
    print("strat:", strat, "->", b)

    try:
        text = b.decode()
    except UnicodeDecodeError:
        break

    urmatorul_strat = ghici_strat(text)

    if urmatorul_strat == "necunoscut":
        if citibil(b):
            print("rezultat final:", text)
        break

    val = text





# A5 - XOR brute force
date = open("probe/xor.bin", "rb").read()

for k in range(256):
    clar = bytes(b ^ k for b in date)

    if citibil(clar):
        text = clar.decode()

        if "FLAG{" in text:
            print("cheie:", k, text)
            break
# A6 - spargerea hash-ului prin dictionar
import hashlib

tinta = open("probe/hashuri.txt").readline().strip()

print("lungime hash:", len(tinta))

for cuv in open("probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()

    if len(tinta) == 32:
        calculat = hashlib.md5(cuv.encode()).hexdigest()
    elif len(tinta) == 40:
        calculat = hashlib.sha1(cuv.encode()).hexdigest()
    elif len(tinta) == 64:
        calculat = hashlib.sha256(cuv.encode()).hexdigest()
    else:
        print("Algoritm necunoscut")
        break

    if calculat == tinta:
        print("parola gasita:", cuv)
        break
# A7 - argparse si fisa JSON
import argparse
import json

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        intrare = open(a.intrare, "r").read().strip()
    else:
        intrare = a.intrare

    strat, rezultat = desfa(intrare)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode(errors="replace")
    }

    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump(fisa, f, indent=4)

    print("fisa.json a fost salvata")
