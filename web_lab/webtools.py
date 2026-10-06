# Laborator: funcții, metode și importuri pe web
# Student: Ovas Viorel

import requests
import time
import re
import socket
import ssl
import json

from urllib.parse import urlparse, urljoin
from datetime import datetime

TIMEOUT = 10

DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Ovas-Viorel"
}

# Exercițiul 44

def fetch(url, timeout=TIMEOUT):
    """Returnează răspunsul HTTP pentru URL-ul primit."""
    return requests.get(
        url,
        headers=DEFAULT_HEADERS,
        timeout=timeout
    )


def get_status(url):
    """Returnează codul de stare HTTP."""
    return fetch(url).status_code


def get_title(html):
    """Returnează titlul unei pagini HTML."""
    start = html.find("<title>")
    end = html.find("</title>")

    if start == -1 or end == -1:
        return None

    start += len("<title>")

    return html[start:end].strip()


def security_headers(url):
    """Verifică antetele de securitate ale paginii."""
    response = fetch(url)

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


# Exercițiul 49

def check_paths(base, paths):
    """Returnează statusurile HTTP pentru căile primite."""
    results = {}

    for path in paths:
        try:
            response = fetch(base + path)
            results[path] = response.status_code
        except requests.RequestException:
            results[path] = None

        time.sleep(1)

    return results


def score_headers(results):
    """Returnează scorul antetelor de securitate."""
    present = sum(results.values())
    total = len(results)

    return f"{present}/{total}"


def fetch_robots(base):
    """Returnează conținutul robots.txt sau None."""
    try:
        response = fetch(base + "/robots.txt")

        if response.status_code == 200:
            return response.text

        return None

    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Extrage valorile Disallow din robots.txt."""
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


def extract_links(html):
    """Extrage toate linkurile href fără duplicate."""
    links = re.findall(r'href="([^"]+)"', html)

    return list(dict.fromkeys(links))


def split_links(links, base_url):
    """Separă linkurile interne și externe."""
    internal = []
    external = []

    domain = urlparse(base_url).netloc

    for link in links:
        full_url = urljoin(base_url, link)
        link_domain = urlparse(full_url).netloc

        if link_domain == domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


def resolve(hostname):
    """Returnează adresa IP a unui hostname."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname):
    """Returnează câte zile mai sunt până la expirarea certificatului."""

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

    expiration_seconds = ssl.cert_time_to_seconds(expiration)

    expiration_date = datetime.fromtimestamp(expiration_seconds)

    now = datetime.now()

    return (expiration_date - now).days


def redirect_chain(url):
    """Returnează lanțul de redirecționări de la HTTP la URL-ul final."""

    parsed = urlparse(url)

    http_url = "http://" + parsed.netloc

    response = requests.get(
        http_url,
        headers=DEFAULT_HEADERS,
        timeout=TIMEOUT
    )

    redirects = []

    for item in response.history:
        redirects.append({
            "status": item.status_code,
            "url": item.url
        })

    return redirects, response.url


# Exercițiul 50

def site_report(url):
    """Generează și salvează raportul complet al site-ului."""

    response = fetch(url)

    status = response.status_code
    final_url = response.url
    title = get_title(response.text)

    hostname = urlparse(final_url).netloc

    ip_address = resolve(hostname)

    redirects, redirect_final_url = redirect_chain(url)

    security = security_headers(final_url)
    security_score = score_headers(security)

    certificate_days = cert_days_left(hostname)

    links = extract_links(response.text)

    internal, external = split_links(
        links,
        final_url
    )

    base = f"{urlparse(final_url).scheme}://{hostname}"

    robots_text = fetch_robots(base)

    disallowed = disallowed_paths(robots_text)

    report = {
        "url": url,
        "status_code": status,
        "final_url": final_url,
        "title": title,
        "ip_address": ip_address,
        "redirects": redirects,
        "redirect_final_url": redirect_final_url,
        "security_headers": security,
        "security_score": security_score,
        "certificate_days_left": certificate_days,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": disallowed
    }

    print()
    print("=== Raport site:", url, "===")
    print("Cod de stare:", status)
    print("URL final:", final_url)
    print("Titlu:", title)
    print("Adresă IP:", ip_address)

    print("Redirecționări:")

    if redirects:
        for redirect in redirects:
            print(
                redirect["status"],
                "->",
                redirect["url"]
            )
    else:
        print("Nicio redirecționare")

    print("Scor securitate:", security_score)

    print(
        "Certificat:",
        certificate_days,
        "zile rămase"
    )

    print(
        "Legături:",
        len(internal),
        "interne,",
        len(external),
        "externe"
    )

    if disallowed:
        print(
            "Căi interzise:",
            ", ".join(disallowed)
        )
    else:
        print("Căi interzise: niciuna")

    with open(
        "report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("Salvat în report.json")

    return report


# Exercițiul 46

if __name__ == "__main__":
    print(
        "Autotest:",
        get_status("https://cybercor.org")
    )
