from django.db import models

# Create your models here.
class Email(models.Model):
    sender_id = models.IntegerField(null=True, blank=True)
    recipient_id = models.IntegerField(null=True, blank=True)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[('SENT', 'Sent'), ('FAILED', 'Failed')])
    error_message = models.TextField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
