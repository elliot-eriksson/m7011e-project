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
    recipient_email =  response.get('recipient_email')
    budget_name = response.get('budget_name')
    inviter_name = response.get('inviter_name')
    role = response.get('role')
    token = response.get('token')


    invitation_link = f"{settings.BUDGET_SERVICE_URL}/api/invitations/{token}"
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
        send_mail(subject, message, 'boinkswe@gmail.com', [recipient_email], fail_silently=False)
        print("Email sent successfully")
        email_log_data = {
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
    

# params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
# connection = pika.BlockingConnection(params)

# channel = connection.channel()

# # channel.exchange_declare(exchange='invitations', exchange_type='fanout')
# channel.queue_declare(queue='send_email_invitations')

# # result = channel.queue_declare(queue='', exclusive=True)
# # queue_name = result.method.queue
# # channel.queue_bind(exchange='invitations', queue=queue_name)

# channel.basic_consume(queue='send_email_invitations', on_message_callback=send_invitation_email, auto_ack=True)
# print('Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
# connection.close()