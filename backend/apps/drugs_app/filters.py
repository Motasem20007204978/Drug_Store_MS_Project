from django_filters import rest_framework as filters
from .models import Drug


class DrugFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")

    class Meta:
        model = Drug
        fields = ("name", "drug_price", "quantity")
