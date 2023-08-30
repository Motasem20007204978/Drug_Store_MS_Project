import csv

from django.http import HttpResponse
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, User
from .serializers import OrderSerializer

# Create your views here.


class AbstractView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ListCreateOrder(AbstractView, ListModelMixin, CreateModelMixin):
    def filter_queryset(self, queryset):
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(user__username=username)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.permission_denied(request)
        return self.create(request, *args, **kwargs)


class ExtractOrders(AbstractView, ListModelMixin):

    queryset = Order.objects.filter(status="completed")

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            self.permission_denied(request)

        response = HttpResponse(content_type="application/octet-stream")
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
    def get_object(self):
        order_id = self.request.resolver_match.kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id, user=self.request.user)
        return order

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.permission_denied(request)
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if self.get_object().status == "Completed":
            self.permission_denied(request)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.get_object().status == "Completed":
            self.permission_denied(request)
        return self.destroy(request, *args, **kwargs)


class StatusOrderView(AbstractView, APIView):
    def patch(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        status = request.data.get("status", "")
        if (
            status != "completed"
            or not request.user.is_staff
            or order.status == "Completed"
        ):
            self.permission_denied(request)
        order.set_status("completed")
        return Response("the state is changed successfully")
