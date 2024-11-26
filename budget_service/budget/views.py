from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from .models import Budget


# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):

    ##CHANGE 
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticated]

    
    def perform_create(self, serializer):
        user_id = self.request.user.id
        serializer.save(owner=user_id)
        print('creating budget')
        self.createBudgetAccessEntry(serializer.instance, user_id)

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve user details from the request (decoded from the JWT token)
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,  # Add additional fields as needed
            'email': user.email,
        })