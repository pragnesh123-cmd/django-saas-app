from apps.tenant.models import User
from apps.common.models import Employees
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from apps.tenant.custom_exception import PlainValidationError
from DjangoSassApi import settings


class CompanyAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for create account endpoint.
    """

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, attrs):
        attrs["password"] = make_password(attrs.get("password"))
        return attrs

    def is_valid(self, raise_exception=False):
        email = self.initial_data["email"]
        user = User.objects.filter(email=email)
        if user.exists() and user[0].password:
            raise PlainValidationError(
                detail={"message": f"user with this email already exists."}
            )
        return super(CompanyAccountSerializer, self).is_valid(raise_exception)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for employee endpoint.
    """
    profile_pic = serializers.FileField()

    class Meta:
        model = Employees
        fields = ("id","first_name", "last_name", "email","profile_pic","is_deleted")


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for employee update endpoint.
    """
    # profile_pic = serializers.FileField()

    class Meta:
        model = Employees
        fields = ("id","first_name", "last_name", "email","is_deleted")

    def validate(self, attrs):
        attrs.pop("is_deleted")
        return super().validate(attrs)