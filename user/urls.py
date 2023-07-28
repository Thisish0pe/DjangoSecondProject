from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'user'

urlpatterns = [
    path("registration/", views.Registration.as_view(), name='registration'), #user/registration/
    path("auth/", views.Auth.as_view(), name='auth'), #user/auth/
    path("auth/refresh", TokenRefreshView.as_view()), #jwt 토큰 재발급
]