from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Drug


@receiver(pre_save, sender=Drug)
def add_updating_time(sender, instance, *args, **kwargs):

    ...
