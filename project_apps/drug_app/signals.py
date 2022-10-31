from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Drug, DrugLike


@receiver(pre_delete, sender=Drug)
def cash_drug(sender, instance, *args, **kwargs):
    print("hello")
    orders = instance.orders.all()
    for order in orders:
        DrugLike.objects.filter(name=instance.name).delete()
        drug_like = DrugLike.objects.create(
            name=instance.name,
            quantity=instance.quantity,
            exp_date=instance.exp_date,
            price=instance.price,
        )
        print(drug_like.name)
        order.drug = drug_like
        order.save()
        print(order.drug_name)
    ...
