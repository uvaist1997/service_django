from rest_framework import serializers
from users import models as user_model
from web import models as web_model
from django.utils.text import Truncator


class StockOrderSerializer(serializers.ModelSerializer):

    StockOrderDetail = serializers.SerializerMethodField()

    class Meta:
        model = web_model.StockOrder
        fields = ('id','GUID','CompanyProductId','TransactionID','status','WarehouseTo_id','WarehouseFrom_id','Date','Notes','Total_qty','Total_cost','StockOrderDetail','VanID')
        

    def get_StockOrderDetail(self, instances):
        StockOrderId = instances.id
        stock_order_details = web_model.StockOrderDetail.objects.filter(StockOrderId=StockOrderId)
        serialized = StockOrderDetailSerializer(stock_order_details,many=True,)

        return serialized.data 


class StockOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.StockOrderDetail
        fields = ('id','StockOrderId','ProductId','PricelistId','qty','cost')