from rest_framework import viewsets
from .models import Email
from .serializers import EmailLogSerializer
#TODO Add the serializer
# 
class EmailLogView(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailLogSerializer

    # TODO: Lägg till check så att bara superuser kan komma åt denna endpoint

    # def dispatch(self, request, *args, **kwargs):
    #     request = AuthService.validate_token(request)
    #     return super().dispatch(request, *args, **kwargs)