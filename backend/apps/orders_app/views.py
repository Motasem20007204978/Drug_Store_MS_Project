from .serializers import OrderSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
    ListAPIView,
    GenericAPIView,
)
from .models import Order, User
from rest_framework.response import Response
import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.


class AbstractView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ListCreateOrder(AbstractView, ListCreateAPIView):
    def get_pharmacy(self):
        code = self.request.resolver_match.kwargs.get("code")
        pharmacy = get_object_or_404(User, code=code)
        return pharmacy

    def filter_queryset(self, queryset):
        pharmacy = self.get_pharmacy()
        if pharmacy != self.request.user or not self.request.user.is_staff:
            return Response({"message": "cannot get another pharmacy orders"})
        queryset = queryset.filter(user=pharmacy)
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user != self.get_pharmacy():
            return Response({"message": "cannot create order for another user"})
        if request.user.is_staff:
            return Response({"message": "staff user cannot make orders"})
        return super().create(request, *args, **kwargs)


class ListOrders(AbstractView, ListAPIView):
    def get_queryset(self):
        filters = self.request.query_params.dict()
        return self.queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "admin only can get all orders"})
        return super().list(request, *args, **kwargs)


class ExtractOrders(ListOrders):

    queryset = Order.objects.filter(status="CO")

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "only admin can extract data"})

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


class ModifyOrder(RetrieveUpdateAPIView, AbstractView):
    def get_pharmacy(self):
        code = self.request.resolver_match.kwargs.get("code")
        pharmacy = get_object_or_404(User, code=code)
        print(pharmacy)
        return pharmacy

    def get_object(self):
        order_id = self.request.resolver_match.kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id, user=self.get_pharmacy())
        return order

    def get(self, request, *args, **kwargs):
        print(request.user, "user")
        if self.get_pharmacy() != request.user or not request.user.is_staff:
            return Response({"message": "cannot get another pharmacy orders"})
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.get_pharmacy() != request.user:
            return Response({"message": "cannot update another pharmacy orders"})
        if self.get_object().status != "PE":
            return Response({"message": "can update when order is pinned"})
        return super().update(request, *args, **kwargs)


class StatusOrderView(AbstractView, APIView):
    def patch(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        status = request.data.get("status", "")
        if not status:
            return Response({"message": "must put status in filed"})
        if order.status != "PE":
            return Response({"message": "cannot change if status is not pinned"})
        if status not in ["CO", "CA"]:
            return Response(
                {
                    "message": 'change status can only be with "CO" characters to be completed or "CA" characters to be cancelled'
                }
            )
        if not request.user.is_staff and status == "CO":
            return Response({"message": "only staff can meke order complete"})

        order.status = status
        print(order.id)
        order.save()
        return Response("the state is changed successfully")
