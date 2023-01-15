from django.db.models.signals import *
from .models import User
from django.dispatch import receiver
from .tasks import send_password
from django.db import transaction


@receiver(post_save, sender=User)
def send_email_activation(instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: send_password.delay(instance.email))
