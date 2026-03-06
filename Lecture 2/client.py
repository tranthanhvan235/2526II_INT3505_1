import requests

url = "http://127.0.0.1:5000/users"

response = requests.get(url)
print("Users:", response.json())

new_user = {"id": 4, "name": "Viet"}
response = requests.post(url, json=new_user)
print(response.json())

response = requests.get(url)
print("Updated users:", response.json())