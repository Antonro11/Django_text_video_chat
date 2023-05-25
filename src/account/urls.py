
from django.urls import path

from app.views import ListUsers
from account.views import Registration, Login, Logout


app_name = "account"

urlpatterns = [
    path("registration/", Registration.as_view(), name="registration"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("", ListUsers.as_view(),name="list-users"),
]
