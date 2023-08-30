from typing import Dict, Tuple

from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class QuerySet(models.QuerySet):
    def all(self):
        return super().filter(is_active=1)

    def delete(self) -> Tuple[int, Dict[str, int]]:
        super().filter(is_active=1).update(is_active=0)


class Manager(models.Manager):
    def get_queryset(self):
        return QuerySet(model=self.model, using=self._db)


class Drug(TimeStampedModel):
    name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    exp_date = models.DateField()
    drug_price = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=1, editable=False, db_index=True)
    objects = Manager()

    def set_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def delete(self, *args, **kwargs):
        self.is_active = 0
        self.save()

    class Meta:
        ordering = ["-created"]
        db_table = "drugs_db"
