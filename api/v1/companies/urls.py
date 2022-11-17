from django.urls import path, re_path
from django.contrib import admin
from django.conf.urls import url,include
from api.v1.companies import views


urlpatterns = [
	path('list-company',views.list_companies,name='api_list_companies'),
	path('create-company',views.create_company,name='api_create_company'),
	re_path('edit-company/(?P<pk>.*)/$',views.edit_company,name='api_edit_company'),

	path('list-company-products',views.list_company_products,name='api_list_company_products'),
	path('create-company-product',views.create_company_product,name='api_create_company_product'),

	path('get-device',views.get_device,name='api_get_device'),
	path('update-device-code',views.update_device_code,name='api_update_device_code'),
	path('get-device-details',views.get_device_details,name='api_get_device_details'),
	path('get-device-details1',views.get_device_details1,name='api_get_device_details1'),
	path('create-e-invoice',views.create_e_invoice,name='api_create_e_invoice')
]