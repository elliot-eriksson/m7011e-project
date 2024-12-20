from rest_framework import viewsets
from .models import Email
from .serializers import EmailLogSerializer
#TODO Add the serializer
# 
class EmailLogView(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailLogSerializer

    # def post(self, request):
    #     try:
    #         data = request.data
    #         serializer = EmailSerializer(data=data)

    #         if not serializer.is_valid():
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #         recipient_list = serializer.validated_data['recipient_list']
    #         budget_name = serializer.validated_data.get('budget_name')
    #         inviter_name = serializer.validated_data.get('inviter_name')
    #         token = serializer.validated_data.get('token')  

    #         if not recipient_list or not budget_name or not inviter_name:
    #             return Response({'error': 'Required fields are missing.'}, status=status.HTTP_400_BAD_REQUEST)


    #         subject = f"Invitation to join the budget: {budget_name}"
    #         invitation_link = f"{settings.BUDGET_SERVICE_URL}/api/invitations/accept?token={token}" 

    #         message = (
    #             f"Hello,\n\n"
    #             f"{inviter_name} has invited you to join the budget '{budget_name}'.\n"
    #             f"Click the link below to accept the invitation:\n\n"
    #             f"[{invitation_link}]\n\n"
    #             f"Best regards,\nBudget Management Team"
    #         )
    #         sender = settings.EMAIL_HOST_USER

    #         send_mail(subject, message, sender, recipient_list, fail_silently=False)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


