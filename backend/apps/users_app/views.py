from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from drugs_app.store_csv import CSVFiles
from .models import User
import csv, os
from .serializers import UserSerializer, LoginSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    lookup_field = "username"
    queryset = User.objects.all()
    http_method_names = ['get', 'patch']

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        if request.user != user or not request.user.is_staff:
            return self.permission_denied(request)
        return super().get(request, *args, **kwargs)

    def patch(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            return self.permission_denied(request)
        return super().patch(request, *args, **kwargs)


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
            "data": kwargs['data'],
            "line": kwargs['line_num'],
            "errors": kwargs['serializer'].errors,
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
                    exceptions = self.gather_exceptions(exceptions, line_num=n, data=data, serializer=serializer)
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
