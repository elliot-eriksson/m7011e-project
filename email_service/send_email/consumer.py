import json
import pika
from django.conf import settings
from django.core.mail import send_mail
from .models import EmailLog

def send_invitation_email(ch, method, properties, body):
    data = json.loads(body)
    recipient_email = data['recipient_email']
    budget_name = data['budget_name']
    inviter_name = data['inviter_name']
    token = data['token']


    invitation_link = f"{settings.BUDGET_SERVICE_URL}/api/invitations/accept?token={token}"
    subject = f"Invitation to join the budget: {budget_name}"
    message = (
        f"Hello,\n\n"
        f"{inviter_name} has invited you to join the budget '{budget_name}'.\n"
        f"Click the link below to accept the invitation:\n\n"
        f"{invitation_link}\n\n"
        f"Best regards,\nBudget Management Team"
    )
    sender = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, sender, [recipient_email], fail_silently=False)
        EmailLog.objects.create(
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            status='SENT',
        )
    except Exception as e:
        EmailLog.objects.create(
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            status='FAILED',
            )


params = pika.URLParameters('amqps://bdsnvese:s3U-C0irT91fkjV9VXgYjA5Uo0bYhPPQ@hawk.rmq.cloudamqp.com/bdsnvese')
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.exchange_declare(exchange='invitations', exchange_type='fanout')


result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='invitations', queue=queue_name)

channel.basic_consume(queue=queue_name, on_message_callback=send_invitation_email, auto_ack=True)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()