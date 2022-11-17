from rest_framework import serializers
from web import models as web_model
from users import models as user_model
from django.utils.text import Truncator


class VanSettingsSerializer(serializers.ModelSerializer):
    exp_date = serializers.SerializerMethodField()
    VanSaleRoundoff = serializers.SerializerMethodField()
    IPAddress = serializers.SerializerMethodField()
    EmployeeID = serializers.SerializerMethodField()

    class Meta:
        model = web_model.VanSettings
        fields = ('id','EmployeeID','sales_return_account','Enable_ZATCA_Rules','BranchID','ServerName','EnablePortForward','CreditLimit','DBUserName','DBPassword', 'IPAddress', 'Port', 'DatabaseName', 'CountryId', 'PlaceofSupply', 'CashBalance', 'EditsalesReturnbeforeSync', 'EditsalesOrderbeforeSync', 'VanSaleRoundoff', 'EditPaymentinsalesbeforeSync', 'EditExpensebeforeSync', 'EditReceiptbeforeSync', 'QtyDecimalPoint', 'Sales_Invoice_Edit', 'Sales_price_lessthan_Purchase_price', 'PriceDecimalPoint', 'PriceCategoryID', 'VoucherPrefix', 'exp_date', 'CompanyProductId', 'Show_Last_Sales_Price', 'Allow_Receipt_Discount',
                  'StockOrderWarehouseFromId', 'Show_Cost_In_Stock_Order', 'Show_Inclusive_Field', 'Allow_Cash_Sales', 'Device_Code', 'VatSalesType', 'VanId', 'WarehouseId', 'VanName', 'Password', 'DiscountPercentPerBill', 'ShowNegativeStockItem', 'CanEditUnitPrice', 'AllowBillDiscount', 'Allow_Sales_Below_Min_Sales_Price', 'AllowNegativeStockSale', 'Allow_Sales_Below_Purchase_Price', 'AllowItemwiseDiscount', 'ShowSalesType', 'UserID', 'UserName', 'CashAccountID', 'BankAccountID', 'sales_account')


    def get_EmployeeID(self, instances):
        EmployeeID = 0
        if instances.EmployeeID:
            EmployeeID = instances.EmployeeID
        return EmployeeID

    def get_IPAddress(self, instances):
        IPAddress = ""
        if instances.IPAddress:
            IPAddress = instances.IPAddress
        return IPAddress

    def get_exp_date(self, instances):
        exp_date = instances.CompanyProductId.ProductExpiryDate
        print(exp_date, 'PKKKK')
        return exp_date

    def get_VanSaleRoundoff(self, instances):
        if instances.VanSaleRoundoff:
            a = instances.VanSaleRoundoff
        else:
            a = 0
        return a
