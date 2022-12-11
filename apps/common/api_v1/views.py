from datetime import datetime
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.tenant.models import Company,User
from apps.common.models import Employees
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from apps.common.api_v1.serializers import (
    CompanyAccountSerializer,
    EmployeeSerializer,
    EmployeeUpdateSerializer
)
from apps.tenant.generate_schema_name import Schema
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from DjangoSassApi import settings
# from rest_framework import filters



class CreateCompanyAccountAPIView(generics.CreateAPIView):
    """
    :In this api create account(for example:Company)
    """

    serializer_class = CompanyAccountSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        schema_name = Schema().generate_schema_name()

        def generate_schema():
            return Schema().generate_schema_name()

        # check schema name unique or not if not then again new schema name generate
        while Company.objects.filter(schema_name=schema_name).exists():
            schema_name = generate_schema()

        company_name = request.data.get("company_name")
        company = Company(schema_name=schema_name,name=company_name)
        company.save()
        employee = serializer.save(
            company=company,is_superuser=True,is_staff=True)
        Token.objects.get_or_create(user=employee)
        return Response(status=status.HTTP_201_CREATED)


class VerifyLoginUser(APIView):
    """
    :Verify company and update last login time
    """

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
        :Returns-
            user,token,uid
        """
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except BaseException as e:
            return Response(
                {"error": True, "message": "Email is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if check_password(password,user.password):
            token, _ = Token.objects.get_or_create(user=user)
            user.last_login = datetime.now()
            user.save()
            return Response(
                {"user": user.email, "token": token.key, "uid": user.company.uid},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": True, "message": "Password is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        

class EmployeeList(generics.ListAPIView):
    """
    :listing company employee
    """
    serializer_class = EmployeeSerializer
    queryset = Employees.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"

    def get_queryset(self):
        queryset = super(EmployeeList, self).get_queryset()
        ordering =  self.request.query_params.get("ordering")
        search =  self.request.query_params.get("search")
        if ordering:
            return queryset.order_by(ordering)
        if search:
            return queryset.filter()
        return queryset
    
    def post(self, request, *args, **kwargs):
        profile_pic = request.FILES.get("profile_pic")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.save()
        parent_dir = f"{settings.BASE_DIR}/profile_pic_upload/{request.headers.get('uid')}_{serializer.id}.png"
        with open(parent_dir, 'wb+') as f:
            for chunk in profile_pic.chunks():
                f.write(chunk)
        return Response(status=status.HTTP_200_OK,data={"error":False,"data":[],"message":"employee is created."})


class EmployeeRemove(generics.DestroyAPIView):
    """
    :Employee remove endpoint
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = EmployeeSerializer
    queryset = Employees.objects.all()

    def delete(self, request, *args, **kwargs):
        employee_id = self.kwargs.get("pk")
        Employees.objects.filter(id=employee_id).update(is_deleted=True)
        return Response(status=status.HTTP_200_OK,data={"error":False,"data":[],"message":"employee deleted successfully."})


class EmployeeUpdate(generics.DestroyAPIView):
    """
    :Employee update endpoint
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = EmployeeUpdateSerializer
    queryset = Employees.objects.all()

    def put(self, request, *args, **kwargs):
        profile_pic = request.FILES.get("profile_pic")
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data,instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer=serializer.save()
        parent_dir = f"{settings.BASE_DIR}/profile_pic_upload/{request.headers.get('uid')}_{serializer.id}.png"
        with open(parent_dir, 'wb+') as f:
            for chunk in profile_pic.chunks():
                f.write(chunk)
        return Response(status=status.HTTP_200_OK,data={"error":False,"data":[],"message":"employee updated successfully."})