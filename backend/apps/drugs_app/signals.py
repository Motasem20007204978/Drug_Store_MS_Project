from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Drug
from .tasks import reject_orders
from django.db.transaction import on_commit


@receiver(post_delete, sender=Drug)
def reject_orders(instance, **kwargs):
    on_commit(lambda: reject_orders.delay(instance.id))
