from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Drug
