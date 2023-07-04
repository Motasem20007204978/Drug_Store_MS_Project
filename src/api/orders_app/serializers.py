from drf_queryfields.mixins import QueryFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drugs_app.models import Drug
from rest_framework import serializers

from .models import Order, OrderedDrug


class OrderedDrugSerialilzer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDrug
        fields = (
            "drug",
            "quantity",
            "total_drug_price",
        )
        read_only_fields = ("total_drug_price",)


class OrderSerializer(QueryFieldsMixin, WritableNestedModelSerializer):

    ordered_drugs = OrderedDrugSerialilzer(many=True)

    class Meta:
        model = Order
        fields = (
            "user",
            "status",
            "description",
            "ordered_drugs",
            "total_price",
            "created",
            "modified",
        )
        read_only_fields = ("status", "created", "modified", "total_price")
