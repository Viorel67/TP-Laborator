
from httptools import *

def test(nume, rezultat, asteptat):
    if rezultat == asteptat:
        print("PASS:", nume)
    else:
        print("FAIL:", nume)
        print("Primit:", rezultat)
        print("Asteptat:", asteptat)


# Partea 1
test("search", search({"q": "python"}), {"q": "python"})
test("search_url", search_url({"q": "python"}), BASE + "/get?q=python")

# Partea 2
test("fetch_with_agent", fetch_with_agent("MyBot/1.0"), "MyBot/1.0")
print("Default agent:", default_agent())

# Partea 3
test("post_json", post_json({"name": "Ana"}), {"name": "Ana"})
test("post_form", post_form({"name": "Ana"}), {"name": "Ana"})

# Partea 4
test("status 200", describe_status(200), "succes")
test("status 404", describe_status(404), "eroare client")
test("status 503", describe_status(503), "eroare server")
test("is_ok 204", is_ok(204), True)
test("is_ok 500", is_ok(500), False)

# Partea 5
test("redirects", count_redirects(3), 3)
test("final_url", final_url(2), BASE + "/get")
test("first_hop", first_hop(3), "/relative-redirect/2")

# Partea 6
test("cookie_demo", cookie_demo("theme", "dark"), {"theme": "dark"})
test("no_session_demo", no_session_demo("theme", "dark"), {})

# Partea 7
r = report("/get")
test("report status", r["status"], 200)
test("report redirects", r["redirects"], 0)
test("report content_type", r["content_type"], "application/json")

print("\nTestarea s-a terminat!")
