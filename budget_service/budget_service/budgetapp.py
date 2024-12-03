# Copyright [2021] [FORTH-ICS]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.parse import urljoin
#import jwt

from requests import HTTPError
from django.contrib.auth.models import User
from social_core.backends.oauth import BaseOAuth2
from .settings import SOCIAL_AUTH_CLIENTAPP_KEY, SOCIAL_AUTH_CLIENTAPP_SECRET
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient


class BudgetappOAuth2(BaseOAuth2):
    """Custom Django OAuth authentication backend"""
    name = 'budgetapp'
    AUTHORIZATION_URL = 'http:///127.0.0.1:8001/oauth/authorize/'
    ACCESS_TOKEN_URL = 'http:///127.0.0.1:8001/oauth/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    REDIRECT_STATE = False
    STATE_PARAMETER = True
    SEND_USER_AGENT = True
    ID_KEY="id"

    def get_user_details(self, response):
            print("get_user_details")
            """Return user details from my provider account"""
            return response


    def user_data(self, access_token, *args, **kwargs):
        print("user_data")
        return self.get_json('http://127.0.0.1:8001/api/userinfo/', headers={
            'Authorization': 'Bearer ' + access_token
        })
    
    def authenticate(self, request):
        """Override the authenticate method to send requests to the auth server"""
        print("authenticate")
        username = request.data.get('username')
        password = request.data.get('password')
        # Check if credentials are provided
        if not username or not password:
            return None

        # Send the POST request to get the access token
        oauth_session = OAuth2Session(client=WebApplicationClient(client_id=SOCIAL_AUTH_CLIENTAPP_KEY))
        token_response = oauth_session.post(
            self.ACCESS_TOKEN_URL,
            data={'grant_type': 'password', 'username': username, 'password': password},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            verify=False
        )

        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data.get('access_token')

            if access_token:
                print("Access token received:", access_token)
                user_data = self.user_data(access_token)
                return user_data  # You can modify this to return a user instance if needed
            else:
                print("No access token found in response.")
        else:
            print(f"Failed to get access token. Status code: {token_response.status_code}")
            print("Response:", token_response.text)
        return None