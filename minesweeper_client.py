import requests

r = requests.get('http://localhost:8000/0/0')
print(r.status_code)
print(r.text)