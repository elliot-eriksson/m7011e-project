from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BudgetSerializer
from .models import Budget

# Create your views here.
class BudgetViewSet(viewsets.ModelViewSet):

    ##CHANGE 
    # queryset = Budget.objects.all()
    # serializer_class = BudgetSerializer
    # permission_classes = [permissions.IsAuthenticated]


    #CRUD create, read, update, delete budget
    def createBudget(self, request):
        serializer = BudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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

    
# @api_view(['POST'])
# def create_budget(request, pk):
#     budget = Budget.objects.get(id=pk)

    


class UserAPIView(APIView):
    def get(self, pk=None):
        users = get_user_model().objects.all()
        user = get_user_model().objects.get(id=pk)
        return Response({'id': user.id})

