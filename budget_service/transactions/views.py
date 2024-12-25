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
    
    # TODO; kan behöva ändras så att den kollar på add_transaction
    def perform_create(self, serializer):
    # Always override user from request context
        serializer.save(user=self.request.session.get('user_id'))

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
        if not access.has_permission('edit_transactions'):
            return Response("Unauthorized to edit transaction for this budget", status=401)
        return super().update(request, pk)
    
    def destroy(self, request, pk=None):
        transaction = get_object_or_404(Transaction, pk=pk)
        access = get_object_or_404(BudgetAccess, user=request.session.get('user_id'), budget=transaction.budget.id)
        if not access.has_permission('delete_transactions'):
            return Response("Unauthorized to delete transaction for this budget", status=401)
        return super().destroy(request, pk)
 
                

    