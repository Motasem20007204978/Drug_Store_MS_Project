from drugs_app.models import Drug
from .models import OrderedDrug, Order
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from notifications_app.tasks import create_notification
from rest_framework.exceptions import ValidationError
from django.db.transaction import on_commit
from .tasks import set_drug_quantity

@receiver(pre_save, sender=Order)
def cant_edit_cancelled(instance, **kwargs):
    if not instance.id:
        return
    previous_status = Order.objects.filter(pk=instance.pk).first().status
    if previous_status in ["CA", "RE"]:
        raise ValidationError("Cant edit order that is cancelled or rejected")


@receiver(post_save, sender=Order)
def rollback_quantity(instance, **kwargs):
    on_commit(lambda: set_drug_quantity.delay(instance.id))
    

@receiver(post_save, sender=Order)
def send_notification(instance, created, **kwargs):
    if created:
        data = {
            "sender_id": instance.user.id,
            "options": {
                'message': f'the user {instance.user.full_name} asks order',
                'order_id': instance.id
            },
        }
        on_commit(lambda: create_notification.delay(**data))

