from django.db import models
from .validators import name_validator, integer_length

# Create your models here.


class Drug(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[name_validator])
    quantity = models.IntegerField(validators=[integer_length])
    exp_date = models.DateField()
    drug_price = models.DecimalField(max_digits=4, decimal_places=2)
    availability = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    ...
