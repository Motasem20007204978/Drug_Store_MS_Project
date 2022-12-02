import re
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .store_csv import CSVFiles
from .models import User
import csv
import os
from .serializers import UserSerializer
from user.serializers import MyTokenSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination


class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenSerializer


class SignoutView(APIView):
    def get(self, request):
        return Response({"message": "User Signed out"}, status=status.HTTP_200_OK)


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, code):
        user = get_object_or_404(User, code=code)
        if request.user != user or not request.user.is_staff:
            return Response({"message": "only cannot get another user data"})

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, code):
        if request.user != get_object_or_404(User, code=code):
            return Response({"message": "cannot update another user data"})
        serializer = UserSerializer(request.user, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AddListUsers(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def list(self, request):
        if not request.user.is_staff:
            return Response({"message": "only staff user can get all users data"})
        return super().list(self, request)

    def create(self, request):
        users = User.objects.all()
        if request.user.is_staff:
            csv_file = CSVFiles(request).get_csv_file()

            admin_user = User.objects.filter(is_staff=True).first()
            User.objects.all().exclude(pk=admin_user.code).delete()

            with open(csv_file) as f_data:
                reader = csv.DictReader(f_data)
                exceptions = []
                for n, row in enumerate(reader, start=1):
                    data = {
                        "code": row["code"],
                        "name": row["name"],
                        "password": row["password"],
                        "latitude": row["latitude"],
                        "longitude": row["longitude"],
                        "picture": None,
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
