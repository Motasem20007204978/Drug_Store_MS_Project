from drf_queryfields.mixins import QueryFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drugs_app.serializers import Drug, DrugSerializer
from rest_framework import serializers

from .models import Order, OrderedDrug


class OrderedDrugSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        did = representation.pop("drug")
        drug = Drug.objects.get(id=did)
        representation["drug"] = DrugSerializer(instance=drug).data
        return representation

    class Meta:
        model = OrderedDrug
        fields = (
            "drug",
            "quantity",
            "total_drug_price",
        )
        read_only_fields = ("total_drug_price",)


class OrderSerializer(QueryFieldsMixin, WritableNestedModelSerializer):

    ordered_drugs = OrderedDrugSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "status",
            "ordered_drugs",
            "total_price",
            "created",
            "modified",
        )
        read_only_fields = (
            "user",
            "status",
            "created",
            "modified",
            "total_price",
        )

    def validate(self, attrs):
        request = self.context.get("request")
        attrs["user"] = request.user
        return attrs
