from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="plutonium"),
    path("plutonium/", views.plutonium, name="plutonium"),
    path('accounts/signup/', views.signup, name='signup'),
       
]
