from django.urls import path, re_path
from django.conf.urls import url,include
from api.v1.reciepts import views


urlpatterns = [
	path('list-reciepts',views.list_reciepts,name='api_list_reciepts'),
	path('create-reciepts',views.create_reciepts,name='api_create_reciepts'),
	path('create-single-reciept',views.create_single_reciept,name='api_create_single_reciept'),

	path('edit-reciepts',views.edit_reciepts,name='api_edit_reciepts'),
]