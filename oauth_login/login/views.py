import base64
import hashlib
from http.client import HTTPResponse
from io import BytesIO

from .models import UserG2FA
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import PasswordChangeSerializer, UserRegistrationSerializer, UserSerializer
from oauth2_provider.models import AccessToken
from django.http import JsonResponse
from django.utils.timezone import now
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.views import IntrospectTokenView
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import get_access_token_model
from django.core.exceptions import ObjectDoesNotExist
# from oauth2_provider.views import TokenViewMixin
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin

import json, pyotp, qrcode

from .producer import publish

# TODO: Create views to create, update, delete and list users
# TODO: Create user Settings

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# TODO:  behöver testas
class UserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print('request.data', request.data)
        data = request.data
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO:  behöver testas, kan vara problem med authentiseringen.
class UserDeleteView(APIView):
    """
    A view for deleting a user.
    Only authenticated users can delete their own account, or an admin can delete any account.
    """

    authentication_classes = [OAuth2Authentication]  # Use OAuth2 Token authentication
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete their account

    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the current user is either the user being deleted or an admin
        if request.user == user or request.user.is_staff:
            user.delete()  # Delete the user
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

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
                publish('token.validated', json_data, 'token_validation_queue')
            else:
                json_data["user_id"] = None
        

        return JsonResponse(json_data)

class PasswordUpdateView(APIView):
    """
    A view for updating the authenticated user's password.
    Only the user themselves can update their own password.
    """
    authentication_classes = [OAuth2Authentication]  # Use OAuth2 Token authentication
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        user = request.user  # Get the authenticated user
        serializer = PasswordChangeSerializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            # Set the new password and save the user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class G2FAView(APIView):
    authentication_classes = [OAuth2Authentication] 
    permission_classes = [IsAuthenticated]

    def get(self, request, action):
        if action == 'setup':
            return self.setup_g2fa(request)
        elif action == 'recovery':
            return self.generate_recovery_codes(request)
        else:
            return JsonResponse({'detail': 'Invalid action.'}, status=400)
       
    def post(self, request, action):
        if action == 'verify':
            return self.verify_otp(request)
        else:
            return JsonResponse({'detail': 'Invalid action.'}, status=400)
        
    def setup_g2fa(self, request):
        print('setup_g2fa')
        user_g2fa, _ = UserG2FA.objects.get_or_create(user=request.user)

        if not user_g2fa.g2fa_secret:
            user_g2fa.generate_secret()
        
        totp = pyotp.TOTP(user_g2fa.g2fa_secret)
        qr_url = totp.provisioning_uri(name=request.user.email, issuer_name='BudgetBuddy')

        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)

        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        return JsonResponse({
            "message": "G2FA setup QR code generated.",
            "qr_code_base64": f"data:image/png;base64,{qr_base64}"
        })
    
    def verify_otp(self, request):
        user_g2fa = UserG2FA.objects.get(user=request.user)
        otp = request.data.get('otp')

        if not user_g2fa.g2fa_secret:
            return JsonResponse({'detail': '2FA not enabled.'}, status=400)
        
        totp = pyotp.TOTP(user_g2fa.g2fa_secret)
        print('otp', otp)
        print('totp', totp)
        if totp.verify(otp):
            if not user_g2fa.g2fa_enabled:
                user_g2fa.g2fa_enabled = True
                user_g2fa.save()
                return JsonResponse({'detail': 'OTP verified!.'}, status=200)
        else:
            return JsonResponse({'detail': 'Invalid OTP.'}, status=400)
        
    def generate_recovery_codes(self, request):
        user_g2fa = UserG2FA.objects.get(user=request.user)
        user_g2fa.generate_recovery_codes()
        return JsonResponse({'recovery_codes': user_g2fa.recovery_codes}, status=200)