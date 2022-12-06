from .models import OrderedDrug, Order
from drugs_app.models import Drug
from rest_framework import serializers
from drf_queryfields.mixins import QueryFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer


class OrderedDrugSerialilzer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDrug
        fields = (
            "drug_id",
            "name",
            "drug_price",
            "quantity",
            "total_drug_price",
            "exp_date",
        )
        read_only_fields = ("name", "drug_price", "price_per_quantity", "exp_date")


    def validate(self, attrs):
        drug_id = attrs.get("drug_id")
        drug = Drug.objects.get(id=drug_id)
        data = {
            'drug_id':drug_id,
            'name':drug.name,
            'drug_price':drug.drug_price,
            'quantity':attrs.get('quantity'),
            'exp_date':drug.exp_date,
        }
        return data


class OrderSerializer(QueryFieldsMixin, WritableNestedModelSerializer):

    ordered_drugs = OrderedDrugSerialilzer(many=True)

    class Meta:
        model = Order
        fields = (
            "status",
            "user",
            "description",
            "ordered_drugs",
            "created",
            "modified",
        )
        read_only_fields = ("status", "created", "modified", "total_price")
