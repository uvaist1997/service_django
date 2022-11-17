from django.urls import path, re_path
from django.contrib import admin
from . import views


urlpatterns = [
	path('list-tax-category',views.list_tax_category,name='api_list_tax_category'),
	path('create-tax-category',views.create_tax_category,name='api_create_tax_category'),

]