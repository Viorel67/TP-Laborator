
from checker import (
    SITES,
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check
)

print("=== PARTEA 1 ===")
print("build_url 1:", build_url("example.com", "login"))
print("build_url 2:", build_url("example.com", "/login"))
print("is_https 1:", is_https(SITES[0]))
print("is_https 2:", is_https("http://example.com"))

print("\n=== PARTEA 2 ===")
print("show_response 1:")
show_response(SITES[0])
print("show_response 2:")
show_response(SITES[9])

print("\n=== PARTEA 3 ===")
print("check_site 1:", check_site(SITES[0]))
print("check_site 2:", check_site(SITES[9]))

print("\n=== PARTEA 4 ===")
scan_sites()

print("\n=== PARTEA 5 ===")
print("check_headers 1:", check_headers(SITES[10]))
print("check_headers 2:", check_headers(SITES[9]))
print("check_headers 3:", check_headers(SITES[11]))

print("\n=== PARTEA 6 ===")
print("retry_check 1:", retry_check(SITES[3]))
print("retry_check 2:", retry_check(SITES[6]))
print("retry_check 3:", retry_check(SITES[7], attempts=2))
print("retry_check 4:", retry_check(SITES[9]))
