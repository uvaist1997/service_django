from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from registration.backends.default.views import RegistrationView
from django.conf import settings
from django.conf.urls import url
from main import views as general_views
from users import views as users_views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include(('api.v1.authentication.urls','api'), namespace='api_v1_authentication')),
    path('api/v1/users/', include(('api.v1.users.urls','api_users'),namespace='api_v1_users')),
    path('api/v1/business-type/', include('api.v1.businesstype.urls')),
    path('api/v1/products/', include('api.v1.products.urls')),
    path('api/v1/softwareplan/', include('api.v1.softwareplan.urls')),
    path('api/v1/companies/', include('api.v1.companies.urls')),
    path('api/v1/sales/', include('api.v1.sales.urls')),
    path('api/v1/stockorder/', include('api.v1.stockorder.urls')),
    path('api/v1/reciepts/', include('api.v1.reciepts.urls')),
    path('api/v1/payments/', include('api.v1.payments.urls')),
    path('api/v1/vansettings/', include('api.v1.vansettings.urls')),
    path('api/v1/taxcategory/', include('api.v1.taxcategory.urls')),


    # version2
    # path('api/v2/auth/', include(('api.v2.authentication.urls','api'), namespace='api_v2_authentication')),
    # path('api/v2/users/', include(('api.v2.users.urls','api_users'),namespace='api_v2_users')),
    # path('api/v2/business-type/', include('api.v2.businesstype.urls')),
    # path('api/v2/products/', include('api.v2.products.urls')),
    # path('api/v2/softwareplan/', include('api.v2.softwareplan.urls')),
    # path('api/v2/companies/', include('api.v2.companies.urls')),
    # path('api/v2/sales/', include('api.v2.sales.urls')),
    # path('api/v2/stockorder/', include('api.v2.stockorder.urls')),
    # path('api/v2/reciepts/', include('api.v2.reciepts.urls')),
    # path('api/v2/payments/', include('api.v2.payments.urls')),
    # path('api/v2/vansettings/', include('api.v2.vansettings.urls')),
    # path('api/v2/taxcategory/', include('api.v2.taxcategory.urls')),
    
    

    
    path('admin/', admin.site.urls),

    path('', general_views.app, name='app'),
    path('e-invoice-view', users_views.e_invoice_view, name='e_invoice_view'),
    path('app/dashboard/', general_views.dashboard, name='dashboard'),
    path('app/users/',include('users.urls',namespace="users")),
    path('app/web/',include('web.urls',namespace="web")),
    path('app/accounts/',include('registration.backends.default.urls')),


    url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_FILE_ROOT}),
]
