from .models import OrderedDrug, Order
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications_app.tasks import create_notification, delete_notifications
from django.db.transaction import on_commit
from .tasks import set_drug_quantity
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=OrderedDrug)
def reduce_drug_quantity(instance, **kwargs):
    on_commit(lambda: set_drug_quantity.delay(instance.drug.id, -instance.quantity))


@receiver(post_delete, sender=OrderedDrug)
def rollback_drug_quantity(instance, **kwargs):
    on_commit(lambda: set_drug_quantity.delay(instance.drug.id, instance.quantity))


@receiver(post_save, sender=Order)
def send_creation_notif(instance, created, **kwargs):
    if created:
        admin = User.objects.get(is_staff=1)
        data = {
            "sender_id": instance.user.id,
            "receiver_id": admin.id,
            "options": {
                "message": f"the user {instance.user.full_name} asks order",
                "order_id": instance.id,
            },
        }
        on_commit(lambda: create_notification.delay(**data))


@receiver(post_save, sender=Order)
def send_approving_notif(instance, **kwargs):
    if instance.status == "Completed":
        admin = User.objects.get(is_staff=1)
        data = {
            "sender_id": admin.id,
            "receiver_id": instance.user.id,
            "options": {
                "message": f"the admin approve your order order",
                "order_id": instance.id,
            },
        }
        on_commit(lambda: create_notification.delay(**data))


@receiver(post_delete, sender=Order)
def send_notification(instance, **kwargs):
    on_commit(lambda: delete_notifications.delay(instance.id, "order_id"))
