from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from budget_service.auth_service import AuthService



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def dispatch(self, request, *args, **kwargs):
        print("Dispatching request for token validation.")
        request = AuthService.validate_token(request)
        return super().dispatch(request, *args, **kwargs)

    def listByUser(self, request, user_id=None):
        # user_id = self.request.user.id
        transactions = Transaction.objects.filter(user=user_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def listByBudget(self, request, budget_id=None):
        transactions = Transaction.objects.filter(budget=budget_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
    # Always override user from request context
        serializer.save(user=self.request.session.get('user_id'))
                

    