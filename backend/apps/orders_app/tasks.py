from celery import shared_task
from .models import Order
from drugs_app.models import Drug

@shared_task(name='set_drug_quantity')
def set_drug_quantity(oid):
    instance = Order.objects.get(id=oid)
    drug = Drug.objects.get(id=instance.drug_id)
    if instance.status == "PE":
        drug.set_quantity(-instance.quantity)
    elif instance.status == 'RE':
        drug.set_quantity(instance.quantity)