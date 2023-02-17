from rest_framework import serializers
from .models import Drug
from drf_queryfields.mixins import QueryFieldsMixin


class DrugSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = (
            "name",
            "quantity",
            "drug_price",
            "exp_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {
            "name": {"required": False},
            "quantity": {"required": False},
            "drug_price": {"required": False},
            "exp_time": {"required": False},
        }
