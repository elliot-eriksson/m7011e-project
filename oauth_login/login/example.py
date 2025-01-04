import requests
import json

oauth_server_url = "http://localhost:8000"

# Replace the credentials below with your own

client_id = "Zx6bjPzYlzArXlKhDbIvNWoIk5LsmZVdcXSpBrSV"  # client ID from my app
client_secret = "wPgMorfcpKEdKlClhqoqeGbPAUrNOYjvxnqsH1k1V6FSdJ0H6WJ9LiUNppTi6SdIb8jOCOAOhfMDdFMMg04lvr1uCRCp6Gxr2t4Iy4LXPMXVdIxUOR4hMk5ixXNP5eef"  # client secret from my app
username = "loginExpert"  # my user
password = "login123"  # user's password

# Function to obtain an OAuth token
def get_access_token():
    token_url = f"{oauth_server_url}/oauth/token/"
    data = {"grant_type": "password", "username": username, "password": password}
    auth = (client_id, client_secret)

    # response = requests.post(token_url, data=data, auth=auth)
    # print(f'{token_url, data, auth}')
    # # Define your token URL and data

    # Create a session
    session = requests.Session()

    # Prepare the request
    request = requests.Request('POST', token_url, data=data, auth=auth)
    prepared_request = session.prepare_request(request)

    # Inspect the request
    print("Request URL:", prepared_request.url)
    print("Request Headers:", prepared_request.headers)
    print("Request Body:", prepared_request.body)

    # Send the request
    response = session.send(prepared_request)

    # Print the response
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)
# Function to make an authenticated API request

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        print(f"Failed to obtain access token. Status code: {response.status_code}")
        print(response.text)
        return None


def make_authenticated_api_request(access_token):
    api_url = f"{oauth_server_url}/api/users/"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to make the API request. Status code: {response.status_code}")
        print(response.text)
        return None

# Obtain an OAuth token
access_token = get_access_token()
if access_token == None:
    # Make an authenticated API request
    print(f"Failed to make the API request. Status code: ")
api_response = make_authenticated_api_request(access_token)
if api_response:
    print("API Response:")
    print(json.dumps(api_response, indent=4))