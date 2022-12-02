from django.db import models
from .validators import name_validator, integer_length
from django.db import models
from .validators import name_validator, integer_length

# Create your models here.


class AbstractDrug(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[name_validator])
    quantity = models.PositiveIntegerField(validators=[integer_length])
    exp_date = models.DateField()
    drug_price = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        abstract = True


class Drug(AbstractDrug):
    def set_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()
        ...
