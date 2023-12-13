import requests


api_server = 'http://localhost:8000/api/v1'


def login():
    # username = input("Username: ").strip()
    # pwd = input("Password: ").strip()
    username = "Lorenzo"
    pwd = "p7Zn#sM#JAfPA@6"

    res = requests.post(url=f'{api_server}/auth/login/', data={'username': username, 'password': pwd})
    if res.status_code != 200:
        return None
    json = res.json()
    return json['key']


def logout(key):
    res = requests.post(url=f'{api_server}/auth/logout/', headers={'Authorization': f'Token {key}'})
    if res.status_code == 200:
        print("Logged out!")
    else:
        print("Log out failed")
    print()


def fetch_articxles(key):
    res = requests.get(url=f'{api_server}/articles/', headers={'Authorization': f'Token {key}'})
    if res.status_code != 200:
        return None
    return res.json()


key = login()
print(key)

if key is not None:
    print(fetch_articxles(key))
    logout(key)



