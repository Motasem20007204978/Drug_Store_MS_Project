from .models import OrderedDrug, Order
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# from notification.utils import create_notfication
from rest_framework.exceptions import ValidationError


@receiver(pre_save, sender=Order)
def cant_edit_cancelled(sender, instance, *args, **kwargs):
    if not instance.id:
        return
    previous_status = Order.objects.filter(pk=instance.pk).first().status
    if previous_status in ["CA", "RE"]:
        raise ValidationError("Cant edit order that is cancelled or rejected")


@receiver(post_save, sender=Order)
def rollback_quantity(sender, instance, *args, **kwargs):
    if instance.status == "CA":
        related_drugs = instance.ordered_drugs.all()
        for drug in related_drugs:
            drug.set_quantity(drug.quantity)


@receiver(post_save, sender=Order)
def send_notification(sender, instance, *args, **kwargs):
    data = {
        "user": instance.user,
        "payload": f"Order with ID {instance.id} have some updates!",
    }
    # create_notfication(data)


@receiver(post_save, sender=OrderedDrug)
def set_drug_quantity(sender, instance, *args, **kwargs):
    drug = instance.origindrug
    if instance.status == "PE":
        drug.set_quantity(-instance.quantity)
