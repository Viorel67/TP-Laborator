# Laborator: funcții, metode și importuri pe web
# Student: Ovas Viorel

import argparse
import csv

from datetime import datetime

from webtools import (
    get_title,
    security_headers,
    fetch,
    check_paths,
    site_report,
    DEFAULT_HEADERS
)


# Exercițiul 44

BASE_URL = "https://cybercor.org"

response = fetch(BASE_URL)

print(
    "Exercițiul 44:",
    get_title(response.text)
)


# Exercițiul 45

# Am importat direct get_title și security_headers.
# Dacă main.py ar avea și o funcție proprie numită get_title,
# numele definit ulterior ar putea înlocui numele importat.


# Exercițiul 47

print(
    "Exercițiul 47 DEFAULT_HEADERS:",
    DEFAULT_HEADERS
)


# Exercițiul 48

parser = argparse.ArgumentParser(
    description="Generează un raport despre un site web."
)

parser.add_argument(
    "url",
    help="URL-ul site-ului analizat"
)

args = parser.parse_args()

url = args.url


# Exercițiul 49

paths = [
    "/",
    "/robots.txt",
    "/sitemap.xml"
]

results = check_paths(
    url.rstrip("/"),
    paths
)

with open(
    "report.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "path",
        "status",
        "checked_at"
    ])

    for path, status in results.items():
        writer.writerow([
            path,
            status,
            datetime.now().isoformat()
        ])

print("Salvat în report.csv")


# Exercițiul 50

site_report(url)
