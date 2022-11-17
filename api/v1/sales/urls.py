from django.urls import path, re_path
from django.contrib import admin
from api.v1.sales import views


urlpatterns = [
	path('sale-products',views.list_sale_products,name='api_list_sale_products'),
	path('create-sale-product',views.create_sale_product,name='api_create_sale_product'),
	path('edit-sale-product',views.edit_sale_product,name='api_edit_sale_product'),
	path('delete-sale-products',views.delete_sale_products,name='api_delete_sale_products'),

	path('list-sale/price',views.list_sale_price,name='api_list_sale_price'),
	path('create-sale/price',views.create_sale_price,name='api_create_sale_price'),
	path('edit-sale-price',views.edit_sale_price,name='api_edit_sale_price'),
	path('delete-sale-price',views.delete_sale_price,name='api_delete_sale_price'),

	path('sale-account-ledgers',views.list_sale_account_ledgers,name='api_list_sale_account_ledgers'),
	path('create-sale-account-ledger',views.create_sale_account_ledger,name='api_create_sale_account_ledger'),
	path('edit-sale-account-ledger',views.edit_sale_account_ledger,name='api_edit_sale_account_ledger'),
	path('delete-sale-account-ledger',views.delete_sale_account_ledger,name='api_delete_sale_account_ledger'),

	path('list-warehouse-stocks',views.list_warehouse_stocks,name='api_list_warehouse_stocks'),
	path('list-warehouse-with-id',views.list_warehouse_with_id,name='api_list_warehouse_with_id'),

	path('create-warehouse-stock',views.create_warehouse_stock,name='api_create_warehouse_stock'),
	path('edit-warehouse-stock',views.edit_warehouse_stock,name='api_edit_warehouse_stock'),
	path('delete-warehouse-stock',views.delete_warehouse_stock,name='api_delete_warehouse_stock'),

	path('list-expense-ledgers',views.list_expense_ledgers,name='api_list_expense_ledgers'),
	path('create-expense-ledger',views.create_expense_ledger,name='api_create_expense_ledger'),
	# path('edit-expense-ledger',views.edit_expense_ledger,name='api_edit_expense_ledger'),
	# path('delete-expense-ledger',views.delete_expense_ledger,name='api_delete_expense_ledger'),


	path('list-last-sale-prices',views.last_sale_prices,name='api_last_sale_prices'),
	path('create-last-sale-price',views.create_last_sale_prices,name='api_create_last_sale_prices'),
	path('edit-last-sale-price',views.edit_last_sale_prices,name='api_edit_last_sale_prices'),
	path('delete-last-sale-price',views.delete_last_sale_prices,name='api_delete_last_sale_prices'),


	path('sale-routes',views.sale_routes,name='api_sale_routes'),
	path('create-sale-route',views.create_sale_route,name='api_create_sale_route'),
	path('edit-sale-route',views.edit_sale_route,name='api_edit_sale_route'),
	path('delete-sale-route',views.delete_sale_route,name='api_delete_sale_route'),

	path('list-transaction-types',views.list_transaction_types,name='api_list_transaction_types'),
	path('create-transaction-type',views.create_transaction_type,name='api_create_transaction_type'),

	path('list-van-routes',views.list_van_routes,name='api_list_van_routes'),
	path('create-van-route',views.create_van_route,name='api_create_van_route'),

	path('sales',views.list_sales,name='api_list_sales'),
	path('create-sale',views.create_sale,name='api_create_sale'),
	path('create-single-sale',views.create_single_sale,name='api_create_single_sale'),
	path('create-single-sale-count',views.create_single_sale_with_count,name='api_create_single_sale_with_count'),

	path('edit-sales',views.edit_sales,name='api_edit_sale'),
	path('update-sale-status',views.update_sale_status,name='api_update_sale_status'),

	path('sale-returns',views.sale_returns,name='api_sale_returns'),
	path('create-sale-returns',views.create_sale_returns,name='api_create_sale_returns'),
	path('create-single-sale-returns',views.create_single_sale_return,name='api_create_single_sale_return'),

	path('edit-sale-returns',views.edit_sale_returns,name='api_edit_sale_returns'),

	path('sale-orders',views.sale_orders,name='api_sale_orders'),
	path('create-sale-orders',views.create_sale_orders,name='api_create_sale_orders'),
	path('edit-sale-orders',views.edit_sale_orders,name='api_edit_sale_orders'),


	path('list-bill-wise',views.list_bill_wise,name='api_list_bill_wises'),
	path('create-bill-wise',views.create_bill_wise,name='api_create_bill_wise'),



	path('create-sale-product-price',views.create_sale_product_price,name='api_create_sale_product_price'),
	# path('sale-product_price',views.list_sale_product_price,name='api_list_sale_product_price'),
	# path('edit-sale-product_price',views.edit_sale_product_price,name='api_edit_sale_product_price'),
	# path('delete-sale-product_price',views.delete_sale_product_price,name='api_delete_sale_product_price'),



]