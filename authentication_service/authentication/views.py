from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserRegistrationSerializer
from rest_framework import generics

# Create your views here.
# class LoginViewSet(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(email=email, password=password)
#         if not user:
#             return Response({'error': 'Invalid credentials'}, status=401)
        
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': {
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email
#         }})

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer  # Correct typo here
    # permission_classes = [AllowAny]