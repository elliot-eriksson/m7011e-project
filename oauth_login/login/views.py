import hashlib

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from oauth2_provider.models import AccessToken
from django.http import JsonResponse
from django.utils.timezone import now
from django.views import View
from rest_framework.views import APIView
from oauth2_provider.views import IntrospectTokenView
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import get_access_token_model
from django.core.exceptions import ObjectDoesNotExist
import json

from .producer import publish

# TODO: Create views to create, update, delete and list users
# TODO: Create user Settings

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomIntrospectToken(IntrospectTokenView):

    def post(self, request, *args, **kwargs):
        print('post')
        post_data = request.POST
        print('post_data', post_data)
        token = post_data.get('token')

        response = super().post(request, *args, **kwargs)
        print('jsondata', response)
        if isinstance(response, JsonResponse):
            json_data = json.loads(response.content)
            
            print('json_data', json_data)

            if json_data.get("active", False):
                # Add a new field to the response data
                token_checksum = hashlib.sha256(token.encode("utf-8")).hexdigest()
                token_obj = get_access_token_model().objects.get(token_checksum=token_checksum)
                json_data["user_id"] = token_obj.user.id
                print('json_data with user_id', json_data)
                publish('token_introspected', json_data)
            else:
                json_data["user_id"] = None
        

        return JsonResponse(json_data)
