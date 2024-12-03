from django.contrib.auth import get_user_model

from .producer import publish
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
from django.conf import settings
from .serializers import *
from .models import Budget

# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):

    ##CHANGE
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    # permission_classes = [IsAuthenticated]


    def validate_token(self, token):
        """
        Validates the token by calling the auth service.
        """
        print(f'{token=}')
        publish('validate_token', {'token': token})
        # print('validating token')
        # auth_url = f"{settings.AUTH_SERVICE_URL}/api/validate_token/"
        # print(f"Auth URL: {auth_url}")
        # headers = {'Authorization': f'Bearer {token}'}
        # print(f"Headers: {headers}")
        # try:
        #     print('trying to validate token')
        #     response = requests.get(auth_url, headers=headers)
        #     print(f"Response: {response}")
        #     if response.status_code == 200:
        #         publish('validate_token', {'token': token})
        #         return response.json()  # User info if token is valid
            
        #     return None  # Invalid or expired token
        # except requests.RequestException as e:
        #     print(f"Error validating token: {e}")
        #     return None
        

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to validate the token before handling any requests.
        """
        print('dispatching')
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]
        user_info = self.validate_token(token)
        if not user_info:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        print(f"User info: {user_info}")

        request.user = user_info.get('user_id')  # Attach user ID to the request for later use
        print(f"User: {request.user}")

        request.user_info = user_info  # Attach user info to the request for later use
        print(f"User Info: {request.user}")
        print(f"Request: {request}")
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        print('getting queryset')
        self.request.user = self.request.user_info.get('user_id')
        print(f"User: {self.request.user}")
        print(f"Budgets for user: {Budget.objects.filter(owner=self.request.user)}")
        return Budget.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        print('listing budgets')
        print(f"User: {request.user}")
        print(f"User_info: {request.user_info}")
        
        request.user = request.user_info.get('user_id')
        # print(f"Authorization Header: {request.META.get('HTTP_AUTHORIZATION')}")
        # print(f"User: {request.user_info.get('user_id')}")
        # print(f"Auth: {request.auth}")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        serializer.save(owner=user_id)
        print('creating budget')
        self.createBudgetAccessEntry(serializer.instance, user_id)
        # self.createBudgetAccessEntry(serializer.instance, self.request.user)

    def createBudgetAccessEntry(self, budget, user_id, accessLevel= 'owner', accepted=True):
        print('creating budget access entry')
        budget_access_data = {
            'budget': budget.id,
            'user': user_id,
            'accessLevel': 'owner',
            'accepted': True
        }
        budget_access_serializer = BudgetAccessSerializer(data=budget_access_data)
        budget_access_serializer.is_valid(raise_exception=True)
        budget_access_serializer.save()


class BudgetAccessViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetAccessSerializer

    def listBudgetAccessByUser(self, request, user_id=None):
        user = get_user_model().objects.get(id=user_id)
        budgetAccess = user.budgetAccess.all()
        serializer = BudgetAccessSerializer(budgetAccess, many=True)
        return Response(serializer.data)

    def listBudgetAccessByBudget(self, request, budget_id=None):
        budget = Budget.objects.get(id=budget_id)
        budgetAccess = budget.budgetAccess.all()
        serializer = BudgetAccessSerializer(budgetAccess, many=True)
        return Response(serializer.data)


# class UserAPIView(APIView):
#     def get(self, pk=None):
#         users = get_user_model().objects.all()
#         user = get_user_model().objects.get(id=pk)
#         return Response({'id': user.id})

class UserAPIView(APIView):
    # Use JWT authentication and ensure the user is authenticated
    # authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve user details from the request (decoded from the JWT token)
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,  # Add additional fields as needed
            'email': user.email,
        })