from django.urls import path
from .views import chatbot,index

urlpatterns = [
    path("", chatbot, name="chatbot"),
    path("index/", index, name="index"),
]