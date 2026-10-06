# Laborator: funcții, metode și importuri pe web
# Student: Ovas Viorel

import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


# Exercițiul 21

def fetch(url):
    """Returnează obiectul răspuns pentru URL-ul primit."""
    return requests.get(url, timeout=TIMEOUT)

response = fetch(BASE_URL)
print("Exercițiul 21:", response.status_code)


# Exercițiul 22

def get_status(url):
    """Returnează codul de stare HTTP pentru URL-ul primit."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

paths = ["/", "/robots.txt", "/sitemap.xml"]

for path in paths:
    print("Exercițiul 22:", path, get_status(BASE_URL + path))
    time.sleep(1)


# Exercițiul 23

def fetch(url, timeout=10):
    """Returnează răspunsul HTTP, folosind un timeout configurabil."""
    return requests.get(url, timeout=timeout)

print("Exercițiul 23 implicit:", fetch(BASE_URL).status_code)
time.sleep(1)
print("Exercițiul 23 timeout=3:", fetch(BASE_URL, timeout=3).status_code)


# Exercițiul 24

def get_title(html):
    """Returnează titlul unei pagini HTML."""
    start = html.find("<title>")
    end = html.find("</title>")

    if start == -1 or end == -1:
        return None

    start += len("<title>")
    return html[start:end].strip()

html = fetch(BASE_URL).text
print("Exercițiul 24:", get_title(html))


# Exercițiul 25

help(get_title)


# Exercițiul 26

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

try:
    print("Exercițiul 26:", get_status(123))
except Exception as e:
    print("Exercițiul 26 eroare:", type(e).__name__)

# Adnotările de tip nu opresc automat folosirea unui tip greșit.
# Ele sunt informații pentru programator și pentru instrumente de analiză.


# Exercițiul 27

def page_exists(url):
    """Returnează True dacă pagina poate fi accesată, altfel False."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

print("Exercițiul 27 valid:", page_exists(BASE_URL))
print(
    "Exercițiul 27 invalid:",
    page_exists("https://this-domain-does-not-exist.invalid")
)


# Exercițiul 28

def check_paths(base, paths):
    """Returnează un dicționar cu statusurile HTTP pentru căile primite."""
    results = {}

    for path in paths:
        try:
            response = requests.get(base + path, timeout=TIMEOUT)
            results[path] = response.status_code
        except requests.RequestException:
            results[path] = None

        time.sleep(1)

    return results

paths = ["/", "/robots.txt", "/sitemap.xml"]
print("Exercițiul 28:", check_paths(BASE_URL, paths))


# Exercițiul 29

def get_header(url, name, default="lipsește"):
    """Returnează valoarea unui antet HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)

print(
    "Exercițiul 29:",
    get_header(BASE_URL, name="Server")
)


# Exercițiul 30

def security_headers(url):
    """Verifică prezența principalelor antete de securitate."""
    response = requests.get(url, timeout=TIMEOUT)

    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    results = {}

    for header in headers_to_check:
        results[header] = header in response.headers

    return results

security_results = security_headers(BASE_URL)
print("Exercițiul 30:", security_results)


# Exercițiul 31

def score_headers(results):
    """Returnează scorul antetelor de securitate sub forma x/y."""
    present = sum(results.values())
    total = len(results)

    return f"{present}/{total}"

print(
    "Exercițiul 31:",
    score_headers(security_headers(BASE_URL))
)


# Exercițiul 32

def fetch_robots(base):
    """Returnează textul robots.txt sau None dacă nu poate fi obținut."""
    try:
        response = requests.get(
            base + "/robots.txt",
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            return response.text

        return None

    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Returnează toate valorile Disallow din robots.txt."""
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()

            if value:
                paths.append(value)

    return paths

robots = fetch_robots(BASE_URL)
print("Exercițiul 32:", disallowed_paths(robots))


# Exercițiul 33

def response_times(*urls):
    """Returnează timpul de răspuns pentru fiecare URL primit."""
    results = {}

    for url in urls:
        start = time.perf_counter()

        try:
            requests.get(url, timeout=TIMEOUT)
            end = time.perf_counter()
            results[url] = end - start

        except requests.RequestException:
            results[url] = None

        time.sleep(1)

    return results

print(
    "Exercițiul 33:",
    response_times(
        BASE_URL,
        BASE_URL + "/robots.txt"
    )
)


# Exercițiul 34

def log(message, **details):
    """Afișează un mesaj urmat de detalii în format nume=valoare."""
    parts = [message]

    for key, value in details.items():
        parts.append(f"{key}={value}")

    print(" | ".join(parts))

log(
    "verificat",
    url=BASE_URL,
    status=200
)

# print() doar afișează o valoare.
# return trimite valoarea înapoi către codul care a apelat funcția.
