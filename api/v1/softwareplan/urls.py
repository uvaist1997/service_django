from django.urls import path, re_path
from django.contrib import admin
from . import views


urlpatterns = [
	path('',views.list_software_plans,name='api_list_software_plans'),
]