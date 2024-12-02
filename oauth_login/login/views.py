from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from oauth2_provider.models import AccessToken
from django.http import JsonResponse
from django.utils.timezone import now
from django.views import View

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ValidateTokenView(View):
    def get(self, request, *args, **kwargs):
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
# @login_required()
# def secret_page(request, *args, **kwargs):
#     return HttpResponse('Secret contents!', status=200)