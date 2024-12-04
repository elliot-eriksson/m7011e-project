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
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        print("CustomIntrospectToken view is being called")
        return super().dispatch(request, *args, **kwargs)
    
    # def get(self, request, *args, **kwargs):
    #     print('get')
    #     return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        print('post')
        post_data = request.POST
        print('post_data', post_data)
        token = post_data.get('token')
        
        # Use the base class's get_token_response method to get the initial response
        token_info = super().get_token_response(token)
        print('token_info', token_info)
        print('token active', token_info.get('active'))
        if 'user_id' not in token_info:
            print('userID')
        if token_info.get("active"):
            print('active')
        # Append the user ID if the token is valid and active
        if 'user_id' not in token_info:
            print('token_info', token_info)
            try:
                print('token', token)
                token_checksum = hashlib.sha256(token.encode("utf-8")).hexdigest()
                token_obj = get_access_token_model().objects.get(token_checksum=token_checksum)
                if token_obj.user:
                    token_info['user_id'] = token_obj.user.id  # Add user ID to the response
                    print('token_info with user_id try', token_info['user_id'])
            except ObjectDoesNotExist:
                print('token_info with user_id exeption', token_info)
                pass  # Token does not exist, handle appropriately

        print('token_info with user_id', token_info)
        return JsonResponse(token_info)
    
    def get_token_response(self, token):
        # This method uses the base class logic to get token info
        return super().get_token_response(token)
        
    # def get_token_response(self, token):
    #     # Get the token info from the default introspection
    #     print('get_token_info')
    #     token_info = super().get_token_response(token)
        
    #     # Add custom data to the response
    #     print('token_info', token_info)
    #     print('token', token_info['valid'])
    #     # user = token.user
    #     # if user:
    #     #     token_info['user_id'] = user.id  # Include the user ID in the response
    #     # print('token_info', token_info)
    #     return token_info
