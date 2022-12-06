from rest_framework.generics import get_object_or_404
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
            return Response({"message": "only cannot get another user data"})

        return super().get(request, *args, **kwargs)

    def patch(self, request, username, *args, **kwargs):
        if request.user != get_object_or_404(User, username=username):
            return Response({"message": "cannot update another user data"})

        return super().patch(request, *args, **kwargs)


class AddListUsers(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "only staff user can get all users data"})
        return super().get(self, request, *args, **kwargs)

    def post(self, request):
        if request.user.is_staff:
            csv_file = CSVFiles(request).get_csv_file()

            admin_user = User.objects.filter(is_staff=True).first()
            User.objects.all().exclude(pk=admin_user.username).delete()

            with open(csv_file) as f_data:
                reader = csv.DictReader(f_data)
                exceptions = []
                for n, row in enumerate(reader, start=1):
                    data = {
                        "username": row["username"],
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "email": row["email"],
                        "location": row["location"],
                    }
                    serializer = UserSerializer(data=data)
                    if not serializer.is_valid():
                        error = {
                            "data": data,
                            "line": n,
                            "errors": serializer.errors,
                        }
                        exceptions.append(error)
                        continue
                    serializer.save()
                os.remove(csv_file)
                if exceptions:
                    return Response({"exceptions": exceptions})
            return Response(
                {"message": "the file data is uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )
