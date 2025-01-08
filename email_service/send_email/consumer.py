import json
import pika
from django.conf import settings
from django.core.mail import send_mail
from .views import EmailLogView
from .serializers import EmailLogSerializer

def send_invitation_email(ch, method, properties, body):
    print("Received message type:", type(body))
    message = body.decode('utf-8')
    print("Received body:", body)
    print("Received message:", message)
    response = json.loads(message)
    print("Response:", response)
    sender_id = response.get('inviter_id')
    recipient_id = response.get('recipient_id')
    recipient_email =  response.get('recipient_email')
    budget_name = response.get('budget_name')
    inviter_name = response.get('inviter_name')
    role = response.get('role')
    token = response.get('token')
    


    invitation_link = f"{settings.BUDGET_SERVICE_URL}/api/invitations/accept/{token}/"
    subject = f"Invitation to join the budget: {budget_name}"
    message = (
        f"Hello,\n\n"
        f"{inviter_name} has invited you to join the budget '{budget_name} with {role} access'.\n"
        f"Click the link below to accept the invitation:\n\n"
        f"{invitation_link}\n\n"
        f"Best regards,\nBudget Management Team"
    )
    sender = settings.EMAIL_HOST_USER

    print(f"Sending email to {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    
    try:
        send_mail(subject, message, settings.SENDGRID_FROM_EMAIL , [recipient_email], fail_silently=False)
        print("Email sent successfully")
        email_log_data = {
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'recipient_email': recipient_email,
            'subject': subject,
            'message': message,
            'status': 'SENT'
        }
        email_log_serializer = EmailLogSerializer(data=email_log_data)
        email_log_serializer.is_valid(raise_exception=True)
        email_log_serializer.save()

    except Exception as e:
        print("Email sending failed:", e)
        email_log_data = {
            'recipient_email': recipient_email,
            'subject': subject,
            'message': message,
            'status': 'FAILED',
        }
        email_log_serializer = EmailLogSerializer(data=email_log_data)
        email_log_serializer.is_valid(raise_exception=True)
        email_log_serializer.save()
    
