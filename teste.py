import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzcyMTkzNjE1fQ.bovkpE0GhSoD0c9w-YOH7Z3rZmzKDCfF7Etg53C07dc"
}
requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)

print(requisicao)
print(requisicao.json)