from django.urls import path, re_path
from django.conf.urls import url,include
from api.v1.payments import views


urlpatterns = [
	path('list-payments',views.list_payments,name='api_list_payments'),
	path('create-payments',views.create_payments,name='api_create_payments'),
	# re_path('edit-payment/(?P<pk>.*)/$',views.edit_payment,name='api_edit_payment'),

	path('edit-payment',views.edit_payment,name='api_edit_payment'),
]