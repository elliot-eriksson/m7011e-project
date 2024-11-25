from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def listByUser(self, request, user_id=None):
        transactions = Transaction.objects.filter(user=user_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def listByBudget(self, request, budget_id=None):
        transactions = Transaction.objects.filter(budget=budget_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    


    