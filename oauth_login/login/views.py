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



class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ValidateTokenView(View):
    def get(self, request, *args, **kwargs):
        # token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        # try:
        #     access_token = AccessToken.objects.get(token=token, expires__gt=now())
        #     user = access_token.user
        #     return JsonResponse({
        #         'user_id': user.id,
        #         'username': user.username,
        #         'email': user.email,
        #     })
        # except AccessToken.DoesNotExist:
        #     return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        return True
# @login_required()
# def secret_page(request, *args, **kwargs):
#     return HttpResponse('Secret contents!', status=200)
# class CustomTokenIntrospectionView(APIView):
#     def post(self, request, *args, **kwargs):
#         print('post')
#         token = request.data.get("token")

#         if not token:
#             return JsonResponse({"active": False, "error": "No token provided"}, status=400)

#         try:
#             access_token = AccessToken.objects.get(token=token, expires__gt=now())
#             user = access_token.user
#             return JsonResponse({
#                 "active": True,
#                 "scope": access_token.scope,
#                 "client_id": access_token.application.client_id,
#                 "username": user.username,
#                 "user_id": user.id,
#                 "exp": access_token.expires.timestamp()
#             })
#         except AccessToken.DoesNotExist:
#             return JsonResponse({"active": False}, status=401)


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
            else:
                json_data["user_id"] = None

        return JsonResponse(json_data)
