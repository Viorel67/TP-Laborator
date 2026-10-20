def tip_real(cale):
    cap = open(cale, "rb").read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return "necunoscut"


print("foto.jpg:", tip_real("probe/foto.jpg"))
print("ascuns.png:", tip_real("probe/ascuns.png"))


# B2 - strings din fisier binar
import re

date = open("probe/ascuns.png", "rb").read()

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())
# B3 - EXIF si GPS
from PIL import Image
from PIL.ExifTags import TAGS

exif = Image.open("probe/foto.jpg")._getexif() or {}

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps = exif.get(34853)

if gps:
    lat = gps[2]
    lon = gps[4]

    lat_zec = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / 3600
    lon_zec = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / 3600

    if gps[1] == "S":
        lat_zec = -lat_zec

    if gps[3] == "W":
        lon_zec = -lon_zec

    print("GPS:", lat_zec, lon_zec)
# B4 - file carving
date = open("probe/ascuns.png", "rb").read()

i = date.find(b"PK\x03\x04")

if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)
# B5 - ascundere mesaj prin LSB
from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())

mesaj = b"FLAG{ascuns_in_pixeli}\x00"
biti = "".join(f"{x:08b}" for x in mesaj)

px_nou = []
i = 0

for r, g, b in px:
    canale = [r, g, b]

    for j in range(3):
        if i < len(biti):
            canale[j] = (canale[j] & ~1) | int(biti[i])
            i += 1

    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")

print("mesaj ascuns in stego.png")
# B6 - dezvaluirea mesajului LSB
px = list(Image.open("stego.png").convert("RGB").getdata())

biti = ""

for r, g, b in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

mesaj_extras = bytearray()

for i in range(0, len(biti), 8):
    octet = biti[i:i+8]

    if len(octet) < 8:
        break

    valoare = int(octet, 2)

    if valoare == 0:
        break

    mesaj_extras.append(valoare)

print("mesaj extras:", mesaj_extras.decode())
