from django.urls import path, re_path
from django.contrib import admin
from api.v1.vansettings import views


urlpatterns = [
    path('list-van-settings', views.list_van_settings,
         name='api_list_van_settings'),
    path('create-van-settings', views.create_van_settings,
         name='api_create_van_settings'),

    path('create-van-password', views.create_van_password,
         name='api_create_van_password'),

    path('get-van-password-expire', views.get_van_password_expire,
         name='api_get_van_password_expire'),
]
