import csv
import os

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from drugs_app.store_csv import CSVFiles
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


@extend_schema_view(
    get=extend_schema(
        operation_id="get user data",
        tags=["users"],
        description="get user data by username_validator",
        parameters=[
            OpenApiParameter(
                name="fields",
                description="select fields you want to be represented, otherwise it will return all fields",
            ),
        ],
    ),
    patch=extend_schema(
        operation_id="updata user data",
        tags=["users"],
        description="update user data by username_validator, iff the authenticated user is the name's user",
    ),
)
class UserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    lookup_field = "username"
    queryset = User.objects.all()
    http_method_names = ["get", "patch"]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get("username"))
        if request.user != user and not request.user.is_staff:
            return self.permission_denied(request)
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print(kwargs.get("username"))
        user = get_object_or_404(User, username=kwargs.get("username"))
        if request.user != user:
            self.permission_denied(request)
        return super().patch(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        description="takes fields and return users' data according to fields to be returned",
        operation_id="list users",
        tags=["users"],
        parameters=[
            OpenApiParameter(
                name="fields",
                description="select fields you want to be represented, otherwise it will return all fields",
            ),
        ],
    ),
    post=extend_schema(
        description="take json data for a user and regiter it",
        operation_id="register a user",
        tags=["users"],
    ),
)
class AddListUsers(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post"]

    def check_staff_permission(self, request):
        if not request.user.is_staff:
            return self.permission_denied(request)

    def get(self, request, *args, **kwargs):
        self.check_staff_permission(request)
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_staff_permission(request)
        return super().post(request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(
        description="extract csv file data for users and regiter it",
        operation_id="register users",
        tags=["users"],
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="register csv data",
                        value={
                            "message": "the file data is uploaded successfully"
                        },
                    )
                ],
            )
        },
    ),
)
class FileUploadView(GenericAPIView):

    queryset = User.objects.all()

    def check_staff_permission(self, request):
        if not request.user.is_staff:
            return self.permission_denied(request)

    def perform_deletion(self):
        admin_user = User.objects.filter(is_staff=True).first()
        self.get_queryset().exclude(id=admin_user.id).delete()

    def extract_data(self, row):
        data = {
            "username": row["username"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "location": row["location"],
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
        exceptions = []
        with open(csv_file) as f_data:
            reader = csv.DictReader(f_data)
            for n, row in enumerate(reader, start=1):
                data = self.extract_data(row)
                serializer = UserSerializer(data=data)
                if not serializer.is_valid():
                    exceptions = self.gather_exceptions(
                        exceptions,
                        line_num=n,
                        data=data,
                        serializer=serializer,
                    )
                    continue
                serializer.save()
        os.remove(csv_file)
        if exceptions:
            return Response({"exceptions": exceptions})

    def post(self, request, *args, **kwargs):
        self.check_staff_permission(request)
        self.perform_deletion()

        csv_file = CSVFiles(request).get_csv_file()
        self.perform_creation(csv_file)

        return Response(
            {"message": "the file data is uploaded successfully"},
            status=status.HTTP_201_CREATED,
        )
