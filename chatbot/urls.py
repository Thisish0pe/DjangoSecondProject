from django.urls import path
from . import views
from .views import ChatView

app_name = 'chatbot'

urlpatterns = [
	path('', views.ChatView.as_view(), name='chat'),
    path('chatlist/', views.ChatList.as_view(), name='chatlist'),
]