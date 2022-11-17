from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from api.v1.general.functions import generate_serializer_errors, call_paginator_all, list_pagination, get_instance
from main.functions import get_auto_id
from web import models as web_model
from api.v1.stockorder import serializers as stock_serializers
from users import models as user_model
from web import models as web_model
from django.shortcuts import render, get_object_or_404


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def stock_orders(request):
    data = request.data
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    companyproduct_ins = None
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName).exists():
        companyproduct_ins = web_model.CompanyProduct.objects.get(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName)
        
        instances = web_model.StockOrder.objects.filter(is_deleted=False,CompanyProductId=companyproduct_ins,status=False)
        print(instances,'ddddddddddddddddddddddddddd')
        serialized = stock_serializers.StockOrderSerializer(instances,many=True)
        data = serialized.data
        if data:
            # data = {
            #   "results": data,
            #   "count": len(instances)
            # }
            return Response(
                {
                    'success': 6000,
                    'data': data,
                    'error': None
                },
                status=status.HTTP_200_OK
            )
    else:
        success = 6001
        error = "error"
        return Response(
            {
                'success': success,
                'data': None,
                'error': error
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_stock_order(request):

    data = request.data
    Stockorders = data["Stockorders"]
    tran_data = []
    if Stockorders:
        print(Stockorders)
        for data in Stockorders:
            pk = data['CompanyProductId']
            CompanyProductId = get_instance(pk,web_model.CompanyProduct)
            Stockorderdetails = data["StockorderDetails"]

            try:
                GUID = data['GUID']
            except:
                GUID = None

            auto_id = get_auto_id(web_model.StockOrder)
            if Stockorderdetails:
                stock_order_instance = web_model.StockOrder.objects.create(
                    auto_id = auto_id,
                    creator = request.user,
                    updater = request.user,
                    CompanyProductId = CompanyProductId,
                    WarehouseTo_id = data['WarehouseTo_id'],
                    WarehouseFrom_id = data['WarehouseFrom_id'],
                    Date = data['Date'],
                    Notes = data['Notes'],
                    Total_qty = data['Total_qty'],
                    Total_cost = data['Total_cost'],
                    TransactionID = data['TransactionID'],
                    VanID = data['VanID'],
                    GUID=GUID
                )
                tran_data.append(stock_order_instance.TransactionID)
                Stockorderdetails = data["StockorderDetails"]

                for Stockorderdetail in Stockorderdetails:

                    ProductId = Stockorderdetail['ProductId']
                    PricelistId = Stockorderdetail['PricelistId']
                    qty = Stockorderdetail['qty']
                    cost = Stockorderdetail['cost']
                    
                    web_model.StockOrderDetail.objects.create(
                        StockOrderId=stock_order_instance,
                        ProductId=ProductId,
                        PricelistId=PricelistId,
                        qty=qty,
                        cost=cost,
                        )

        response_data = {
            "data" : tran_data,
            "StatusCode" : 6000,
            "message" : 'Successfully Created'
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode" : 6001,
            # "message" : generate_serializer_errors(serialized._errors)
             "message" : 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def edit_stock_order(request):
    data = request.data
    pk = data['id']
    # Reciepts = data["Reciepts"]
    if pk:
        # for data in Reciepts:

        if web_model.StockOrder.objects.filter(status=False,pk=pk).exists():
            # instance = get_object_or_404(web_model.Reciept.objects.filter(status=False,CompanyProductId=CompanyProductId))
            instance = get_object_or_404(web_model.StockOrder.objects.filter(status=False,pk=pk))           
            instance.status = True
            instance.save()

            response_data = {
                "StatusCode" : 6000,
                "message" : 'Successfully Updated'
            }

        return Response(response_data, status=status.HTTP_200_OK)
            
    else:
        response_data = {
            "StatusCode" : 6001,
            # "message" : generate_serializer_errors(serialized._errors)
             "message" : 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)