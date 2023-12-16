import requests

# Set your Django API base URL
api_base_url = 'http://localhost:8000/api/v1/'

# Replace 'your_username' and 'your_password' with valid credentials
credentials = {'username': 'Lorenzo2', 'password': 'Test_234'}

# Obtain the authentication token
token_response = requests.post(api_base_url + 'auth/login/', data=credentials)
print(token_response)
token = token_response.json().get('key')

# Check if the token was obtained successfully
if token:
    # Set up headers with the authentication token
    headers = {'Authorization': f'Token {token}'}

    # Example: Make a GET request to the MyModel API endpoint
    mymodel_response = requests.get(api_base_url + 'articles/editor/', headers=headers)

    # Check the response
    if mymodel_response.status_code == 200:
        mymodel_data = mymodel_response.json()
        print("MyModel data:", mymodel_data)
    else:
        print("Failed to fetch MyModel data. Status code:", mymodel_response.status_code)
else:
    print("Failed to obtain the authentication token. Status code:", token_response.status_code)
