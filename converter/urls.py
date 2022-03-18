from django.urls import path
from .views import ConverterViews

urlpatterns = [
    path('converter/', ConverterViews.as_view())
]