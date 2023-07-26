from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path("registration/", views.Registration.as_view(), name='registration'), #user/registration/
    path("login/", views.Login.as_view(), name='login'), #user/login/
]