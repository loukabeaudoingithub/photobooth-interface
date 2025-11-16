import requests

res = requests.post("http://localhost:5001/take-photo?group=Test&index=1")
print(res.status_code)
print(res.text)