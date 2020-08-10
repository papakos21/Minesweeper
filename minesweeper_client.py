import requests

r = requests.get('http://localhost:8000/get_tile/0/0')
print(r.status_code)
print(r.text)