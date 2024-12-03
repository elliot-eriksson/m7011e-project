from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from oauth2_provider.models import AccessToken
from django.http import JsonResponse
from django.utils.timezone import now
from django.views import View
from rest_framework.views import APIView

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
class CustomTokenIntrospectionView(APIView):
    def post(self, request, *args, **kwargs):
        print('post')
        token = request.data.get("token")

        if not token:
            return JsonResponse({"active": False, "error": "No token provided"}, status=400)

        try:
            access_token = AccessToken.objects.get(token=token, expires__gt=now())
            user = access_token.user
            return JsonResponse({
                "active": True,
                "scope": access_token.scope,
                "client_id": access_token.application.client_id,
                "username": user.username,
                "user_id": user.id,
                "exp": access_token.expires.timestamp()
            })
        except AccessToken.DoesNotExist:
            return JsonResponse({"active": False}, status=401)