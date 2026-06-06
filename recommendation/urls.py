from django.urls import path
from .views import crop_prediction, crop_recommendation

urlpatterns = [
    path('predict/', crop_prediction, name='predict'),
    path('', crop_recommendation, name='crop_recommendation'),
]