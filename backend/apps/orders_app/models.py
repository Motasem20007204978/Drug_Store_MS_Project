from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from drugs_app.models import Drug, TimeStampedModel
from django.conf import settings


User = get_user_model()


class Order(TimeStampedModel):
    STATUS = (
        ("PE", "Pending"),
        ("CO", "Completed"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(default="Pending", choices=STATUS, max_length=2)
    description = models.TextField()

    class Meta:
        db_table = "orders_db"

    @property
    def total_price(self) -> int:
        total_price = 0
        for drug in self.ordered_drugs.all():
            total_price += float(drug.total_drug_price)
        return total_price

    def set_status(self, status):
        self.status = status
        self.save()


class OrderedDrug(models.Model):

    drug = models.ForeignKey(
        Drug, on_delete=models.CASCADE, related_name="related_orders"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="ordered_drugs"
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ["order", "drug"]
        db_table = "ordered_drugs_db"

    def validate_unique(self, **kwargs) -> None:
        try:
            return super().validate_unique(**kwargs)
        except:
            raise ValidationError("cannot add the drug in the same order more than one")

    @property
    def total_drug_price(self):
        return "%.2f" % (float(self.drug.drug_price) * int(self.quantity))

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("The quantity must be above or equal 1")

        if self.quantity > self.drug.quantity:
            raise ValidationError(
                f"Please add quantity value lower than {self.drug.quantity}"
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)
