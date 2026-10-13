import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]
#Partea 1


def build_url(host, path):
    return "https://" + host + "/" + path.lstrip("/")
def is_https(url):
    return url.startswith("https://")

#Partea 2


def show_response(url):
    try:
        response=requests.get(url,timeout=5)
        print("Status:",response.status_code)
        print("Content-Type:",response.headers.get("Content-Type"))
    except requests.exceptions.RequestException as e:
        print("Eroare:",str(e))
#Partea 3



def check_site(url):
    try:
        response=requests.get(url,timeout=5)
     return {
            "status":response.status_code,
            "content_type":response.headers.get("Content-Type"),
            "length":len(response.content),
            "server":response.headers.get("Server", "unknown")        }
    except requests.exceptions.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }


#partea 4

def scan_sites():
    rezultate = []
    for url in SITES:
        rezultat = check_site(url)
        rezultate.append((url, rezultat))
    reusite = []
    for url, rezultat in rezultate:
        if rezultat["status"] == 200:
            reusite.append((url, rezultat))
    reusite.sort(
        key=lambda element: element[1]["length"],
        reverse=True
    )
    for url, rezultat in reusite:
        print(url, "->", rezultat["status"],
              ",", rezultat["length"], "octeti")
    print("Reusite:", len(reusite),
          "| Esuate:", len(rezultate) - len(reusite))


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
