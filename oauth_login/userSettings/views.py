from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from .models import UserSettings
from .serializers import UserSettingsSerializer

# Create your views here.
class UserSettingsView(APIView):
    authentication_classes = [OAuth2Authentication]  # Use OAuth2 Token authentication
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_settings = UserSettings.objects.get(user=request.user)
        serializer = UserSettingsSerializer(user_settings)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user_settings = UserSettings.objects.get(user=request.user)
        data=request.data
        data['user'] = request.user.id
        print("-----><>",data)
        serializer = UserSettingsSerializer(user_settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_settings = UserSettings.objects.get(user=request.user)
        user_settings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

