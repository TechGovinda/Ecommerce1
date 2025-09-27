from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .views import *

urlpatterns = [
               path("product/", product),
               path('',home),
               path('productpage/',productpage),
               ]

