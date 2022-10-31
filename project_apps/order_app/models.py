from django.db import models
from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

# Create your models here.


class OrderDrugRel(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, editable=False
    )

    drug_name = models.CharField(editable=False, max_length=50, null=True)
    drug = GenericForeignKey("content_type", "drug_name")
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        indexes = [  # to fill it automatically
            models.Index(fields=["content_type", "drug_name"]),
        ]
        unique_together = ["order", "drug_name"]

    def validate_unique(self, exclude=None) -> None:
        super().validate_unique(exclude)
        if self.__class__.objects.filter(drug__name=self.drug.name):
            raise ValidationError(
                "this drug name is already exists", code="unique_together"
            )
            ...


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default="Pinned")

    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()
