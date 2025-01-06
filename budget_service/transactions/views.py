from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from budget_service.auth_service import AuthService
from budget.models import BudgetAccess


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def dispatch(self, request, *args, **kwargs):
        print("Dispatching request for token validation.")
        request = AuthService.validate_token(request)
        return super().dispatch(request, *args, **kwargs)
    
    def perform_create(self, request, *args, **kwargs):
    # Always override user from request context
        print("Performing create")
        print(self.request.session.get('user_id'), self.request.data['budget'])
        access = BudgetAccess.objects.get(user=self.request.session.get('user_id'), budget=request.data['budget'])

        if not access.has_permission('add_transaction'):
            return Response("Unauthorized to add transaction for this budget", status=401)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.session.get('user_id'))
        print("Transaction created")
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        transaction = get_object_or_404(Transaction, pk=pk)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=transaction.budget.id)
        if not access.has_permission('view_transactions'):
            return Response("Unauthorized to view transaction for this budget", status=401)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


    def listByUser(self, request, user_id=None):
        # user_id = self.request.user.id

        if user_id != request.session.get('user_id'):
            return Response("Unauthorized", status=401)
        transactions = Transaction.objects.filter(user=user_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def listByBudget(self, request, budget_id=None):
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=budget_id)
        if not access.has_permission('view_transactions'):
            return Response("Unauthorized to view transaction for this budget", status=401)
        transactions = Transaction.objects.filter(budget=budget_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        transaction = get_object_or_404(Transaction, pk=pk)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=transaction.budget.id)
        if not access.has_permission('edit_transaction'):
            return Response("Unauthorized to edit transaction for this budget", status=401)

          # Pass partial=True to allow partial updates (only fields provided in the request will be updated)
        serializer = self.get_serializer(transaction, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
        # return super().update(request, pk)
    
    def destroy(self, request, pk=None):
        transaction = get_object_or_404(Transaction, pk=pk)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=transaction.budget.id)
        if not access.has_permission('delete_transaction'):
            return Response("Unauthorized to delete transaction for this budget", status=401)
        return super().destroy(request, pk)
 
                

    