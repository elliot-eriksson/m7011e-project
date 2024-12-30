from django.shortcuts import render
from rest_framework.response import Response, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import UserSettings
from .serializers import UserSettingsSerializer

# Create your views here.
class UserSettingsView(APIView):
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
        serializer = UserSettingsSerializer(user_settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_settings = UserSettings.objects.get(user=request.user)
        user_settings.deleteAccount()
        return Response({"detail","Your account and all related data have been deleted."},
                        status=status.HTTP_204_NO_CONTENT)
