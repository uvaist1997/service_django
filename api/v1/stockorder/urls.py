from django.urls import path, re_path
from django.contrib import admin
from . import views


urlpatterns = [
	path('list-stock-orders',views.stock_orders,name='api_stock_orders'),
	path('create-stock-order',views.create_stock_order,name='api_create_stock_order'),
	path('edit-stock-order',views.edit_stock_order,name='api_edit_stock_order'),
]