from .views import WeatherDetails
from django.urls import path

urlpatterns = [
    path('', WeatherDetails , name='home'),

]