from django.urls import path, re_path
from users import views

app_name="users"

urlpatterns = [
    re_path('change-password/(?P<pk>.*)/$',views.change_password, name="change_password"),


    path('create-software-version/',views.create_software_version, name="create_software_version"),

    path('list-business-type/',views.list_business_types, name="list_business_types"),
    path('create-business-type/',views.create_business_type, name="create_business_type"),
    re_path('single-business-type/(?P<pk>.*)/$',views.single_business_type, name="single_business_type"),
    re_path('edit-business-type/(?P<pk>.*)/$',views.edit_business_type, name="edit_business_type"),
    re_path('delete-business-type/(?P<pk>.*)/$',views.delete_business_type, name="delete_business_type"),

    path('list_product/',views.list_product, name="list_product"),
    path('create_product/',views.create_product, name="create_product"),
    re_path('single-product/(?P<pk>.*)/$',views.single_product, name="single_product"),
    re_path('edit-product/(?P<pk>.*)/$',views.edit_product, name="edit_product"),
    re_path('delete-product/(?P<pk>.*)/$',views.delete_product, name="delete_product"),

    path('list-software-plan/',views.list_software_plan, name="list_software_plan"),
    path('create-software-plan/',views.create_software_plan, name="create_software_plan"),
    re_path('single-software-plan/(?P<pk>.*)/$',views.single_software_plan, name="single_software_plan"),
    re_path('edit-software-plan/(?P<pk>.*)/$',views.edit_software_plan, name="edit_software_plan"),
    re_path('delete-software-plan/(?P<pk>.*)/$',views.delete_software_plan, name="delete_software_plan"),


    path('list_service/',views.list_service, name="list_service"),
    path('create_service/',views.create_service, name="create_service"),
    re_path('single-service/(?P<pk>.*)/$',views.single_service, name="single_service"),
    re_path('edit-service/(?P<pk>.*)/$',views.edit_service, name="edit_service"),
    re_path('delete-service/(?P<pk>.*)/$',views.delete_service, name="delete_service"),
    path('list_currency/',views.list_currency, name="list_currency"),
    path('create_currency/',views.create_currency, name="create_currency"),
    re_path('single-currency/(?P<pk>.*)/$',views.single_currency, name="single_currency"),
    re_path('edit-currency/(?P<pk>.*)/$',views.edit_currency, name="edit_currency"),
    re_path('delete-currency/(?P<pk>.*)/$',views.delete_currency, name="delete_currency"),
    path('list_period/',views.list_period, name="list_period"),
    path('create_period/',views.create_period, name="create_period"),
    re_path('single_period/(?P<pk>.*)/$',views.single_period, name="single_period"),
    re_path('edit-period/(?P<pk>.*)/$',views.edit_period, name="edit_period"),
    re_path('delete-period/(?P<pk>.*)/$',views.delete_period, name="delete_period"),
    path('master/',views.master, name="master"),
    re_path('list-details/(?P<pk>.*)/$',views.list_details, name="list_details"),
    re_path('edit-details/(?P<pk>.*)/$',views.edit_details, name="edit_details"),
    re_path('delete-details/(?P<pk>.*)/$',views.delete_details, name="delete_details"),

    re_path('delete-user/(?P<pk>.*)/$',views.delete_user, name="delete_user"),
    path('list-users/',views.list_users, name="list_users"),
    path('user-companies/',views.user_companies, name="user_companies"),

    
    path('get-user-companies/',views.get_user_companies, name="get_user_companies"),
    path('get-company-vanId/',views.get_company_vanId, name="get_company_vanId"),
    path('get-company-products/',views.get_company_products, name="get_company_products"),
    re_path('user-edit-company/(?P<pk>.*)/$',views.user_edit_company, name="user_edit_company"),
    

    path('list-master/',views.list_master, name="list_master"),
    re_path('delete-master/(?P<pk>.*)/$',views.delete_master, name="delete_master"),
    re_path('single-view-master/(?P<pk>.*)/$',views.single_view_master, name="single_view_master"),
    re_path('edit-sale-status/(?P<pk>.*)/$',views.edit_sale_status, name="edit_sale_status"),

    re_path('edit-payment-status/(?P<pk>.*)/$',views.edit_payment_status, name="edit_payment_status"),
    re_path('edit-reciept-status/(?P<pk>.*)/$',views.edit_reciept_status, name="edit_reciept_status"),
    re_path('edit-sale-return-status/(?P<pk>.*)/$',views.edit_sale_return_status, name="edit_sale_return_status"),
    re_path('edit-stock-order-status/(?P<pk>.*)/$',views.edit_stock_order_status, name="edit_stock_order_status"),

    
    path('list-reciept/',views.list_reciept, name="list_reciept"),
    re_path('delete-reciept/(?P<pk>.*)/$',views.delete_reciept, name="delete_reciept"),
    re_path('single-view-reciept/(?P<pk>.*)/$',views.single_view_reciept, name="single_view_reciept"),


    path('list-payment/',views.list_payment, name="list_payment"),
    re_path('delete-payment/(?P<pk>.*)/$',views.delete_payment, name="delete_payment"),
    re_path('single-view-payment/(?P<pk>.*)/$',views.single_view_payment, name="single_view_payment"),

    path('list-sale-returns/',views.list_sale_returns, name="list_sale_returns"),
    re_path('single-view-sale-returns/(?P<pk>.*)/$',views.single_view_sale_return, name="single_view_sale_return"),

    re_path('delete-sale-returns/(?P<pk>.*)/$',views.delete_sale_return, name="delete_sale_return"),

    re_path('single-view-stock-order/(?P<pk>.*)/$',views.single_view_stock_order, name="single_view_stock_order"),
    path('list-stock-order/',views.list_stock_order, name="list_stock_order"),
    re_path('delete-stock-order/(?P<pk>.*)/$',views.delete_stock_order, name="delete_stock_order"),

    path('list-sale-products/',views.list_sale_products, name="list_sale_products"),
    re_path('delete-sale-products/(?P<pk>.*)/$',views.delete_sale_product, name="delete_sale_product"),

    path('get-sale-price-list/',views.get_sale_price_list, name="get_sale_price_list"),
    re_path('delete-sale-price/(?P<pk>.*)/$',views.delete_sale_price, name="delete_sale_price"),
    path('list-sale-price/',views.list_sale_price, name="list_sale_price"),

    re_path('delete-sale-account-ledger/(?P<pk>.*)/$',views.delete_sale_account_ledger, name="delete_sale_account_ledger"),
    path('list-sale-account-ledger/',views.list_sale_account_ledger, name="list_sale_account_ledger"),

    re_path('delete-warehouse-stock/(?P<pk>.*)/$',views.delete_warehouse_stock, name="delete_warehouse_stock"),
    path('list-warehouse-stock/',views.list_warehouse_stock, name="list_warehouse_stock"),
    path('get-warehouse-stock-list/',views.get_warehouse_stock_list, name="get_warehouse_stock_list"),

    re_path('delete-expence-ledger/(?P<pk>.*)/$',views.delete_expence_ledger, name="delete_expence_ledger"),
    path('list-expence-ledger/',views.list_expence_ledger, name="list_expence_ledger"),

    re_path('delete-last-sale-price/(?P<pk>.*)/$',views.delete_last_sale_price, name="delete_last_sale_price"),
    path('list-last-sale-price/',views.list_last_sale_price, name="list_last_sale_price"),

    re_path('delete-sale-route/(?P<pk>.*)/$',views.delete_sale_route, name="delete_sale_route"),
    path('list-sale-route/',views.list_sale_route, name="list_sale_route"),

    path('list-transaction-type/',views.list_transaction_type, name="list_transaction_type"),
    re_path('delete-transaction-type/(?P<pk>.*)/$',views.delete_transaction_type, name="delete_transaction_type"),

    re_path('delete-van-route/(?P<pk>.*)/$',views.delete_van_route, name="delete_van_route"),
    path('list-van-route/',views.list_van_route, name="list_van_route"),

    # path('list-sale-return/',views.list_sale_return, name="list_sale_return"),
    # re_path('delete-sale-return/(?P<pk>.*)/$',views.delete_sale_return, name="delete_sale_return"),

    path('list-sale-order/',views.list_sale_order, name="list_sale_order"),
    re_path('single-view-sale-order/(?P<pk>.*)/$',views.single_view_sale_order, name="single_view_sale_order"),

    re_path('delete-sale-order/(?P<pk>.*)/$',views.delete_sale_order, name="delete_sale_order"),

    path('list-bill-wise/',views.list_bill_wise, name="list_bill_wise"),
    re_path('delete-bill-wise/(?P<pk>.*)/$',views.delete_bill_wise, name="delete_bill_wise"),

    path('list-van-settings/',views.list_van_settings, name="list_van_settings"),
    re_path('single-view-vansettings/(?P<pk>.*)/$',views.single_view_vansettings, name="single_view_vansettings"),
    re_path('delete-van-settings/(?P<pk>.*)/$',views.delete_van_settings, name="delete_van_settings"),

    path('company-product-report/',views.company_product_report, name="company_product_report"),
    re_path('print-company-product/(?P<pk>.*)/$',views.print_company_product, name="print_company_product"),


    path('e-invoice-list/',views.e_invoice_list, name="e_invoice_list"),
    path('e-invoice-view/',views.e_invoice_view, name="e_invoice_view"),
    re_path('delete-e-invoice/(?P<pk>.*)/$',views.delete_e_invoice, name="delete_e_invoice"),

    path('list-user-device-details/',views.list_user_device_details, name="list_user_device_details"),
]