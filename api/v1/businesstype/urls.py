from django.urls import path, re_path
from django.contrib import admin
from django.conf.urls import url,include
from api.v1.businesstype import views


urlpatterns = [
	path('',views.list_business_types,name='api_list_business_types'),
	# re_path('single-business-type/(?P<pk>.*)/$',views.single_business_type,name='api_single_business_type'),
]