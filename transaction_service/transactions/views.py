from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
# class TransactionViewSet(viewsets.ViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def list(self, request):
#         transactions = Transaction.objects.all()
#         serializer = TransactionSerializer(transactions, many=True)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = TransactionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def retrieve(self, request, pk=None):
#         transaction = Transaction.objects.get(id=pk)
#         serializer = TransactionSerializer(transaction)
#         return Response(serializer.data)
    
#     def update(self, request, pk=None):
#         transaction = Transaction.objects.get(id=pk)
#         serializer = TransactionSerializer(instance=transaction, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     def destroy(self, request, pk=None):
#         transaction = Transaction.objects.get(id=pk)
#         transaction.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

budgetURL = 'http://localhost:8000/budgets/'
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def listByUser(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def listByBudget(self, request):
        budget_id = request.data.get('budget_id')
        transactions = Transaction.objects.filter(budget=budget_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    


    