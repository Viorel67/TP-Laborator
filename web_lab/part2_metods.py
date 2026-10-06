# Laborator: funcții, metode și importuri pe web
# Student: Ovas Viorel

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercițiul 9

response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Status code:", response.status_code)   # atribut
print("OK:", response.ok)                     # atribut
print("URL:", response.url)                   # atribut
print("Encoding:", response.encoding)         # atribut


# Exercițiul 10

try:
    response.raise_for_status()
    print("Pagina principală nu are erori HTTP.")
except requests.HTTPError as e:
    print("Eroare HTTP:", e)

time.sleep(1)

try:
    bad_response = requests.get(
        BASE_URL + "/this-page-does-not-exist",
        timeout=TIMEOUT
    )
    bad_response.raise_for_status()

except requests.HTTPError:
    print("Pagina cerută nu există sau a apărut o eroare HTTP.")


# Exercițiul 11

print("\nToate antetele:")

for name, value in response.headers.items():
    print(f"{name}: {value}")


# Exercițiul 12

server = response.headers.get("Server", "lipsește")
content_type = response.headers.get("Content-Type", "lipsește")
content_type_lower = response.headers.get("content-type", "lipsește")

print("\nServer:", server)
print("Content-Type:", content_type)
print("content-type:", content_type_lower)

# Observație:
# Dicționarul de antete HTTP din requests nu ține cont de litere mari/mici.


# Exercițiul 13

cyber_count = response.text.lower().count("cyber")

print("\nNumărul aparițiilor cuvântului 'cyber':", cyber_count)

# Putem înlănțui metodele deoarece lower() returnează un șir,
# iar pe acel șir putem apela imediat metoda count().


# Exercițiul 14

html = response.text

start = html.find("<title>") + len("<title>")
end = html.find("</title>")

if start != -1 and end != -1:
    title = html[start:end].strip()
    print("Titlul paginii:", title)
else:
    print("Titlul nu a fost găsit.")


# Exercițiul 15

lines = html.splitlines()

print("\nNumăr de linii HTML:", len(lines))

if lines:
    longest_line = max(lines, key=len)
    print("Lungimea celei mai lungi linii:", len(longest_line))
else:
    print("Pagina nu conține linii.")


# Exercițiul 16

if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")


# Exercițiul 17

time.sleep(1)

redirect_response = requests.get(
    "http://cybercor.org",
    timeout=TIMEOUT
)

print("\nRedirecționări:")

if redirect_response.history:
    for redirect in redirect_response.history:
        print(redirect.status_code, "->", redirect.url)
else:
    print("Nu au existat redirecționări.")

print("URL final:", redirect_response.url)


# Exercițiul 18

time.sleep(1)

head_response = requests.head(
    BASE_URL,
    timeout=TIMEOUT
)

time.sleep(1)

get_response = requests.get(
    BASE_URL,
    timeout=TIMEOUT
)

print("\nHEAD content length:", len(head_response.content))
print("GET content length:", len(get_response.content))

# HEAD returnează în principal antetele răspunsului,
# fără corpul complet al paginii.
# GET returnează și conținutul paginii.


# Exercițiul 19

print("\nCookie-uri:")

if response.cookies:
    for cookie in response.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat")


# Exercițiul 20

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-Ovas-Viorel"
})

time.sleep(1)

session_response = session.get(
    ECHO_URL + "/headers",
    timeout=TIMEOUT
)

print("\nRăspuns de la httpbin:")
print(session_response.text)

# response.text este un atribut și conține corpul ca text.
# response.json() este o metodă și transformă JSON-ul în obiect Python.

try:
    data = session_response.json()

    print("\nUser-Agent trimis:")
    print(data["headers"].get("User-Agent", "lipsește"))

except requests.JSONDecodeError:
    print("Răspunsul nu este JSON valid.")
