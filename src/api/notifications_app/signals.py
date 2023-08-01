from django.db import transaction
from django.db.models.signals import *
from django.dispatch import receiver

from .models import Notification
from .tasks import delete_notification_client_side, send_client_notification


@receiver(signal=post_save, sender=Notification)
def send_notification(created, instance, **kwargs):
    if created:
        transaction.on_commit(lambda: send_client_notification(instance.id))


@receiver(post_delete, sender=Notification)
def delete_from_client_side(instance, **kwargs):
    transaction.on_commit(
        lambda: delete_notification_client_side(
            instance.id, instance.receiver.username
        )
    )
