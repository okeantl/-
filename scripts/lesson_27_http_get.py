import requests

URL = "https://httpbin.org/get"

response = requests.get(URL)

status = response.status_code
content_type = response.headers["Content-Type"]
url_from_body = response.json()["url"]

print(f"Статус: {status}")
print(f"Content-Type: {content_type}")
print(f"URL из тела: {url_from_body}")
