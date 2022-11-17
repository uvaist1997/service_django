from rest_framework import serializers
from web import models as web_model
from users import models as user_model
from django.utils.text import Truncator
from django.contrib.auth.models import User


class SaleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.SaleProduct
        fields = ('id','ProductId','minimumSalesPrice','BranchId','Productcode','Productname','Displayname','Description','SyncDate','VatId','GstId','Tax1Id','Tax2Id','Tax3Id')


class EditSaleProductSerializer(serializers.ModelSerializer):
    saleproduct = SaleProductSerializer(many=True)

    class Meta:
        model = web_model.SaleProduct
        fields = ('saleproduct','ProductId','BranchId','Productcode','Productname','Displayname','Description','SyncDate')

    def update(self, instance, validated_data):
        saleproduct = validated_data.pop('saleproduct')
        products = (instance.saleproduct).all()
        products = list(product)
        instance.BranchId = validated_data.get('BranchId', instance.BranchId)
        instance.Productcode = validated_data.get('Productcode', instance.Productcode)
        instance.Productname = validated_data.get('Productname', instance.Productname)
        instance.Displayname = validated_data.get('Displayname', instance.Displayname)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.SyncDate = validated_data.get('SyncDate', instance.SyncDate)
        instance.save()

        for i in saleproduct:
            product = products.pop(0)
            product.BranchId = i.get('BranchId', product.BranchId)
            product.Productcode = i.get('Productcode', product.Productcode)
            product.Productname = i.get('Productname', product.Productname)
            product.Displayname = i.get('Displayname', product.Displayname)
            product.Description = i.get('Description', product.Description)
            product.SyncDate = i.get('SyncDate', product.SyncDate)
            product.save()
        return instance


class SalePriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.SalePrice
        fields = ('id','ProductId','PriceListId','BranchId','UnitName','PurchasePrice','SalePrice','IsDefault','SalePrice1','SalePrice2','SalePrice3','MultiFactor','AutoBarcode','Barcode','SyncDate')


class SaleAccountLedgerSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField() 
    CompanyProductId = serializers.SerializerMethodField() 

    class Meta:
        model = web_model.SaleAccountLedger
        fields = ('id','CrNum','PlaceofSupply','LedgerCode','BillwiseApplicable','Credit_Limit','Balance','PriceCategoryID','CompanyProductId','LedgerId','PartyName','DisplayName','VatNum','GstNum','Tax1Number','Tax2Number','Tax3Number','RouteId','GroupId','Address1','City','State','Country','BuildingNumber','District','StreetName','AdditionalNo')
   
    def get_id(self, instances):
        id = instances.id
        return str(id)

    def get_CompanyProductId(self, instances):
        CompanyProductId = instances.CompanyProductId
        return str(CompanyProductId)


class WarehouseStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.WarehouseStock
        fields = ('id','CompanyProductId','ProductId','PriceListId','WarehouseId','Stock')



class ExpenseLedgerSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.ExpenseLedger
        fields = ('id','LedgerId','LedgerName')


class SaleRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.LastSalesPrice
        fields = ('id','LedgerId','CompanyProductId','SalePrice','PriceListId')


class SaleRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.SaleRoute
        fields = ('id','CompanyProductId','RouteId','RouteName')


class TransactionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.TransactionType
        fields = ('id','CompanyProductId','TransactionTypeId','MasterTypeId','TransactionTypeName','SyncDate')


class SaleMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.SaleMaster
        fields = ('Treatment','TaxableAmount','NonTaxableAmount','GUID','CompanyProductId','PlaceofSupply','salesOrderMasterID','TransactionTypeId','BranchId','LedgerId','PriceCategoryId','SaleAccount','TaxId','TaxType','Date','TotalGrossAmt','AddlDiscPercent','AddlDiscAmt','BillDiscPercent','BillDiscAmt','TotalDiscount','VATAmount','SGSTAmount','CGSTAmount','IGSTAmount','TAX1Amount','TAX2Amount','TAX3Amount','TotalTax','NetTotal','AdditionalCost','GrandTotal','RoundOff','CashReceived','CashAmount','BankAmount','Balance','VanId','status','Address1','Address2','Notes','CardNumber','CustomerName')


class SaleRestSerializer(serializers.ModelSerializer):

    SaleDetails = serializers.SerializerMethodField()

    class Meta:
        model = web_model.SaleMaster
        fields = ('id','Treatment','TaxableAmount','NonTaxableAmount','GUID','CompanyProductId','PlaceofSupply','TransactionTypeId','TransactionId','BranchId','LedgerId','PriceCategoryId','SaleAccount','TaxId','TaxType',
            'Date','TotalGrossAmt','AddlDiscPercent','AddlDiscAmt','BillDiscPercent','BillDiscAmt','TotalDiscount','VATAmount',
            'SGSTAmount','CGSTAmount','IGSTAmount','TAX1Amount','TAX2Amount','TAX3Amount','TotalTax','NetTotal','AdditionalCost',
            'GrandTotal','RoundOff','CashReceived','CashAmount','BankAmount','Balance','VanId','status','Address1','Address2','Notes',
            'CardNumber','CustomerName','SaleDetails')
        

    def get_SaleDetails(self, instances):
        SaleId = instances.id
        sales_details = web_model.SaleDetails.objects.filter(SaleId=SaleId)
        serialized = SalesDetailsSerializer(sales_details,many=True,)

        return serialized.data 


class SalesDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.SaleDetails
        fields = ('id','Qty','FreeQty','UnitPrice','InclusivePrice','PriceListId','DiscountPerc',
            'DiscountAmount','AddlDiscPercent','AddlDiscAmt','GrossAmount','TaxableAmount','VATPerc','VATAmount',
            'SGSTPerc','SGSTAmount','CGSTPerc','CGSTAmount','IGSTPerc','IGSTAmount','TAX1Perc','TAX1Amount',
            'TAX2Perc','TAX2Amount','TAX3Perc','TAX3Amount','NetAmount','ProductId','OrderStatus','CostPerPrice','StockOrderNo')



class SaleReturnRestSerializer(serializers.ModelSerializer):

    salereturndetails = serializers.SerializerMethodField()
    salereturn_billwise_details = serializers.SerializerMethodField()

    class Meta:
        model = web_model.SaleReturnMaster
        fields = ('id','Treatment','TaxableAmount','NonTaxableAmount','GUID','CompanyProductId','TransactionId','Date','RefferenceBillNo','RefferenceBillDate','LedgerId',
            'PriceCategoryId','EmployeeId','SaleAccount','TaxId','TaxType',
            'VATAmount','SGSTAmount','CGSTAmount','IGSTAmount','TAX1Amount',
            'TAX2Amount','TAX3Amount','TotalTax','NetTotal','AdditionalCost',
            'TotalGrossAmt','AddlDiscPercent','AddlDiscAmt','TotalDiscount','BillDiscPercent',
            'BillDiscAmt','GrandTotal','RoundOff','VanId','status',
            'Address1','Address2','Notes','CustomerName','salereturndetails','salereturn_billwise_details')
        

    def get_salereturndetails(self, instances):
        pk = instances.id
        sale_return_details = web_model.SaleReturnDetails.objects.filter(SaleReturnMasterId=pk)
        serialized = SaleReturnDetailsSerializer(sale_return_details,many=True,)

        return serialized.data 

    def get_salereturn_billwise_details(self, instances):
        pk = instances.id
        sale_return_billwise_details = web_model.SalesReturnBillWiseDetails.objects.filter(SaleReturnMasterId=pk)
        serialized = SalesReturnBillWiseDetailsSerializer(sale_return_billwise_details,many=True,)

        return serialized.data 


class SaleReturnDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.SaleReturnDetails
        fields = ('id','SaleReturnMasterId','ProductId','Qty','FreeQty','UnitPrice','RateWithTax',
            'CostPerPrice','PriceListId','DiscountAmount','DiscountPerc','GrossAmount','AddlDiscPercent','AddlDiscAmt',
            'TaxableAmount','VATPerc','VATAmount','SGSTPerc','SGSTAmount','CGSTPerc','CGSTAmount',
            'IGSTPerc','IGSTAmount','TAX1Perc','TAX1Amount','TAX2Perc','TAX2Amount','TAX3Perc','TAX3Amount','NetAmount')


class SalesReturnBillWiseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.SalesReturnBillWiseDetails
        fields = ('id','SaleReturnMasterId','Amount','VoucherNumber','VoucherType','Due_Date','Date',
            'DueAmount','Invoice_Amount')


class SaleOrderRestSerializer(serializers.ModelSerializer):

    saleorderdetails = serializers.SerializerMethodField()

    class Meta:
        model = web_model.SaleOrder
        fields = ('id','TransactionId','VanId','Date','LedgerId','PriceCategoryId','SaleAccount','TaxId',
            'TaxType','VATAmount','SGSTAmount','CGSTAmount','IGSTAmount',
            'TAX1Amount','TAX2Amount','TAX3Amount','TotalTax','NetTotal',
            'BillDiscount','GrandTotal','RoundOff','IsInvoiced','status',
            'Address1','Address2','Notes','CustomerName','saleorderdetails')
        

    def get_saleorderdetails(self, instances):
        pk = instances.id
        sale_return_details = web_model.SaleOrderDetails.objects.filter(SaleOrderId=pk)
        serialized = SaleOrderDetailsSerializer(sale_return_details,many=True,)

        return serialized.data 


class SaleOrderDetailsSerializer(serializers.ModelSerializer):
    stockOrderMasterID = serializers.SerializerMethodField()

    class Meta:
        model = web_model.SaleOrderDetails
        fields = ('id','ProductId','Qty','stockOrderMasterID','FreeQty','UnitPrice','RateWithTax','CostPerPrice','PriceListId',
            'DiscountAmount','DiscountPerc','GrossAmount','AddlDiscPercent','AddlDiscAmt','TaxableAmount',
            'VATPerc','VATAmount','SGSTPerc','SGSTAmount','CGSTPerc','CGSTAmount','IGSTPerc','IGSTAmount',
            'TAX1Perc','TAX1Amount','TAX2Perc','TAX2Amount','TAX3Perc','TAX3Amount','NetAmount')

    def get_stockOrderMasterID(self, instances):
        stockOrderMasterID = instances.stockOrderMasterID
        if stockOrderMasterID:
            stockOrderMasterID = stockOrderMasterID
        else:
            stockOrderMasterID = 0
        return stockOrderMasterID 


class VanRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.VanRoute
        fields = ('id','CompanyProductId','RouteId','VanId','RouteName',)



class BillWiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.BillWise
        fields = ('id','CompanyProductId','TransactionID','VoucherType','VoucherNo','Date','Due_Date','Invoice_Amount','Due_Amount','CustomerID','VanId')


class LastSalesPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.LastSalesPrice
        fields = ('id','CompanyProductId','LedgerId','SalePrice','PriceListId','Van_ID')