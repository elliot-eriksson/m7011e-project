from rest_framework import viewsets
from .models import Email
from .serializers import EmailLogSerializer
from email_service.auth_service import AuthService
from email_service.user_lookup import getStaffStatus
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseForbidden

import json
#TODO Add the serializer
# 
class EmailLogView(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailLogSerializer

    # TODO: Lägg till check så att bara staff kan komma åt denna endpoint

    def dispatch(self, request, *args, **kwargs):
        request = AuthService.validate_token(request)
        print("Request: ", request)
        # print("Request.json: ", request.json())
        isStaff = getStaffStatus(request.session["user_id"])
        if not isStaff:
            print("Not staff, access forbidden")
            return HttpResponseForbidden("You do not have permission to access this resource.")
        

        print("isStaff Dispatch: ", isStaff)
        # if not isStaff:
        #     print("Not staff")
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        
        print("End of dispatch")
        return super().dispatch(request, *args, **kwargs)
    