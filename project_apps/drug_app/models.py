from django.db import models
from .validators import name_validator, integer_length, code_length
from django_extensions.db.models import ModificationDateTimeField, CreationDateTimeField
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class ParentDrug(models.Model):
    name = models.CharField(
        max_length=50, validators=[name_validator], primary_key=True
    )
    drug_id = models.PositiveIntegerField(
        verbose_name="code", unique=True, validators=[code_length]
    )
    quantity = models.PositiveIntegerField(validators=[integer_length])
    exp_date = models.DateField()
    price = models.DecimalField()
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()
    orders = GenericRelation(
        "order_app.OrderDrugRel",
        "drug_name",
        "content_type",
        related_query_name="orders",
    )

    class Meta:
        ordering = ["-created_at"]
        abstract = True


class Drug(ParentDrug):

    ...


# force admin to approve all orders before uploading another file
# cashing table to cash related objects with order without contstraints
#   as unique name, etc. and associate last filtering object at each time, remove that before last object
# also i think to prevent on_hold status,
# when saving another drugs from new file, checking if the drug is in druglike and has orders associated, we


class DrugLike(ParentDrug):
    ...
