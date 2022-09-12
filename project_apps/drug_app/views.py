from signal import raise_signal
from .serializers import DrugSerializer
from .models import Drug
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from .store_csv import CSVFiles
import csv


class ListCreateDrugView(ListCreateAPIView):

    serializer_class = DrugSerializer
    queryset = Drug.objects.all()

    def post(self, request, *args, **kwargs):
        # some logic to get data from csv file
        # get data from csv file
        csv_file = CSVFiles(request).get_csv_file()
        # delete database   
        self.get_queryset().delete()

        with open(csv_file) as f_data:
            reader = csv.DictReader(f_data)
            errors = []
            for n, row in enumerate(reader, start=1):
                data = {
                    "name": row["name"],
                    "quantity": row["quantity"],
                    "exp_date": row["expiration_date"],
                    "drug_price": row["price"],
                    "availability": row["availability"],
                }
                serializer = DrugSerializer(data=data)
                if not serializer.is_valid():
                    # print('hello')
                    error = {
                        "data": data,
                        "line": n,
                        "errors": serializer.errors,
                    }
                    errors.append(error)
                    continue
                serializer.save()
            return Response({"exceptions": errors})


class OneDrugView(RetrieveUpdateAPIView):

    serializer_class = DrugSerializer
    queryset = Drug.objects.all()

    def get_object(self):
        drug_id = self.request.resolver_match.kwargs["drug_id"]
        print(drug_id)
        drug = Drug.objects.get(pk=drug_id)
        return drug
