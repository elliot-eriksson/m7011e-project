from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.contrib import admin
from .serializers import UserSerializer
from oauth2_provider.models import AccessToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from django.views import View

admin.autodiscover()
class UserList(generics.ListCreateAPIView):
    permission_classes= [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ValidateTokenView(View):
    def get(self, request, *args, **kwargs):
        print("Validating token")
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        try:
            access_token = AccessToken.objects.get(token=token, expires__gt=now())
            user = access_token.user
            return JsonResponse({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            })
        except AccessToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        
@login_required()
def user_info_secret(request, *args, **kwargs):
    print("User info secret")
    return JsonResponse({
                        'user_id': request.user.id,
                        'username' : request.user.username,
                        'first_name' : request.user.first_name ,
                        'email' : request.user.email},
                        status=200)