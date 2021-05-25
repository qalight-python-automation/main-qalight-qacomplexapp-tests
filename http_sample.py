"""Sample HTTP commands"""
import requests

# print("====================Hello=========================")
# # GET hello message
# response = requests.request(method="GET", url='http://0.0.0.0:8083/hello', params={"name": "Drulio"})
# print(response.status_code)
# print(response.text)
# print("="*50)
#
# print("=====================POST /user====================")
# # POST (add) user
# response = requests.request(method="POST", url='http://0.0.0.0:8083/user', data={"name": "Greham", "surname": "Balahov"})
# print(response.status_code)
# print(response.text)
# print("="*50)
#
# print("=====================PUT /user====================")
# # PUT (edit) user
# response = requests.request(method="PUT", url='http://0.0.0.0:8083/user', data={"name": "Greham", "surname": "Crutashov"})
# print(response.status_code)
# print(response.text)
# print(response.reason)
# print("="*50)
#
# print("=====================PUT /user====================")
# # GET user
# response = requests.request(method="GET", url='http://0.0.0.0:8083/user')
# print(response.status_code)
# print(response.text)
# print("="*50)

url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

response = requests.get(url=url)
assert response.status_code == 200
data = response.json()
for currency in data:
    print(f"Course of {currency['ccy']} is {currency['buy']}")
