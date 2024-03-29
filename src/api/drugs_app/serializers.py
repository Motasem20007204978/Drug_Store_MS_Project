from drf_queryfields.mixins import QueryFieldsMixin
from rest_framework import serializers

from .models import Drug


class DrugSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = (
            "id",
            "name",
            "quantity",
            "drug_price",
            "exp_date",
            "created",
            "modified",
        )
        read_only_fields = ("created", "modified")
        extra_kwargs = {
            "name": {"required": False},
            "quantity": {"required": False},
            "drug_price": {"required": False},
            "exp_time": {"required": False},
        }
