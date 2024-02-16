import requests
from secure_token import SecureToken as sc
from urllib.parse import quote

url = "http://127.0.0.1:5000/api/"
responseofprivate = requests.get(url + 'private_method/' + quote('hello to all'))

if responseofprivate.status_code == 200:
    data = responseofprivate.json()  # Assuming the response is in JSON format
    print(data)
else:
    print("Failed to fetch data. Status code:", responseofprivate.status_code)
    login_response = requests.post(
        url + 'login', 
        data={'credentials': sc.tokenencrypt('test:testuserps')}
    )
    if(login_response.status_code == 200):
        token = login_response.json()['msg']
        responseofprivate = requests.get(
            url + 'private_method/' + quote('hello to all'),
            headers={'Authorization': f"Bearer {token}"}
        )
        if(responseofprivate.status_code == 200):
            data = responseofprivate.json()['msg']
            print(f'identity: {data["identity"]} \nparam1: {data["param1"]}')
        else:
            print('failed')
