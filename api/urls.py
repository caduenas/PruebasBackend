from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('api/registro/', views.register),
    path('api/all_users/', views.all_users),
    path('api/login/', views.login),
    path('api/hash/', views.hashing),
]
