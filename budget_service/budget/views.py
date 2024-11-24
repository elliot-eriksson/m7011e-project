from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .models import Budget


# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):

    ##CHANGE 
    # queryset = Budget.objects.all()
    # serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]


    #CRUD create, read, update, delete budget
    def createBudget(self, request):
        serializer = BudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        print('creating budget')
        self.createBudgetAccessEntry(serializer.instance, request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def getBudget(self, request, pk=None):
        budget = Budget.objects.get(id=pk)
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)
    
    def listBudgets(self, request):
        budgets = Budget.objects.all()
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)
    
    def updateBudget(self, request, pk=None):
        budget = Budget.objects.get(id=pk)
        serializer = BudgetSerializer(instance=budget, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def deleteBudget(self, pk=None):
        budget = Budget.objects.get(id=pk)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def createBudgetAccessEntry(self, budget, user, accessLevel= 'owner', accepted=True):
        print('creating budget access entry')
        budget_access_data = {
            'budget': budget.id,
            'user': user.id,
            'accessLevel': 'owner',
            'accepted': True
        }
        budget_access_serializer = BudgetAccessSerializer(data=budget_access_data)
        budget_access_serializer.is_valid(raise_exception=True)
        budget_access_serializer.save()

# @api_view(['POST'])
# def create_budget(request, pk):
#     budget = Budget.objects.get(id=pk)

class BudgetAccessViewSet(viewsets.ModelViewSet):
    # queryset = Budget.objects.all()
    # serializer_class = BudgetSerializer

    #CRUD create, read, update, delete budget access
    def createBudgetAccess(self, request):
        serializer = BudgetAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # should be possible for user to get list of all budgets they have access to
    # and list of all users that have access to a budget

    def listBudgetAccessByUser(self, request, pk=None):
        user = get_user_model().objects.get(id=pk)
        budgetAccess = user.budgetAccess.all()
        serializer = BudgetAccessSerializer(budgetAccess, many=True)
        return Response(serializer.data)
    
    def listBudgetAccessByBudget(self, request, pk=None):
        budget = Budget.objects.get(id=pk)
        budgetAccess = budget.budgetAccess.all()
        serializer = BudgetAccessSerializer(budgetAccess, many=True)
        return Response(serializer.data)
    
    # def getBudgetAccess(self, request, pk=None):
    #     budgetAccess = BudgetAccess.objects.get(id=pk)
    #     serializer = BudgetAccessSerializer(budgetAccess)
    #     return Response(serializer.data)
    
    # def listBudgetAccess(self, request):
    #     budgetAccess = BudgetAccess.objects.all()
    #     serializer = BudgetAccessSerializer(budgetAccess, many=True)
    #     return Response(serializer.data)
    
    def updateBudgetAccess(self, request, pk=None):
        budgetAccess = BudgetAccess.objects.get(id=pk)
        serializer = BudgetAccessSerializer(instance=budgetAccess, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def deleteBudgetAccess(self, pk=None):
        budgetAccess = BudgetAccess.objects.get(id=pk)
        budgetAccess.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


class UserAPIView(APIView):
    def get(self, pk=None):
        users = get_user_model().objects.all()
        user = get_user_model().objects.get(id=pk)
        return Response({'id': user.id})

