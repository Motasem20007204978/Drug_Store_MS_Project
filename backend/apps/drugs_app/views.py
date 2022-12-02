from .serializers import DrugSerializer
from .models import Drug
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
    GenericAPIView,
)
from rest_framework.response import Response
from .store_csv import CSVFiles
import csv, os
from .filters import DrugFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from orderapp.models import Order


class AbstractView(GenericAPIView):
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ListCreateDrugView(AbstractView, ListCreateAPIView):

    filter_backends = [DjangoFilterBackend]
    filterset_class = DrugFilter

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "this user is not admin"})

        # some logic to get data from csv file
        # get data from csv file
        csv_file = CSVFiles(request).get_csv_file()

        # delete database
        self.get_queryset().delete()
        # reject all orders after deleting
        Order.objects.all().update(status="RE")

        with open(csv_file) as f_data:
            reader = csv.DictReader(f_data)
            exceptions = []
            for n, row in enumerate(reader, start=1):
                data = {
                    "name": row["name"],
                    "quantity": row["quantity"],
                    "exp_date": row["expiration_date"],
                    "drug_price": row["price"],
                }
                serializer = DrugSerializer(data=data)
                if not serializer.is_valid():
                    error = {
                        "data": data,
                        "line": n,
                        "errors": serializer.errors,
                    }
                    exceptions.append(error)
                    continue
                serializer.save()
        os.remove(csv_file)  # remove csv file after get data
        if exceptions:
            return Response({"exceptions": exceptions})
        return Response({"message": "the file data is uploaded successfully"})


class OneDrugView(AbstractView, RetrieveUpdateAPIView):
    def get_object(self):
        drug_id = self.kwargs["drug_id"]
        drug = get_object_or_404(Drug, pk=drug_id)
        return drug

    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().update(request, *args, **kwargs)
        return Response({"message": "this user is not admin"})
