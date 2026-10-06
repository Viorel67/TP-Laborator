# Laborator: funcții, metode și importuri pe web
# Student: Ovas Viorel

import requests
import time
import re
import hashlib
import json
import socket
import ssl

from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from datetime import datetime


BASE_URL = "https://cybercor.org"
TIMEOUT = 10


# Exercițiul 35

def parse_url(url):
    """Descompune un URL și afișează componentele lui."""
    parsed = urlparse(url)

    print("Scheme:", parsed.scheme)
    print("Netloc:", parsed.netloc)
    print("Path:", parsed.path)
    print("Query:", parsed.query)
    print("Fragment:", parsed.fragment)


parse_url("https://cybercor.org/path?x=1#top")


# Exercițiul 36

def build_urls(base, links):
    """Transformă linkurile relative în URL-uri complete."""
    for link in links:
        print(link, "->", urljoin(base, link))


links = [
    "/about",
    "contact.html",
    "../index.html"
]

build_urls(BASE_URL, links)


# Exercițiul 37

def extract_links(html):
    """Extrage toate linkurile href fără duplicate."""
    links = re.findall(r'href="([^"]+)"', html)

    return list(dict.fromkeys(links))


response = requests.get(BASE_URL, timeout=TIMEOUT)

links = extract_links(response.text)

print("Exercițiul 37:")
print("Număr linkuri găsite:", len(links))

for link in links:
    print(link)


# Exercițiul 38

def split_links(links, domain):
    """Separă linkurile interne de cele externe."""
    internal = []
    external = []

    for link in links:
        full_url = urljoin(BASE_URL, link)
        link_domain = urlparse(full_url).netloc

        if link_domain == domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


domain = urlparse(BASE_URL).netloc

internal, external = split_links(links, domain)

print("Exercițiul 38:")
print("Linkuri interne:", len(internal))
print("Linkuri externe:", len(external))


# Exercițiul 39

class ImageFinder(HTMLParser):
    """Parser HTML care găsește sursele imaginilor."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src:
                self.images.append(src)


test_html = """
<html><body>
<img src="/logo.png" alt="Logo">
<IMG SRC="poza.jpg">
<img alt="imagine fără src">
<img src="https://cdn.example.com/banner.webp" />
<a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)

print("Exercițiul 39 test:")
print(finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
], "Parserul nu a găsit exact imaginile așteptate"

print("Testul a trecut!")

time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

finder = ImageFinder()
finder.feed(response.text)

print(len(finder.images), "imagini găsite")

for src in finder.images:
    print(src)

print(
    "Număr tag-uri img:",
    response.text.lower().count("<img")
)


# Exercițiul 40

def page_fingerprint(url):
    """Returnează hash-ul SHA-256 al conținutului paginii."""
    response = requests.get(url, timeout=TIMEOUT)

    return hashlib.sha256(
        response.content
    ).hexdigest()


fingerprint1 = page_fingerprint(BASE_URL)

time.sleep(1)

fingerprint2 = page_fingerprint(BASE_URL)

print("Exercițiul 40:")
print("Hash 1:", fingerprint1)
print("Hash 2:", fingerprint2)

if fingerprint1 == fingerprint2:
    print("Paginile sunt identice.")
else:
    print("Conținutul paginii s-a schimbat.")


# Exercițiul 41

def save_headers(url):
    """Salvează antetele HTTP în headers.json și le încarcă din nou."""
    response = requests.get(url, timeout=TIMEOUT)

    with open("headers.json", "w") as file:
        json.dump(
            dict(response.headers),
            file,
            indent=2
        )

    with open("headers.json", "r") as file:
        data = json.load(file)

    print("Server:", data.get("Server", "lipsește"))


print("Exercițiul 41:")
save_headers(BASE_URL)


# Exercițiul 42

def resolve(hostname):
    """Returnează adresa IP asociată unui hostname."""
    return socket.gethostbyname(hostname)


print(
    "Exercițiul 42:",
    resolve("cybercor.org")
)


# Exercițiul 43

def cert_days_left(hostname):
    """Returnează numărul de zile până la expirarea certificatului SSL."""

    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443),
        timeout=TIMEOUT
    ) as sock:

        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_socket:

            certificate = secure_socket.getpeercert()

    expiration = certificate["notAfter"]

    expiration_seconds = ssl.cert_time_to_seconds(
        expiration
    )

    expiration_date = datetime.fromtimestamp(
        expiration_seconds
    )

    now = datetime.now()

    days_left = (expiration_date - now).days

    return days_left


print(
    "Exercițiul 43:",
    cert_days_left("cybercor.org"),
    "zile rămase"
)
