# Laborator: funcții, metode și importuri pe web
# Student: Ovas Viorel

import urllib.request
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercițiul 1

print("Versiune requests:", requests.__version__)

# requests este o bibliotecă externă și trebuie instalată cu pip.
# urllib face parte din biblioteca standard Python și este inclusă
# automat atunci când instalăm Python.


# Exercițiul 2

res1 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Stil 1 Status Code:", res1.status_code)

time.sleep(1)

from requests import get

res2 = get(BASE_URL, timeout=TIMEOUT)
print("Stil 2 Status Code:", res2.status_code)

# Avantaj import requests:
# Este mai clar din ce modul provine funcția get.

# Avantaj from requests import get:
# Codul este mai scurt și putem scrie direct get().


# Exercițiul 3

import requests as rq

time.sleep(1)

res3 = rq.get(BASE_URL, timeout=TIMEOUT)
print("Alias Status Code:", res3.status_code)

# Aliasul este util când numele modulului este lung și este folosit des.
# Aliasul poate face codul mai greu de citit dacă numele ales nu este clar.


# Exercițiul 4

time.sleep(1)

request = urllib.request.Request(
    BASE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
    status = response.status
    body = response.read().decode("utf-8")

    print("Urllib Status:", status)
    print("Primele 200 de caractere:")
    print(body[:200])



# Exercițiul 5

print("\nConținutul modulului requests:")
print(dir(requests))

# Exemple din requests:
# get - funcție
# Session - clasă
# exceptions - modul


# Exercițiul 6

print("\nAjutor pentru requests.get:")
help(requests.get)

time.sleep(1)

res6 = requests.get(BASE_URL, timeout=TIMEOUT)

print("Exercițiul 6 Status:", res6.status_code)

# Parametrul timeout stabilește timpul maxim de așteptare al cererii.


# Exercițiul 7

time.sleep(1)

start = time.perf_counter()

res_time = requests.get(BASE_URL, timeout=TIMEOUT)

end = time.perf_counter()

manual_time = end - start
server_time = res_time.elapsed.total_seconds()

print("Timp măsurat manual:", round(manual_time, 4), "secunde")
print("response.elapsed:", round(server_time, 4), "secunde")

# time.perf_counter() măsoară timpul total observat de program,
# iar response.elapsed măsoară timpul cererii HTTP.


# Exercițiul 8
try:
    import bs4
    print("Modulul bs4 este instalat.")

except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4") 

