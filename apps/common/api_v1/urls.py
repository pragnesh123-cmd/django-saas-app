from django.urls import re_path
# from rest_framework import routers
from apps.common.api_v1 import views

# router = routers.SimpleRouter()
# router.register("employee", views.EmployeeViewSet)

app_name = "tenant"
urlpatterns = [
    re_path(r"create-account/$", views.CreateCompanyAccountAPIView.as_view()),
    re_path(r"login/$", views.VerifyLoginUser.as_view()),
    re_path(r"employees/",views.EmployeeList.as_view()),
    re_path(r"employee-remove/(?P<pk>[^/.]+)/$",views.EmployeeRemove.as_view()),
    re_path(r"employee-update/(?P<pk>[^/.]+)/$",views.EmployeeUpdate.as_view())
]
