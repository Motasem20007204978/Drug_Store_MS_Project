from .serializers import DrugSerializer
from .models import Drug
from rest_framework.generics import (
    get_object_or_404,
    GenericAPIView,
)
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    CreateModelMixin,
)
from rest_framework.response import Response
from .store_csv import CSVFiles
import csv, os
from rest_framework.parsers import FileUploadParser
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes


class AbstractView(GenericAPIView):
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()

    def check_staff_permission(self, request):
        if not request.user.is_staff:
            return self.permission_denied(request)


@extend_schema_view(
    get=extend_schema(
        description="takes fields and return drugs' data according to fields to be returned",
        operation_id="list drugs",
        tags=["drugs"],
        parameters=[
            OpenApiParameter(
                name="fields",
                description="select fields you want to be represented, otherwise it will return all fields",
            ),
        ],
    ),
    post=extend_schema(
        description="take json data for a drug and add it",
        operation_id="add a drug",
        tags=["drugs"],
    ),
)
class ListCreateDrugView(AbstractView, ListModelMixin, CreateModelMixin):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_staff_permission(request)
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(
        description="extract csv file data for drugs and add it",
        operation_id="add drugs",
        # request={
        #     "multipart/form-data": {
        #         "type": "object",
        #         "properties": {"file": OpenApiTypes.BINARY},
        #     }
        # },
        tags=["drugs"],
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="add csv data",
                        value={"message": "the file data is uploaded successfully"},
                    )
                ],
            )
        },
    ),
)
class FileUploadView(AbstractView):

    parser_classes = (FileUploadParser,)

    def perform_deletion(self):
        # delete database
        self.get_queryset().delete()

    def extract_data(self, row):
        data = {
            "name": row["name"],
            "quantity": row["quantity"],
            "exp_date": row["expiration_date"],
            "drug_price": row["price"],
        }
        return data

    def gather_exceptions(self, exps, **kwargs):
        error = {
            "data": kwargs["data"],
            "line": kwargs["line_num"],
            "errors": kwargs["serializer"].errors,
        }
        exps.append(error)
        return exps

    def perform_creation(self, csv_file):
        with open(csv_file) as f_data:
            reader = csv.DictReader(f_data)
            exceptions = []
            for n, row in enumerate(reader, start=1):
                data = self.extract_data(row)
                serializer = self.get_serializer(data=data)
                if not serializer.is_valid():
                    exceptions = self.gather_exceptions(
                        exceptions, line_num=n, data=data, serializer=serializer
                    )
                    continue
                serializer.save()
        os.remove(csv_file)  # remove csv file after get data
        if exceptions:
            return Response({"exceptions": exceptions})

    def post(self, request, *args, **kwargs):
        self.check_staff_permission(request)
        self.perform_deletion()

        # some logic to get data from csv file
        # get data from csv file
        csv_file = CSVFiles(request).get_csv_file()
        self.perform_creation(csv_file)

        return Response({"message": "the file data is uploaded successfully"})


@extend_schema_view(
    get=extend_schema(
        operation_id="get drug data",
        tags=["drugs"],
        description="get drug data by id",
        parameters=[
            OpenApiParameter(
                name="fields",
                description="select fields you want to be represented, otherwise it will return all fields",
            ),
        ],
    ),
    patch=extend_schema(
        operation_id="updata drug data",
        tags=["drugs"],
        description="update user data by id",
    ),
)
class OneDrugView(AbstractView, RetrieveModelMixin, UpdateModelMixin):
    def get_object(self):
        drug_id = self.kwargs["drug_id"]
        drug = get_object_or_404(Drug, pk=drug_id)
        return drug

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return self.partial_update(request, *args, **kwargs)
        return Response({"message": "this user is not admin"})
