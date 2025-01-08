from rest_framework import viewsets
from .models import Email
from .serializers import EmailLogSerializer
from email_service.auth_service import AuthService
from email_service.user_lookup import getStaffStatus
from django.http import HttpResponseForbidden


class EmailLogView(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailLogSerializer


    def dispatch(self, request, *args, **kwargs):
        request = AuthService.validate_token(request)
        isStaff = getStaffStatus(request.session["user_id"])
        if not isStaff:
            print("Not staff, access forbidden")
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return super().dispatch(request, *args, **kwargs)
    