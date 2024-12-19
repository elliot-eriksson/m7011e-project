import json
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .producer import publish
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from .consumer import validate_token_with_auth_service
import requests
from django.conf import settings
from .serializers import *
from .models import Budget
from budget_service.auth_service import AuthService
from budget_service.user_lookup import getUserID

# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):

    ##CHANGE
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    def dispatch(self, request, *args, **kwargs):
        print("Dispatching request for token validation.")
        request = AuthService.validate_token(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        print('getting queryset')
        # self.request.user = self.request.user_info.get('user_id')
        print(f"User: {self.request.user}")
        print(f"Budgets for user: {Budget.objects.filter(owner=self.request.user)}")
        return Budget.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        print(f"User ID: {request.session.get('user_id')}")
        request.user = request.session.get('user_id')
        
        response = BudgetAccessViewSet.listBudgetAccessByUser(self, request, request.user)
        serialized_budgets = []

        for r in response.data:
            try:
                # Get the Budget object associated with the budget ID
                budget = Budget.objects.get(id=r['budget'])
                
                # Serialize the Budget object
                serialized_budget = BudgetSerializer(budget)
                serialized_budgets.append(serialized_budget.data)

            except Budget.DoesNotExist:
                print(f"Budget with ID {r['budget']} does not exist.")

        print(f"List of budgets: {serialized_budgets}")
        # Return the serialized data in a Response object
        return Response(serialized_budgets)


    def perform_create(self, serializer):
        self.request.user = self.request.session.get('user_id')
        user_id = self.request.user
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

    def dispatch(self, request, *args, **kwargs):
        print("Dispatching request for token validation.")
        request = AuthService.validate_token(request)
        return super().dispatch(request, *args, **kwargs)

    def listBudgetAccessByUser(self, request, user_id=None):
        user = user_id
        budgetAccess = BudgetAccess.objects.filter(user=user)
        serializer = BudgetAccessSerializer(budgetAccess, many=True)

        print(serializer.data)
        return Response(serializer.data)

    def listBudgetAccessByBudget(self, request, budget_id=None):
        budget = Budget.objects.get(id=budget_id)
        budgetAccess = BudgetAccess.objects.filter(budget=budget)
        serializer = BudgetAccessSerializer(budgetAccess, many=True)
        return Response(serializer.data)

    # Todo: kanske byta namn på denna till invite_user
    def addBudgetAccess(self, request, pk=None):
        self.request.user = self.request.session.get('user_id')
        budget = get_object_or_404(Budget, pk=pk)
        access = get_object_or_404(BudgetAccess, user=request.user, budget=budget)

        if not access.has_permission('invite_users'):
            return Response({'error': 'You do not have permission to invite users.'}, status=status.HTTP_403_FORBIDDEN)


        username = request.data.get('username')
        email = request.data.get('email')
        role = request.data.get('role', BudgetRole.member)

        if not username and not email:
            return Response(
                {'error': 'At least one of username or email must be provided.'},
                status=status.HTTP_400_BAD_REQUEST
        )

        if role == BudgetRole.admin and not access.has_permission('invite_user_as_admin'):
            return Response({'error': 'You do not have permission to invite admins.'}, status=status.HTTP_403_FORBIDDEN)

        if role not in [BudgetRole.admin, BudgetRole.member]:
            return Response({'error': 'Invalid role.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_ID, user_email = getUserID(username, email)
            print(f"User ID: {user_ID}")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print(f"Den som bjöd in: {self.request.session.get('username')}")
        print(f"Budget Name: {budget.budgetName}")
        print(f"User email: {user_email}")


        


        return Response({'message': 'User invited successfully.'})


        

# class UserAPIView(APIView):
#     def get(self, pk=None):
#         users = get_user_model().objects.all()
#         user = get_user_model().objects.get(id=pk)
#         return Response({'id': user.id})

class UserAPIView(APIView):
    # Use JWT authentication and ensure the user is authenticated
    # authentication_classes = [OAuth2Authentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve user details from the request (decoded from the JWT token)
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,  # Add additional fields as needed
            'email': user.email,
        })