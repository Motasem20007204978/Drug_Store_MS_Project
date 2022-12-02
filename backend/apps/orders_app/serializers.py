from .models import OrderedDrug, Order
from rest_framework import serializers


class OrderedDrugSerialilzer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDrug
        fields = (
            "origindrug",
            "order",
            "name",
            "drug_price",
            "quantity",
            "total_drug_price",
            "exp_date",
        )
        read_only_fields = ("name", "drug_price", "price_per_quantity", "exp_date")
        extra_kwargs = {
            "order": {"write_only": True, "required": False},
        }

    def create(self, validated_data):
        order = validated_data.pop("order")
        drug = validated_data.pop("origindrug")
        quantity = validated_data.pop("quantity")
        ordered_drug = OrderedDrug.objects.create(
            order=order,
            origindrug=drug,
            name=drug.name,
            drug_price=drug.drug_price,
            quantity=quantity,
            exp_date=drug.exp_date,
        )
        return ordered_drug

    def validate(self, attrs):
        print("attrs", attrs)
        drug = attrs.pop("origindrug")
        attrs["origindrug"] = drug.id
        data = super().validate(attrs)
        data["origindrug"] = drug
        return data


class OrderSerializer(serializers.ModelSerializer):

    ordered_drugs = OrderedDrugSerialilzer(many=True)

    class Meta:
        model = Order
        fields = (
            "status",
            "user",
            "description",
            "updated_at",
            "created_at",
            "ordered_drugs",
        )
        read_only_fields = ("status", "created_at", "updated_at", "total_price")
        ...

    def create_ordered_drugs(self, ordered_drugs: dict, order):
        for ordered_drug in ordered_drugs:
            ordered_drug["order"] = order.id
            ordered_drug["origindrug"] = ordered_drug["origindrug"].id
            serializer = OrderedDrugSerialilzer(data=ordered_drug)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    def create(self, validated_data):
        ordered_drugs = validated_data.pop("ordered_drugs")
        order = super().create(validated_data)
        self.create_ordered_drugs(ordered_drugs, order)
        return order

    def update(self, instance, validated_data):
        ordered_drugs = validated_data.pop("ordered_drugs")
        OrderedDrug.objects.filter(order=instance).delete()
        self.create_ordered_drugs(ordered_drugs, instance)
        return super().update(instance, validated_data)
