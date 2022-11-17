from django.urls import path, re_path
from django.contrib import admin
from . import views


urlpatterns = [
    path('user-login/', views.user_login, name='user_login'),
	re_path('verify/(?P<pk>.*)/$',views.verify,name='api_verify'),
	
    path('list-users/', views.list_users, name='list_users'),
    path('database-detail/', views.database_detail, name='database_detail'),
    path('create-user-device-detail/', views.create_user_device_detail, name='create_user_device_detail'),
    # path('single-customer/', views.single_customer, name='api_single_customer'),

    # path('list-categories/', views.categories, name='api_categories'),

    path('user-registration/', views.user_registration, name='user_registration'),

]