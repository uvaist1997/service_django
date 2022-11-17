from django.conf.urls import  url,include
from main import views


app_name = "main"

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
]