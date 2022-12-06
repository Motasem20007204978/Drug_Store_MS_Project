from django.db import models
from .validators import name_validator, integer_length
from django.db import models
from .validators import name_validator, integer_length
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class AbstractDrug(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True, validators=[name_validator])
    quantity = models.PositiveIntegerField(validators=[integer_length])
    exp_date = models.DateField()
    drug_price = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        ordering = ["-created_at"]
        abstract = True


class Drug(AbstractDrug):
    def set_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    class Meta:
        db_table = "drugs_db"
