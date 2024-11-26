from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework_oauth.authentication import JWTAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .serializers import *
from .models import Budget


# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):

    ##CHANGE
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    print('BudgetViewSet')
    authentication_classes = [OAuth2Authentication]
    print('authclass', authentication_classes)
    permission_classes = [IsAuthenticated]
    print('permission_classes', permission_classes)

    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        print(f"User: {self.request.user}")
        print(f"Budgets for user: {Budget.objects.filter(owner=self.request.user)}")
        return Budget.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        print(f"Authorization Header: {request.META.get('HTTP_AUTHORIZATION')}")
        print(f"User: {request.user}")
        print(f"Auth: {request.auth}")
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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve user details from the request (decoded from the JWT token)
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,  # Add additional fields as needed
            'email': user.email,
        })