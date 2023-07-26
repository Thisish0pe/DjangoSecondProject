from django.urls import path
from . import views
from .views import ChatView

urlpatterns = [
	path('', views.ChaView.as_view(), name='chat'),
]