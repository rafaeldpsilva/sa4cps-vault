import requests

url = "http://192.168.2.91:3456/api/v1"
token = "tk_a3f9c49bdc19b5fc164ce95e4df6f6df8374f568"

headers = {
    "Authorization": f"Bearer {token}"
}

try:
    response = requests.get(f"{url}/projects", headers=headers)
    print("Status code:", response.status_code)
    print("Projects:", response.json())
except Exception as e:
    print(e)
