from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.urls import include
from .views import login_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
]