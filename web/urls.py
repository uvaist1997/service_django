from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from web import views

app_name = 'web'

urlpatterns = [
	
    path('create-version', views.create_version, name='create_version'),

	#account_group
    path('account-groups', views.account_group, name='account_group'),
	path('create-account-group', views.create_account_group, name='create_account_group'),
	re_path('single_account_group/(?P<pk>.*)/$',views.single_account_group, name="single_account_group"),
    re_path('edit_account_group/(?P<pk>.*)/$',views.edit_account_group, name="edit_account_group"),
    re_path('delete_account_group/(?P<pk>.*)/$',views.delete_account_group, name="delete_account_group"),
    #AccountLedger
    path('accountLedger', views.accountLedger, name='accountLedger'),
    path('CreateAccountLedger', views.CreateAccountLedger, name='CreateAccountLedger'),
    re_path('single_account_ledger/(?P<pk>.*)/$',views.single_account_ledger, name="single_account_ledger"),
    re_path('edit_account_ledger/(?P<pk>.*)/$',views.edit_account_ledger, name="edit_account_ledger"),
    re_path('delete_account_ledger/(?P<pk>.*)/$',views.delete_account_ledger, name="delete_account_ledger"),
    #CustomerTable
    path('customer-table', views.customertable, name='customertable'),

    # #companies
    path('companies', views.companies, name='companies'),
    path('create-company', views.create_company, name='create_company'),
    re_path('single-company/(?P<pk>.*)/$',views.single_company, name="single_company"),
    re_path('edit-company/(?P<pk>.*)/$',views.edit_company, name="edit_company"),
    re_path('delete-company/(?P<pk>.*)/$',views.delete_company, name="delete_company"),

    #company products
    path('export-company-products', views.export_company_products, name='export_company_products'),
    path('company-products', views.company_products, name='company_products'),
    path('create-company-product', views.create_company_product, name='create_company_product'),
    re_path('single-company-product/(?P<pk>.*)/$',views.single_company_product, name="single_company_product"),
    re_path('edit-company-product/(?P<pk>.*)/$',views.edit_company_product, name="edit_company_product"),
    re_path('delete-company-product/(?P<pk>.*)/$',views.delete_company_product, name="delete_company_product"),
    re_path('exp-date-trail-company-device/(?P<pk>.*)/$',views.exp_date_is_trail_company_device, name="exp_date_is_trail_company_device"),
    #company devics
    path('company-devices', views.company_devices, name='company_devices'),
    path('create-company-devices', views.create_company_devices, name='create_company_devices'),
    re_path('single-company-devices/(?P<pk>.*)/$',views.company_device, name="company_device"),
    re_path('edit-company-devices/(?P<pk>.*)/$',views.edit_company_devices, name="edit_company_devices"),
    re_path('delete-company-devices/(?P<pk>.*)/$',views.delete_company_devices, name="delete_company_devices"), 

    path('register', views.register, name='register'),


    path('company-list', views.company_list, name='company_list'),
    path('company-device-list', views.company_device_list, name='company_device_list'),
    path('get-company-device-list', views.get_company_device_list, name='get_company_device_list'),
    path('get-company-device', views.get_company_device, name='get_company_device'),
    path('get-update-company-device', views.get_update_company_device, name='get_update_company_device'),
    path('get-company-list', views.get_company_list, name='get_company_list'),
    re_path('delete-company-list/(?P<pk>.*)/$',views.delete_company_list, name="delete_company_list"),
    path('get-activity-logs', views.get_activity_logs, name='get_activity_logs'),
    path('activity-logs', views.activity_logs, name='activity_logs'),

    

]