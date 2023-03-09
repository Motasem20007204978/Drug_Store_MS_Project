from .serializers import OrderSerializer
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from .models import Order, User
from rest_framework.response import Response
import csv
from django.http import HttpResponse
from rest_framework.views import APIView

# Create your views here.


class AbstractView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ListCreateOrder(AbstractView, ListModelMixin, CreateModelMixin):
    def get_pharmacy(self):
        username = self.request.resolver_match.kwargs.get("username")
        pharmacy = get_object_or_404(User, username=username)
        return pharmacy

    def filter_queryset(self, queryset):
        pharmacy = self.get_pharmacy()
        if pharmacy != self.request.user or not self.request.user.is_staff:
            return self.permission_denied()
        queryset = queryset.filter(user=pharmacy)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != self.get_pharmacy() or request.user.is_staff:
            return self.permission_denied()
        return self.create(request, *args, **kwargs)


class ListOrders(AbstractView, ListModelMixin):
    def get_queryset(self):
        filters = self.request.query_params.dict()
        return self.queryset.filter(**filters)

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.permission_denied()
        return self.list(request, *args, **kwargs)


class ExtractOrders(ListOrders):

    queryset = Order.objects.filter(status="CO")

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.permission_denied()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'

        serializer = self.get_serializer(
            self.get_queryset(),
        )
        header = OrderSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response


class ModifyOrder(
    AbstractView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
):
    def get_pharmacy(self):
        username = self.request.resolver_match.kwargs.get("username")
        pharmacy = get_object_or_404(User, username=username)
        return pharmacy

    def get_object(self):
        order_id = self.request.resolver_match.kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id, user=self.get_pharmacy())
        return order

    def get(self, request, *args, **kwargs):
        if self.get_pharmacy() != request.user or not request.user.is_staff:
            return self.permission_denied()
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if (
            self.get_pharmacy() != request.user
            or self.get_object().status == "Completed"
        ):
            return self.permission_denied()
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if (
            self.get_pharmacy() != request.user
            or self.get_object().status != "Completed"
        ):
            return self.permission_denied()
        return self.destroy(request, *args, **kwargs)


class StatusOrderView(AbstractView, APIView):
    def patch(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        status = request.data.get("status", "")
        if (
            status != "Completed"
            or not request.user.is_staff
            or order.status == "Completed"
        ):
            return self.permission_denied()
        order.set_status("Completed")
        return Response("the state is changed successfully")
