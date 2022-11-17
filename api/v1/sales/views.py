from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from api.v1.general.functions import bulkCreate, generate_serializer_errors, call_paginator_all, list_pagination, get_instance, convertOrderdDict
from main.functions import get_auto_id
from web import models as web_model
from api.v1.sales import serializers as sale_serializers
from users import models as user_model
from django.shortcuts import render, get_object_or_404
import datetime
from django.db import transaction, IntegrityError
import re
import sys
import os


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_sale_products(request):
    data = request.data
    print(data, '@@@@@@@@@########')
    CompanyProductId = data['CompanyProductId']
    if CompanyProductId:
        # for data in saleproducts:
        instances = web_model.SaleProduct.objects.filter(
            is_deleted=False, CompanyProductId=CompanyProductId)
        serialized = sale_serializers.SaleProductSerializer(
            instances, many=True)
        data = serialized.data

        data = {
            "results": data,
            "count": len(instances)
        }
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
@transaction.atomic
def create_sale_product(request):
    data = request.data
    try:
        with transaction.atomic():
            print("KAYARYYYYYYYYYYYYYYYYYYYYYY")
            today = datetime.datetime.now()
            Saleproduct = data["Saleproduct"]
            companyproduct_ins = None
            CompanyID = data['CompanyID']
            CompanyProductName = data['CompanyProductName']

            if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
                companyproduct_ins = web_model.CompanyProduct.objects.get(
                    CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
                instances = web_model.SaleProduct.objects.filter(
                    CompanyProductId=companyproduct_ins)
                instances.delete()

            if Saleproduct:
                if companyproduct_ins:
                    auto_id = get_auto_id(web_model.SaleProduct)
                    count = 0
                    instances_arr = []
                    for data in Saleproduct:                        
                        ProductId = data['ProductID']
                        VatId = data['VAT_ID']
                        GstId = data['GST_ID']
                        Tax1Id = data['Tax1_ID']
                        Tax2Id = data['Tax2_ID']
                        Tax3Id = data['Tax3_ID']
                        Productcode = data['ProductCode']
                        Productname = data['ProductName']

                        # SyncDate = data['SyncDate']
                        try:
                            Displayname = data['DisplayName']
                        except:
                            Displayname = None
                        try:
                            Description = data['Description']
                        except:
                            Description = None
                        try:
                            BranchId = data['BranchID']
                        except:
                            BranchId = 0
                        try:
                            minimumSalesPrice = data['minimumSalesPrice']
                        except:
                            minimumSalesPrice = 0
                        # auto_id = get_auto_id(web_model.SaleProduct)

                        # web_model.SaleProduct.objects.create(
                        #     auto_id=get_auto_id(web_model.SaleProduct),
                        #     creator=request.user,
                        #     updater=request.user,
                        #     CompanyProductId=companyproduct_ins,
                        #     ProductId=ProductId,
                        #     BranchId=BranchId,
                        #     VatId=VatId,
                        #     GstId=GstId,
                        #     Tax1Id=Tax1Id,
                        #     Tax2Id=Tax2Id,
                        #     Tax3Id=Tax3Id,
                        #     Productcode=Productcode,
                        #     Productname=Productname,
                        #     minimumSalesPrice=minimumSalesPrice,
                        #     Displayname=Displayname,
                        #     Description=Description,
                        #     SyncDate=today,
                        # )
                        instances_arr.append({
                            "auto_id":int(auto_id)+count,
                            "ProductId":ProductId,
                            "BranchId":BranchId,
                            "VatId":VatId,
                            "GstId":GstId,
                            "Tax1Id":Tax1Id,
                            "Tax2Id":Tax2Id,
                            "Tax3Id":Tax3Id,
                            "Productcode":Productcode,
                            "Productname":Productname,
                            "minimumSalesPrice":minimumSalesPrice,
                            "Displayname":Displayname,
                            "Description":Description,
                            "SyncDate":today,
                                                    
                        })
                        count += 1
                    bulkCreate(instances_arr,companyproduct_ins,request,web_model.SaleProduct)


                    response_data = {
                        "StatusCode": 6000,
                        "data": data,
                        "message": 'Successfully Created'
                    }

                    return Response(response_data, status=status.HTTP_200_OK)

                else:
                    response_data = {
                        "StatusCode": 6001,
                        "message": 'company product is not exist!'
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
                # response_data = {
                #   "StatusCode" : 6000,
                #   "data" : Saleproduct,
                #   "message" : 'Successfully Created'
                # }

                # return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                    # "message" : generate_serializer_errors(serialized._errors)
                    "message": 'Data does not exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_descrb = str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
        print(err_descrb)
        response_data = {
            "StatusCode": 6001,
            "message": "some error occured..please try again"
        }
        user_model.ActivityLog.objects.create(
            CompanyId=data['CompanyID'],
            log_type="create sale product",
            message=str(e),
            description=err_descrb,

        )

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_sale_product(request):
    data = request.data
    Saleproduct = data["Saleproduct"]
    if Saleproduct:
        for data in Saleproduct:
            CompanyProductId = data['CompanyProductId']
            ProductId = data['ProductId']
            if web_model.SaleProduct.objects.filter(ProductId=ProductId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SaleProduct.objects.filter(
                    ProductId=ProductId, CompanyProductId=CompanyProductId))
                instance.delete()

        for data in Saleproduct:
            CompanyProductId = data['CompanyProductId']
            ProductId = data['ProductId']
            BranchId = data['BranchId']
            Productcode = data['Productcode']
            Productname = data['Productname']
            SyncDate = data['SyncDate']
            try:
                Description = data['Description']
            except:
                Description = None
            try:
                Displayname = data['Displayname']
            except:
                Displayname = None

            if web_model.SaleProduct.objects.filter(is_deleted=False, ProductId=ProductId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SaleProduct.objects.filter(
                    is_deleted=False, ProductId=ProductId, CompanyProductId=CompanyProductId))
            # instance.ProductId = ProductId
            instance.BranchId = BranchId
            instance.Productcode = Productcode
            instance.Productname = Productname
            instance.Displayname = Displayname
            instance.Description = Description
            instance.SyncDate = SyncDate
            instance.save()

        response_data = {
            "StatusCode": 6000,
            "data": Saleproduct,
            "message": 'Successfully Updated'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def delete_sale_products(request):
    data = request.data
    Saleproduct = data["Saleproduct"]
    if Saleproduct:
        for data in Saleproduct:
            instance = None
            CompanyProductId = data['CompanyProductId']
            ProductId = data['ProductId']
            if web_model.SaleProduct.objects.filter(ProductId=ProductId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SaleProduct.objects.filter(
                    ProductId=ProductId, CompanyProductId=CompanyProductId))
                instance.delete()

        response_data = {
            "StatusCode": 6000,
            "message": "Sale Products Deleted Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Saleproduct is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_sale_price(request):
    data = request.data
    pk = data['CompanyProductId']
    instances = web_model.SalePrice.objects.filter(
        is_deleted=False, CompanyProductId=pk)

    serialized = sale_serializers.SalePriceSerializer(instances, many=True)
    data = serialized.data
    if data:
        data = {
            "results": data,
            "count": len(instances)
        }
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
@transaction.atomic
def create_sale_price(request):
    data = request.data
    try:
        with transaction.atomic():
            today = datetime.datetime.now()
            Saleprice = data["Saleprice"]
            CompanyID = data['CompanyID']
            CompanyProductName = data['CompanyProductName']
            companyproduct_ins =None
            if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
                companyproduct_ins = web_model.CompanyProduct.objects.get(
                    CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
                instances = web_model.SalePrice.objects.filter(
                    CompanyProductId=companyproduct_ins)
                # for i in instances:
                instances.delete()

            if Saleprice:
                count = 0
                instances_arr = []
                if companyproduct_ins:
                    auto_id=get_auto_id(web_model.SalePrice)
                    for data in Saleprice:                   
                    
                        try:
                            Barcode = data['Barcode']
                        except:
                            Barcode = None

                        try:
                            IsDefault = data['IsDefault']
                        except:
                            IsDefault = False

                        # web_model.SalePrice.objects.create(
                        #     auto_id=get_auto_id(web_model.SalePrice),
                        #     creator=request.user,
                        #     updater=request.user,
                        #     CompanyProductId=companyproduct_ins,
                        #     ProductId=data['ProductID'],
                        #     PriceListId=data['PriceListID'],
                        #     BranchId=data['BranchID'],
                        #     UnitName=data['UnitName'],
                        #     SalePrice=data['SalesPrice'],
                        #     PurchasePrice=data['PurchasePrice'],
                        #     SalePrice1=data['SalesPrice1'],
                        #     SalePrice2=data['SalesPrice2'],
                        #     SalePrice3=data['SalesPrice3'],
                        #     MultiFactor=data['MultiFactor'],
                        #     AutoBarcode=data['AutoBarcode'],
                        #     IsDefault=IsDefault,
                        #     Barcode=Barcode,
                        #     SyncDate=today
                        # )
                        instances_arr.append({
                            "auto_id":int(auto_id)+count,
                            "ProductId":data['ProductID'],
                            "PriceListId":data['PriceListID'],
                            "BranchId":data['BranchID'],
                            "UnitName":data['UnitName'],
                            "SalePrice":data['SalesPrice'],
                            "PurchasePrice":data['PurchasePrice'],
                            "SalePrice1":data['SalesPrice1'],
                            "SalePrice2":data['SalesPrice2'],
                            "SalePrice3":data['SalesPrice3'],
                            "MultiFactor":data['MultiFactor'],
                            "AutoBarcode":data['AutoBarcode'],
                            "IsDefault":IsDefault,
                            "Barcode":Barcode,
                            "SyncDate":today                            
                        })
                        count += 1
                    bulkCreate(instances_arr,companyproduct_ins,request,web_model.SalePrice)
                    response_data = {
                        "StatusCode": 6000,
                        "message": 'Successfully Created'
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        "StatusCode": 6001,
                        "message": 'product is not exist!'
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                    # "message" : generate_serializer_errors(serialized._errors)
                    "message": 'Data does not exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_descrb = str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
        response_data = {
            "StatusCode": 6001,
            "message": "some error occured..please try again"
        }
        user_model.ActivityLog.objects.create(
            CompanyId=data['CompanyID'],
            log_type="create sale product",
            message=str(e),
            description=err_descrb,

        )

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_sale_price(request):
    data = request.data
    Saleprice = data["Saleprice"]
    if Saleprice:
        for data in Saleprice:
            CompanyProductId = data['CompanyProductId']
            ProductId = data['ProductId']
            PriceListId = data['PriceListId']
            BranchId = data['BranchId']
            UnitName = data['UnitName']
            SalePrice1 = data['SalePrice1']
            SalePrice2 = data['SalePrice2']
            SalePrice3 = data['SalePrice3']
            MultiFactor = data['MultiFactor']
            AutoBarcode = data['AutoBarcode']
            SyncDate = data['SyncDate']
            try:
                Barcode = data['Barcode']
            except:
                Barcode = None

            if web_model.SalePrice.objects.filter(is_deleted=False, ProductId=ProductId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SalePrice.objects.filter(
                    is_deleted=False, ProductId=ProductId, CompanyProductId=CompanyProductId))
            instance.BranchId = BranchId
            instance.UnitName = UnitName
            instance.SalePrice1 = SalePrice1
            instance.SalePrice2 = SalePrice2
            instance.SalePrice3 = SalePrice3
            instance.MultiFactor = MultiFactor
            instance.AutoBarcode = AutoBarcode
            instance.SyncDate = SyncDate
            instance.Barcode = Barcode
            instance.save()

        response_data = {
            "StatusCode": 6000,
            "data": Saleprice,
            "message": 'Successfully Updated'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def delete_sale_price(request):
    data = request.data
    Saleprice = data["Saleprice"]
    if Saleprice:
        for data in Saleprice:
            instance = None
            CompanyProductId = data['CompanyProductId']
            ProductId = data['ProductId']
            if web_model.SalePrice.objects.filter(ProductId=ProductId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SalePrice.objects.filter(
                    ProductId=ProductId, CompanyProductId=CompanyProductId))
                instance.delete()

        response_data = {
            "StatusCode": 6000,
            "message": "Sale Price Deleted Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Sale Price is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_sale_account_ledgers(request):
    data = request.data
    pk = data['CompanyProductId']
    VanId = data['VanId']
    instances = None
    van_routes = web_model.VanRoute.objects.filter(
        is_deleted=False, CompanyProductId=pk, VanId=VanId)
    ledger_arr = []
    ledger_dic = {}
    for i in van_routes:
        instances = web_model.SaleAccountLedger.objects.filter(
            is_deleted=False, RouteId=i.RouteId, CompanyProductId=pk)
        serialized = sale_serializers.SaleAccountLedgerSerializer(
            instances, many=True)
        data = serialized.data
        list_item = convertOrderdDict(data)
        for i in list_item:
            print(i['RouteId'], "======================")
            dic = {
                "id": i['id'],
                "CrNum": i['CrNum'],
                "LedgerCode": i['LedgerCode'],
                "Credit_Limit": i['Credit_Limit'],
                "Balance": i['Balance'],
                "PriceCategoryID": i['PriceCategoryID'],
                "CompanyProductId": i['CompanyProductId'],
                "LedgerId": i['LedgerId'],
                "PartyName": i['PartyName'],
                "DisplayName": i['DisplayName'],
                "VatNum": i['VatNum'],
                "GstNum": i['GstNum'],
                "Tax1Number": i['Tax1Number'],
                "Tax2Number": i['Tax2Number'],
                "Tax3Number": i['Tax3Number'],
                "RouteId": i['RouteId'],
                "BillwiseApplicable": i['BillwiseApplicable'],
                "GroupId": i['GroupId'],
                "PlaceofSupply": i['PlaceofSupply'],

                "Address1": i['Address1'],
                "City": i['City'],
                "State": i['State'],
                "Country": i['Country'],
                "BuildingNumber": i['BuildingNumber'],
                "District": i['District'],
                "StreetName": i['StreetName'],
                "AdditionalNo": i['AdditionalNo']
            }
            ledger_arr.append(dic)
    if ledger_arr:
        data = {
            "results": ledger_arr,
        }
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
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_sale_account_ledger(request):

    data = request.data
    Saleaccountledger = data["Saleaccountledger"]
    comp_instance = None
    if Saleaccountledger:
        CompanyID = data['CompanyID']
        CompanyProductName = data['CompanyProductName']
        if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
            comp_instance = web_model.CompanyProduct.objects.get(
                CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
            instances = web_model.SaleAccountLedger.objects.filter(
                CompanyProductId=comp_instance)
            instances.delete()

        if comp_instance:
            count = 0
            instances_arr = []
            for data in Saleaccountledger:
                auto_id = get_auto_id(web_model.SaleAccountLedger)
                try:
                    VATNumber = data['VATNumber']
                except:
                    VATNumber = ""
                try:
                    GSTNumber = data['GSTNumber']
                except:
                    GSTNumber = ""
                try:
                    Tax1Number = data['Tax1Number']
                except:
                    Tax1Number = ""
                try:
                    Tax2Number = data['Tax2Number']
                except:
                    Tax2Number = ""
                try:
                    Tax3Number = data['Tax3Number']
                except:
                    Tax3Number = ""
                try:
                    CRNumber = data['CRNumber']
                except:
                    CRNumber = ""
                try:
                    LedgerCode = data['LedgerCode']
                except:
                    LedgerCode = ""
                try:
                    PlaceofSupply = data['PlaceofSupply']
                except:
                    PlaceofSupply = ""

                try:
                    Address1 = data['Address1']
                except:
                    Address1 = ""
                try:
                    City = data['City']
                except:
                    City = ""
                try:
                    State = data['State']
                except:
                    State = ""
                try:
                    Country = data['Country']
                except:
                    Country = ""
                try:
                    BuildingNumber = data['BuildingNumber']
                except:
                    BuildingNumber = ""
                try:
                    District = data['District']
                except:
                    District = ""
                try:
                    StreetName = data['StreetName']
                except:
                    StreetName = ""
                try:
                    AdditionalNo = data['AdditionalNo']
                except:
                    AdditionalNo = ""

                # web_model.SaleAccountLedger.objects.create(
                #     auto_id=auto_id,
                #     creator=request.user,
                #     updater=request.user,
                #     CompanyProductId=comp_instance,
                #     PriceCategoryID=data['PriceCategoryID'],
                #     LedgerId=data['LedgerID'],
                #     PartyName=data['PartyName'],
                #     DisplayName=data['DisplayName'],
                #     VatNum=VATNumber,
                #     GstNum=GSTNumber,
                #     Tax1Number=Tax1Number,
                #     Tax2Number=Tax2Number,
                #     Tax3Number=Tax3Number,
                #     LedgerCode=LedgerCode,
                #     RouteId=data['RouteID'],
                #     CrNum=CRNumber,
                #     GroupId=data['GroupID'],
                #     Credit_Limit=data['Credit_Limit'],
                #     BillwiseApplicable=data['BillwiseApplicable'],
                #     Balance=data['Balance'],
                #     PlaceofSupply=PlaceofSupply,
                #     Address1=Address1,
                #     City=City,
                #     State=State,
                #     Country=Country,
                #     BuildingNumber=BuildingNumber,
                #     District=District,
                #     StreetName=StreetName,
                #     AdditionalNo=AdditionalNo,
                # )
                instances_arr.append({
                    "auto_id":int(auto_id)+count,
                    "PriceCategoryID":data['PriceCategoryID'],
                    "LedgerId":data['LedgerID'],
                    "PartyName":data['PartyName'],
                    "DisplayName":data['DisplayName'],
                    "VatNum":VATNumber,
                    "GstNum":GSTNumber,
                    "Tax1Number":Tax1Number,
                    "Tax2Number":Tax2Number,
                    "Tax3Number":Tax3Number,
                    "LedgerCode":LedgerCode,
                    "RouteId":data['RouteID'],
                    "CrNum":CRNumber,
                    "GroupId":data['GroupID'],
                    "Credit_Limit":data['Credit_Limit'],
                    "BillwiseApplicable":data['BillwiseApplicable'],
                    "Balance":data['Balance'],
                    "PlaceofSupply":PlaceofSupply,
                    "Address1":Address1,
                    "City":City,
                    "State":State,
                    "Country":Country,
                    "BuildingNumber":BuildingNumber,
                    "District":District,
                    "StreetName":StreetName,
                    "AdditionalNo":AdditionalNo,
                                            
                })
                count += 1
            bulkCreate(instances_arr,comp_instance,request,web_model.SaleAccountLedger)

            response_data = {
                "StatusCode": 6000,
                "message": 'Successfully Created'
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "StatusCode": 6001,
                "message": 'product is not exist!'
            }

            return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_sale_account_ledger(request):
    data = request.data
    Saleaccountledger = data["Saleaccountledger"]
    if Saleaccountledger:
        for data in Saleaccountledger:
            CompanyProductId = data['CompanyProductId']
            LedgerId = data['LedgerId']
            PartyName = data['PartyName']
            RouteId = data['RouteId']
            GroupId = data['GroupId']

            DisplayName = data['DisplayName']
            VatNum = data['VatNum']
            GstNum = data['GstNum']
            Tax1Number = data['Tax1Number']
            Tax2Number = data['Tax2Number']
            Tax3Number = data['Tax3Number']
            CrNum = data['CrNum']
            # try:
            #   Barcode = data['Barcode']
            # except:
            #   Barcode = None

            if web_model.SaleAccountLedger.objects.filter(is_deleted=False, LedgerId=LedgerId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SaleAccountLedger.objects.filter(
                    is_deleted=False, LedgerId=LedgerId, CompanyProductId=CompanyProductId))
            instance.LedgerId = LedgerId
            instance.PartyName = PartyName
            instance.RouteId = RouteId
            instance.GroupId = GroupId
            instance.DisplayName = DisplayName
            instance.VatNum = VatNum
            instance.GstNum = GstNum
            instance.Tax1Number = Tax1Number
            instance.Tax2Number = Tax2Number
            instance.Tax3Number = Tax3Number
            instance.CrNum = CrNum
            instance.save()

        response_data = {
            "StatusCode": 6000,
            "data": Saleaccountledger,
            "message": 'Successfully Updated'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def delete_sale_account_ledger(request):
    data = request.data
    Saleaccountledger = data["Saleaccountledger"]
    if Saleaccountledger:
        for data in Saleaccountledger:
            instance = None
            CompanyProductId = data['CompanyProductId']
            LedgerId = data['LedgerId']
            if web_model.SaleAccountLedger.objects.filter(LedgerId=LedgerId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SaleAccountLedger.objects.filter(
                    LedgerId=LedgerId, CompanyProductId=CompanyProductId))
                instance.delete()

        response_data = {
            "StatusCode": 6000,
            "message": "Sale Account Ledger Deleted Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Sale Account Ledger is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_warehouse_stocks(request):
    data = request.data
    CompanyProductId = data['CompanyProductId']
    WarehouseId = data['WarehouseId']

    instances = web_model.WarehouseStock.objects.filter(
        is_deleted=False, CompanyProductId=CompanyProductId, WarehouseId=WarehouseId)
    serialized = sale_serializers.WarehouseStockSerializer(
        instances, many=True)
    data = serialized.data
    if data:
        data = {
            "results": data,
            "count": len(instances)
        }
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
def list_warehouse_with_id(request):
    data = request.data
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    WarehouseId = data['WarehouseID']
    comp_instance = None
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
    instances = web_model.WarehouseStock.objects.filter(
        is_deleted=False, CompanyProductId=comp_instance, WarehouseId=WarehouseId)
    serialized = sale_serializers.WarehouseStockSerializer(
        instances, many=True)
    data = serialized.data
    if data:
        data = {
            "results": data,
            "count": len(instances)
        }
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
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def create_warehouse_stock(request):

    data = request.data
    try:
        with transaction.atomic():
            Warehousestock = data["Warehousestock"]
            instance = None
            CompanyID = data['CompanyID']
            CompanyProductName = data['CompanyProductName']
            companyproduct_ins = None
            if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
                companyproduct_ins = web_model.CompanyProduct.objects.get(
                    CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
                instances = web_model.WarehouseStock.objects.filter(
                    CompanyProductId=companyproduct_ins)
                instances.delete()

                if Warehousestock and companyproduct_ins:
                    auto_id = get_auto_id(web_model.WarehouseStock)
                    count = 0
                    instances_arr = []
                    for data in Warehousestock:
                        # web_model.WarehouseStock.objects.create(
                        #     auto_id=auto_id,
                        #     creator=request.user,
                        #     updater=request.user,
                        #     CompanyProductId=companyproduct_ins,
                        #     ProductId=data['ProductID'],
                        #     PriceListId=data['PriceListID'],
                        #     WarehouseId=data['WarehouseID'],
                        #     Stock=data['Stock'],
                        # )
                        instances_arr.append({
                            "auto_id":int(auto_id)+count,
                            "ProductId":data['ProductID'],
                            "PriceListId":data['PriceListID'],
                            "WarehouseId":data['WarehouseID'],
                            "Stock":data['Stock'],
                                                    
                        })
                        count += 1
                    bulkCreate(instances_arr,companyproduct_ins,request,web_model.WarehouseStock)


                    response_data = {
                        "StatusCode": 6000,
                        "message": 'Successfully Created'
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        "StatusCode": 6001,
                        # "message" : generate_serializer_errors(serialized._errors)
                        "message": 'Data does not exists'
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": 'CompanyProduct does not exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_descrb = str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
        response_data = {
            "StatusCode": 6001,
            "message": "some error occured..please try again"
        }
        user_model.ActivityLog.objects.create(
            CompanyId=data['CompanyID'],
            log_type="create sale product",
            message=str(e),
            description=err_descrb,

        )

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_warehouse_stock(request):
    data = request.data
    Warehousestock = data["Warehousestock"]
    if Warehousestock:
        for data in Warehousestock:
            CompanyProductId = data['CompanyProductId']
            ProductId = data['ProductId']
            PriceListId = data['PriceListId']
            WarehouseId = data['WarehouseId']
            Stock = data['Stock']

            if web_model.WarehouseStock.objects.filter(is_deleted=False, ProductId=ProductId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.WarehouseStock.objects.filter(
                    is_deleted=False, ProductId=ProductId, CompanyProductId=CompanyProductId))
            instance.PriceListId = PriceListId
            instance.WarehouseId = WarehouseId
            instance.Stock = Stock
            instance.save()

        response_data = {
            "StatusCode": 6000,
            "data": Warehousestock,
            "message": 'Successfully Updated'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def delete_warehouse_stock(request):
    data = request.data
    Warehousestock = data["Warehousestock"]
    if Warehousestock:
        for data in Warehousestock:
            instance = None
            CompanyProductId = data['CompanyProductId']
            ProductId = data['ProductId']
            if web_model.WarehouseStock.objects.filter(ProductId=ProductId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.WarehouseStock.objects.filter(
                    ProductId=ProductId, CompanyProductId=CompanyProductId))
                instance.delete()

        response_data = {
            "StatusCode": 6000,
            "message": "Warehouse Stock Deleted Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Warehouse Stock is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_expense_ledgers(request):
    data = request.data
    pk = data['CompanyProductId']
    VanId = data['VanId']
    instances = web_model.ExpenseLedger.objects.filter(
        is_deleted=False, CompanyProductId=pk, VanId=VanId)
    serialized = sale_serializers.ExpenseLedgerSerializer(instances, many=True)
    data = serialized.data
    if data:
        data = {
            "results": data,
        }
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
def create_expense_ledger(request):
    data = request.data
    Expenseledger = data["Expenseledger"]

    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        instances = web_model.ExpenseLedger.objects.filter(
            CompanyProductId=comp_instance)
        for i in instances:
            i.delete()

    if Expenseledger:
        for data in Expenseledger:
            web_model.ExpenseLedger.objects.create(
                auto_id=get_auto_id(web_model.ExpenseLedger),
                creator=request.user,
                updater=request.user,
                LedgerId=data['LedgerID'],
                LedgerName=data['LedgerName'],
                VanId=data['Van_ID'],
                CompanyProductId=comp_instance
            )

        response_data = {
            "StatusCode": 6000,
            "message": 'Successfully Created'
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
# def edit_expense_ledger(request):
#   data = request.data
#   Expenseledger = data["Expenseledger"]
#   if Expenseledger:
#       for data in Expenseledger:
#           CompanyProductId = data['CompanyProductId']
#           LedgerName = data['LedgerName']
#           LedgerId = data['LedgerId']

#           if web_model.ExpenseLedger.objects.filter(is_deleted=False,LedgerId=LedgerId,CompanyProductId=CompanyProductId).exists():
#               instance = get_object_or_404(web_model.ExpenseLedger.objects.filter(is_deleted=False,LedgerId=LedgerId,CompanyProductId=CompanyProductId))
#           instance.LedgerName = LedgerName
#           # instance.LedgerId = LedgerId
#           instance.save()

#       response_data = {
#           "StatusCode" : 6000,
#           "data" : Expenseledger,
#           "message" : 'Successfully Updated'
#       }

#       return Response(response_data, status=status.HTTP_200_OK)

#   else:
#       response_data = {
#           "StatusCode" : 6001,
#           # "message" : generate_serializer_errors(serialized._errors)
#            "message" : 'Data does not exists'
#       }

#       return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['DELETE'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
# def delete_expense_ledger(request):
#   data = request.data
#   Expenseledger = data["Expenseledger"]
#   if Expenseledger:
#       for data in Expenseledger:
#           instance = None
#           CompanyProductId = data['CompanyProductId']
#           LedgerId = data['LedgerId']
#           if web_model.ExpenseLedger.objects.filter(LedgerId=LedgerId,CompanyProductId=CompanyProductId).exists():
#               instance = get_object_or_404(web_model.ExpenseLedger.objects.filter(LedgerId=LedgerId,CompanyProductId=CompanyProductId))
#               instance.delete()

#       response_data = {
#           "StatusCode" : 6000,
#           "message" : "Warehouse Stock Deleted Successfully!"
#       }

#       return Response(response_data, status=status.HTTP_200_OK)

#   response_data = {
#       "StatusCode" : 6001,
#       "message" : "Warehouse Stock is not exists!"
#   }

#   return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def last_sale_prices(request):
    data = request.data
    CompanyProductId = data["CompanyProductId"]
    try:
        Van_ID = data["VanId"]
    except:
        Van_ID = None
    instances = web_model.LastSalesPrice.objects.filter(
        is_deleted=False, CompanyProductId=CompanyProductId, Van_ID=Van_ID)
    serialized = sale_serializers.LastSalesPriceSerializer(
        instances, many=True)
    data = serialized.data
    if data:
        data = {
            "results": data,
            "count": len(instances)
        }
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
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_last_sale_prices(request):

    data = request.data
    Lastsalesprice = data["Lastsalesprice"]
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    comp_instance = None
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        instances = web_model.LastSalesPrice.objects.filter(
            CompanyProductId=comp_instance)
        instances.delete()

    if Lastsalesprice:
        count = 0
        instances_arr = []
        auto_id = get_auto_id(web_model.LastSalesPrice)
        for i in Lastsalesprice:
            # web_model.LastSalesPrice.objects.create(
            #     auto_id=auto_id,
            #     creator=request.user,
            #     updater=request.user,
            #     CompanyProductId=comp_instance,
            #     LedgerId=data['LedgerId'],
            #     SalePrice=data['SalePrice'],
            #     PriceListId=data['PriceListId'],
            #     Van_ID=data['Van_ID'],
            # )
            print(i['Van_ID'])
            instances_arr.append({
                "auto_id":int(auto_id)+count,
                "LedgerId":i['LedgerId'],
                "SalePrice":i['SalePrice'],
                "PriceListId":i['PriceListId'],
                "Van_ID":i['Van_ID'],
                                        
            })
            count += 1
        bulkCreate(instances_arr,comp_instance,request,web_model.LastSalesPrice)


        response_data = {
            "StatusCode": 6000,
            "data": Lastsalesprice,
            "message": 'Successfully Created'
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_last_sale_prices(request):
    data = request.data
    Lastsalesprice = data["Lastsalesprice"]
    if Lastsalesprice:
        for data in Lastsalesprice:
            CompanyProductId = data['CompanyProductId']
            LedgerId = data['LedgerId']
            SalePrice = data['SalePrice']
            PriceListId = data['PriceListId']

            # try:
            #   Barcode = data['Barcode']
            # except:
            #   Barcode = None

            if web_model.LastSalesPrice.objects.filter(is_deleted=False, LedgerId=LedgerId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.LastSalesPrice.objects.filter(
                    is_deleted=False, LedgerId=LedgerId, CompanyProductId=CompanyProductId))
            instance.SalePrice = SalePrice
            instance.PriceListId = PriceListId
            instance.save()

        response_data = {
            "StatusCode": 6000,
            "data": Lastsalesprice,
            "message": 'Successfully Updated'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def delete_last_sale_prices(request):
    data = request.data
    Lastsalesprice = data["Lastsalesprice"]
    if Lastsalesprice:
        for data in Lastsalesprice:
            instance = None
            CompanyProductId = data['CompanyProductId']
            LedgerId = data['LedgerId']
            if web_model.LastSalesPrice.objects.filter(LedgerId=LedgerId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.LastSalesPrice.objects.filter(
                    LedgerId=LedgerId, CompanyProductId=CompanyProductId))
                instance.delete()

        response_data = {
            "StatusCode": 6000,
            "message": "Sale Account Ledger Deleted Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Last Sale Price is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def sale_routes(request):
    instances = web_model.SaleRoute.objects.filter(is_deleted=False)
    serialized = sale_serializers.SaleRouteSerializer(instances, many=True)
    data = serialized.data
    if data:
        data = {
            "results": data,
            "count": len(instances)
        }
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
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_sale_route(request):

    data = request.data
    Saleroute = data["Saleroute"]
    comp_instance = None
    if Saleroute:
        CompanyID = data['CompanyID']
        CompanyProductName = data['CompanyProductName']
        if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
            comp_instance = web_model.CompanyProduct.objects.get(
                CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        for data in Saleroute:
            auto_id = get_auto_id(web_model.SaleRoute)
            # pk = data['CompanyProductId']
            # CompanyProductId = get_instance(pk,web_model.CompanyProduct)

            web_model.SaleRoute.objects.create(
                auto_id=auto_id,
                creator=request.user,
                updater=request.user,
                CompanyProductId=comp_instance,
                RouteId=data['RouteId'],
                RouteName=data['RouteName'],
            )

        response_data = {
            "StatusCode": 6000,
            "message": 'Successfully Created'
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_sale_route(request):
    data = request.data
    Saleroute = data["Saleroute"]
    if Saleroute:
        for data in Saleroute:
            CompanyProductId = data['CompanyProductId']
            RouteId = data['RouteId']
            RouteName = data['RouteName']

            # try:
            #   Barcode = data['Barcode']
            # except:
            #   Barcode = None

            if web_model.SaleRoute.objects.filter(is_deleted=False, RouteId=RouteId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SaleRoute.objects.filter(
                    is_deleted=False, RouteId=RouteId, CompanyProductId=CompanyProductId))
            # instance.RouteId = RouteId
            instance.RouteName = RouteName
            instance.save()

        response_data = {
            "StatusCode": 6000,
            "data": Saleroute,
            "message": 'Successfully Updated'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def delete_sale_route(request):
    data = request.data
    Saleroute = data["Saleroute"]
    if Saleroute:
        for data in Saleroute:
            instance = None
            CompanyProductId = data['CompanyProductId']
            RouteId = data['RouteId']
            if web_model.SaleRoute.objects.filter(RouteId=RouteId, CompanyProductId=CompanyProductId).exists():
                instance = get_object_or_404(web_model.SaleRoute.objects.filter(
                    RouteId=RouteId, CompanyProductId=CompanyProductId))
                instance.delete()

        response_data = {
            "StatusCode": 6000,
            "message": "Sale Account Ledger Deleted Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Last Sale Price is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_transaction_types(request):
    data = request.data
    # pk = data['CompanyProductId']
    pk = request.GET.get("CompanyProductId")
    instances = web_model.TransactionType.objects.filter(
        is_deleted=False, CompanyProductId=pk)
    serialized = sale_serializers.TransactionTypeSerializer(
        instances, many=True)
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
def create_transaction_type(request):
    today = datetime.datetime.now()

    data = request.data
    Transactiontype = data["Transactiontype"]
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    comp_instance = None
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        instances = web_model.TransactionType.objects.filter(
            CompanyProductId=comp_instance)
        instances.delete()

    if Transactiontype and comp_instance:
        count = 0
        instances_arr = []
        auto_id = get_auto_id(web_model.TransactionType)
        for data in Transactiontype:           
            # web_model.TransactionType.objects.create(
            #     auto_id=auto_id,
            #     creator=request.user,
            #     updater=request.user,
            #     TransactionTypeId=data['TransactionTypeID'],
            #     MasterTypeId=data['MasterTypeID'],
            #     TransactionTypeName=data['TransactionTypeName'],
            #     SyncDate=today,
            #     CompanyProductId=comp_instance
            # )
            instances_arr.append({
                "auto_id":int(auto_id)+count,
                "TransactionTypeId":data['TransactionTypeID'],
                "MasterTypeId":data['MasterTypeID'],
                "TransactionTypeName":data['TransactionTypeName'],
                "SyncDate":today,
                                        
            })
            count += 1
        bulkCreate(instances_arr,comp_instance,request,web_model.TransactionType)


        response_data = {
            "StatusCode": 6000,
            "message": 'Successfully Created'
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_van_routes(request):
    data = request.data
    pk = data['CompanyProductId']
    VanId = data['VanId']
    instances = web_model.VanRoute.objects.filter(
        is_deleted=False, CompanyProductId=pk, VanId=VanId)
    serialized = sale_serializers.VanRouteSerializer(instances, many=True)
    data = serialized.data
    if data:
        data = {
            "results": data,
            "count": len(instances)
        }
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
def create_van_route(request):
    data = request.data
    Vanroute = data["Vanroute"]
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    comp_instance = None
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        instances = web_model.VanRoute.objects.filter(
            CompanyProductId=comp_instance, is_deleted=False)
        instances.delete()

    if Vanroute and comp_instance:
        auto_id = get_auto_id(web_model.VanRoute)
        count = 0
        instances_arr = []
        for data in Vanroute:
            # web_model.VanRoute.objects.create(
            #     auto_id=get_auto_id(web_model.VanRoute),
            #     creator=request.user,
            #     updater=request.user,
            #     CompanyProductId=comp_instance,
            #     RouteId=data['RouteID'],
            #     RouteName=data['RouteName'],
            #     VanId=data['Van_ID']
            # )
            instances_arr.append({
                "auto_id":int(auto_id)+count,
                "RouteId":data['RouteID'],
                "RouteName":data['RouteName'],
                "VanId":data['Van_ID']
                                        
            })
            count += 1
        bulkCreate(instances_arr,comp_instance,request,web_model.VanRoute)


        response_data = {
            "StatusCode": 6000,
            "message": 'Successfully Created'
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def update_sale_status(request):
    data = request.data
    MasterID = data['MasterID']
    if MasterID:
        if web_model.SaleMaster.objects.filter(pk=MasterID).exists():
            print("YESSSSSSS")
            instance = web_model.SaleMaster.objects.get(pk=MasterID)
            instance.status = True
            instance.save()

            return Response(
                {
                    'success': 6000,
                    "message": "Sale status updated successfully!!!",
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
                    'message': error
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        success = 6001
        error = "error"
        return Response(
            {
                'success': success,
                'data': None,
                'message': "MasterID is "
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_sales(request):
    data = request.data
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    comp_instance = None
    print(CompanyID)
    print(CompanyProductName)
    s = web_model.CompanyProduct.objects.filter(
        ProductId__Name=CompanyProductName, CompanyId__pk=CompanyID)
    print(s, 's')
    if web_model.CompanyProduct.objects.filter(ProductId__Name=CompanyProductName).exists():
        print("YESSSSSSS")
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)

    instances = web_model.SaleMaster.objects.filter(
        CompanyProductId=comp_instance, status=False, is_deleted=False)
    print(comp_instance.pk, 'lkkkkkkkkkk')
    serialized = sale_serializers.SaleRestSerializer(instances, many=True)

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
                'message': error
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def create_sale(request):
    data = request.data
    print(data)
    try:
        with transaction.atomic():
            Sales = data["Sales"]
            if Sales:
                tran_data = []
                for i in Sales:
                    pk = i['CompanyProductId']

                    try:
                        salesOrderMasterID = i['salesOrderMasterID']
                    except:
                        salesOrderMasterID = None

                    a = i['TransactionId']
                    CompanyProductId = get_instance(
                        pk, web_model.CompanyProduct)
                    auto_id = get_auto_id(web_model.SaleMaster)
                    print(i['Date'], "DATEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
                    # print(CompanyProductId.ProductId.Name,'name')

                    salesdetails = i["SalesDetails"]

                    if salesdetails:
                        try:
                            PlaceofSupply = data['PlaceofSupply']
                        except:
                            PlaceofSupply = ""

                        saleid = web_model.SaleMaster.objects.create(
                            auto_id=auto_id,
                            MasterId=auto_id,
                            creator=request.user,
                            updater=request.user,
                            CompanyProductId=CompanyProductId,
                            salesOrderMasterID=salesOrderMasterID,
                            TransactionTypeId=i['TransactionTypeId'],
                            TransactionId=i['TransactionId'],
                            BranchId=i['BranchId'],
                            LedgerId=i['LedgerId'],
                            PriceCategoryId=i['PriceCategoryId'],
                            SaleAccount=i['SaleAccount'],
                            TaxId=i['TaxId'],
                            TaxType=i['TaxType'],
                            Date=i['Date'],
                            TotalGrossAmt=i['TotalGrossAmt'],
                            AddlDiscPercent=i['AddlDiscPercent'],
                            AddlDiscAmt=i['AddlDiscAmt'],
                            BillDiscPercent=i['BillDiscPercent'],
                            BillDiscAmt=i['BillDiscAmt'],
                            TotalDiscount=i['TotalDiscount'],
                            VATAmount=i['VATAmount'],
                            SGSTAmount=i['SGSTAmount'],
                            CGSTAmount=i['CGSTAmount'],
                            IGSTAmount=i['IGSTAmount'],
                            TAX1Amount=i['TAX1Amount'],
                            TAX2Amount=i['TAX2Amount'],
                            TAX3Amount=i['TAX3Amount'],
                            TotalTax=i['TotalTax'],
                            NetTotal=i['NetTotal'],
                            AdditionalCost=i['AdditionalCost'],
                            GrandTotal=i['GrandTotal'],
                            RoundOff=i['RoundOff'],
                            CashReceived=i['CashReceived'],
                            CashAmount=i['CashAmount'],
                            BankAmount=i['BankAmount'],
                            Balance=i['Balance'],
                            VanId=i['VanId'],
                            Address1=i['Address1'],
                            Address2=i['Address2'],
                            Notes=i['Notes'],
                            CardNumber=i['CardNumber'],
                            CustomerName=i['CustomerName'],
                            PlaceofSupply=PlaceofSupply,
                        )
                        tran_data.append(saleid.TransactionId)

                        for salesdetail in salesdetails:

                            # TransactionId = salesdetail['TransactionId']
                            ProductId = salesdetail['ProductId']
                            Qty = salesdetail['Qty']
                            FreeQty = salesdetail['FreeQty']
                            UnitPrice = salesdetail['UnitPrice']
                            InclusivePrice = salesdetail['InclusivePrice']
                            PriceListID = salesdetail['PriceListID']
                            DiscountPerc = salesdetail['DiscountPerc']
                            DiscountAmount = salesdetail['DiscountAmount']
                            AddlDiscPercent = salesdetail['AddlDiscPercent']
                            AddlDiscAmt = salesdetail['AddlDiscAmt']
                            GrossAmount = salesdetail['GrossAmount']
                            TaxableAmount = salesdetail['TaxableAmount']
                            VATPerc = salesdetail['VATPerc']
                            VATAmount = salesdetail['VATAmount']
                            SGSTPerc = salesdetail['SGSTPerc']
                            SGSTAmount = salesdetail['SGSTAmount']
                            CGSTPerc = salesdetail['CGSTPerc']
                            CGSTAmount = salesdetail['CGSTAmount']
                            IGSTPerc = salesdetail['IGSTPerc']
                            IGSTAmount = salesdetail['IGSTAmount']
                            TAX1Perc = salesdetail['TAX1Perc']
                            TAX1Amount = salesdetail['TAX1Amount']
                            TAX2Perc = salesdetail['TAX2Perc']
                            TAX2Amount = salesdetail['TAX2Amount']
                            TAX3Perc = salesdetail['TAX3Perc']
                            TAX3Amount = salesdetail['TAX3Amount']
                            NetAmount = salesdetail['NetAmount']
                            try:
                                OrderStatus = salesdetail['OrderStatus']
                            except:
                                OrderStatus = False
                            try:
                                CostPerPrice = salesdetail['CostPerPrice']
                            except:
                                CostPerPrice = 0
                            try:
                                StockOrderNo = salesdetail['StockOrderNo']
                            except:
                                StockOrderNo = ""

                            web_model.SaleDetails.objects.create(
                                MasterId=auto_id,
                                SaleId=saleid,
                                # TransactionId=TransactionId,
                                ProductId=ProductId,
                                Qty=Qty,
                                FreeQty=FreeQty,
                                UnitPrice=UnitPrice,
                                InclusivePrice=InclusivePrice,
                                PriceListId=PriceListID,
                                DiscountPerc=DiscountPerc,
                                DiscountAmount=DiscountAmount,
                                AddlDiscPercent=AddlDiscPercent,
                                AddlDiscAmt=AddlDiscAmt,
                                GrossAmount=GrossAmount,
                                TaxableAmount=TaxableAmount,
                                VATPerc=VATPerc,
                                VATAmount=VATAmount,
                                SGSTPerc=SGSTPerc,
                                SGSTAmount=SGSTAmount,
                                CGSTPerc=CGSTPerc,
                                CGSTAmount=CGSTAmount,
                                IGSTPerc=IGSTPerc,
                                IGSTAmount=IGSTAmount,
                                TAX1Perc=TAX1Perc,
                                TAX1Amount=TAX1Amount,
                                TAX2Perc=TAX2Perc,
                                TAX2Amount=TAX2Amount,
                                TAX3Perc=TAX3Perc,
                                TAX3Amount=TAX3Amount,
                                NetAmount=NetAmount,
                                OrderStatus=OrderStatus,
                                CostPerPrice=CostPerPrice,
                                StockOrderNo=StockOrderNo,

                            )
                    # else:
                    #   response_data = {
                    #       "StatusCode" : 6000,
                    #       "message" : "Detail is not exists!!!",
                    #       "data" : tran_data,
                    #       }

                    #   return Response(response_data, status=status.HTTP_200_OK)

                response_data = {
                    "StatusCode": 6000,
                    "message": "Sales created Successfully!!!",
                    "data": tran_data,
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": 'Data does not exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_descrb = str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
        response_data = {
            "StatusCode": 6001,
            "message": "some error occured..please try again"
        }
        user_model.ActivityLog.objects.create(
            CompanyId=data['CompanyID'],
            log_type="create sale",
            message=str(e),
            description=err_descrb,

        )

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def create_single_sale(request):
    data = request.data
    try:
        with transaction.atomic():
            pk = data['CompanyProductId']

            try:
                salesOrderMasterID = data['salesOrderMasterID']
            except:
                salesOrderMasterID = None

            try:
                GUID = data['GUID']
            except:
                GUID = None

            try:
                Treatment = data['Treatment']
            except:
                Treatment = 0
            try:
                TaxableAmount = data['TaxableAmount']
            except:
                TaxableAmount = 0
            try:
                NonTaxableAmount = data['NonTaxableAmount']
            except:
                NonTaxableAmount = 0

            a = data['TransactionId']
            CompanyProductId = get_instance(pk, web_model.CompanyProduct)
            auto_id = get_auto_id(web_model.SaleMaster)
            # print(CompanyProductId.ProductId.Name,'name')
            tran_data = []
            salesdetails = data["SalesDetails"]
            is_ok = True
            today = datetime.datetime.now()
            if web_model.SaleMaster.objects.filter(TransactionId=data['TransactionId'], VanId=data['VanId']):
                instances = web_model.SaleMaster.objects.filter(
                    TransactionId=data['TransactionId'], VanId=data['VanId'])
                for i in instances:
                    print(i.check_date, "EXISST%====================================", str(
                        today.strftime('%Y-%m-%d %H:%M')))
                    if i.check_date == str(today.strftime('%Y-%m-%d %H:%M')) and i.VanId == data['VanId'] and i.TransactionId == data['TransactionId']:
                        is_ok = False

            if salesdetails:
                try:
                    PlaceofSupply = data['PlaceofSupply']
                except:
                    PlaceofSupply = ""
                if is_ok:
                    saleid = web_model.SaleMaster.objects.create(
                        check_date=str(today.strftime('%Y-%m-%d %H:%M')),
                        auto_id=auto_id,
                        MasterId=auto_id,
                        creator=request.user,
                        updater=request.user,
                        CompanyProductId=CompanyProductId,
                        salesOrderMasterID=salesOrderMasterID,
                        TransactionTypeId=data['TransactionTypeId'],
                        TransactionId=data['TransactionId'],
                        BranchId=data['BranchId'],
                        LedgerId=data['LedgerId'],
                        PriceCategoryId=data['PriceCategoryId'],
                        SaleAccount=data['SaleAccount'],
                        TaxId=data['TaxId'],
                        TaxType=data['TaxType'],
                        Date=data['Date'],
                        TotalGrossAmt=data['TotalGrossAmt'],
                        AddlDiscPercent=data['AddlDiscPercent'],
                        AddlDiscAmt=data['AddlDiscAmt'],
                        BillDiscPercent=data['BillDiscPercent'],
                        BillDiscAmt=data['BillDiscAmt'],
                        TotalDiscount=data['TotalDiscount'],
                        VATAmount=data['VATAmount'],
                        SGSTAmount=data['SGSTAmount'],
                        CGSTAmount=data['CGSTAmount'],
                        IGSTAmount=data['IGSTAmount'],
                        TAX1Amount=data['TAX1Amount'],
                        TAX2Amount=data['TAX2Amount'],
                        TAX3Amount=data['TAX3Amount'],
                        TotalTax=data['TotalTax'],
                        NetTotal=data['NetTotal'],
                        AdditionalCost=data['AdditionalCost'],
                        GrandTotal=data['GrandTotal'],
                        RoundOff=data['RoundOff'],
                        CashReceived=data['CashReceived'],
                        CashAmount=data['CashAmount'],
                        BankAmount=data['BankAmount'],
                        Balance=data['Balance'],
                        VanId=data['VanId'],
                        Address1=data['Address1'],
                        Address2=data['Address2'],
                        Notes=data['Notes'],
                        CardNumber=data['CardNumber'],
                        CustomerName=data['CustomerName'],
                        PlaceofSupply=PlaceofSupply,
                        GUID=GUID,

                        Treatment=Treatment,
                        TaxableAmount=TaxableAmount,
                        NonTaxableAmount=NonTaxableAmount,
                    )
                    tran_data.append(saleid.TransactionId)

                    for salesdetail in salesdetails:

                        # TransactionId = salesdetail['TransactionId']
                        ProductId = salesdetail['ProductId']
                        Qty = salesdetail['Qty']
                        FreeQty = salesdetail['FreeQty']
                        UnitPrice = salesdetail['UnitPrice']
                        InclusivePrice = salesdetail['InclusivePrice']
                        PriceListID = salesdetail['PriceListID']
                        DiscountPerc = salesdetail['DiscountPerc']
                        DiscountAmount = salesdetail['DiscountAmount']
                        AddlDiscPercent = salesdetail['AddlDiscPercent']
                        AddlDiscAmt = salesdetail['AddlDiscAmt']
                        GrossAmount = salesdetail['GrossAmount']
                        TaxableAmount = salesdetail['TaxableAmount']
                        VATPerc = salesdetail['VATPerc']
                        VATAmount = salesdetail['VATAmount']
                        SGSTPerc = salesdetail['SGSTPerc']
                        SGSTAmount = salesdetail['SGSTAmount']
                        CGSTPerc = salesdetail['CGSTPerc']
                        CGSTAmount = salesdetail['CGSTAmount']
                        IGSTPerc = salesdetail['IGSTPerc']
                        IGSTAmount = salesdetail['IGSTAmount']
                        TAX1Perc = salesdetail['TAX1Perc']
                        TAX1Amount = salesdetail['TAX1Amount']
                        TAX2Perc = salesdetail['TAX2Perc']
                        TAX2Amount = salesdetail['TAX2Amount']
                        TAX3Perc = salesdetail['TAX3Perc']
                        TAX3Amount = salesdetail['TAX3Amount']
                        NetAmount = salesdetail['NetAmount']
                        try:
                            OrderStatus = salesdetail['OrderStatus']
                        except:
                            OrderStatus = False
                        try:
                            CostPerPrice = salesdetail['CostPerPrice']
                        except:
                            CostPerPrice = 0
                        try:
                            StockOrderNo = salesdetail['StockOrderNo']
                        except:
                            StockOrderNo = ""

                        web_model.SaleDetails.objects.create(
                            MasterId=auto_id,
                            SaleId=saleid,
                            # TransactionId=TransactionId,
                            ProductId=ProductId,
                            Qty=Qty,
                            FreeQty=FreeQty,
                            UnitPrice=UnitPrice,
                            InclusivePrice=InclusivePrice,
                            PriceListId=PriceListID,
                            DiscountPerc=DiscountPerc,
                            DiscountAmount=DiscountAmount,
                            AddlDiscPercent=AddlDiscPercent,
                            AddlDiscAmt=AddlDiscAmt,
                            GrossAmount=GrossAmount,
                            TaxableAmount=TaxableAmount,
                            VATPerc=VATPerc,
                            VATAmount=VATAmount,
                            SGSTPerc=SGSTPerc,
                            SGSTAmount=SGSTAmount,
                            CGSTPerc=CGSTPerc,
                            CGSTAmount=CGSTAmount,
                            IGSTPerc=IGSTPerc,
                            IGSTAmount=IGSTAmount,
                            TAX1Perc=TAX1Perc,
                            TAX1Amount=TAX1Amount,
                            TAX2Perc=TAX2Perc,
                            TAX2Amount=TAX2Amount,
                            TAX3Perc=TAX3Perc,
                            TAX3Amount=TAX3Amount,
                            NetAmount=NetAmount,
                            OrderStatus=OrderStatus,
                            CostPerPrice=CostPerPrice,
                            StockOrderNo=StockOrderNo,

                        )

                    # ins = web_model.SaleMaster.objects.filter(date_added=saleid.date_added,TransactionId=saleid.TransactionId,CompanyProductId=saleid.CompanyProductId,status=False).exclude(pk=saleid.pk)
                    # for i in ins:
                    #     print(i.date_added)
                    # ins.delete()
                response_data = {
                    "StatusCode": 6000,
                    "message": "Sales created Successfully!!!",
                    "data": tran_data,
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": 'Data does not exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_descrb = str(exc_type) + str(fname) + str(exc_tb.tb_lineno)+str(data['TransactionTypeId'])
        response_data = {
            "StatusCode": 6001,
            "message": "some error occured..please try again"
        }
        user_model.ActivityLog.objects.create(
            CompanyId=data['CompanyProductId']+str('CompanyProductId'),
            log_type="create sale",
            message=str(e),
            description=err_descrb,

        )

        return Response(response_data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def create_single_sale_with_count(request):
    data = request.data
    try:
        with transaction.atomic():
            pk = data['CompanyProductId']

            try:
                count = data['count']
            except:
                count = 0

            try:
                salesOrderMasterID = data['salesOrderMasterID']
            except:
                salesOrderMasterID = None

            try:
                GUID = data['GUID']
            except:
                GUID = None

            try:
                Treatment = data['Treatment']
            except:
                Treatment = 0
            try:
                TaxableAmount = data['TaxableAmount']
                if TaxableAmount == '' or TaxableAmount == ' ':
                    TaxableAmount = 0
            except:
                TaxableAmount = 0
            try:
                NonTaxableAmount = data['NonTaxableAmount']
                if NonTaxableAmount == '' or NonTaxableAmount == ' ':
                    NonTaxableAmount = 0
            except:
                NonTaxableAmount = 0

            a = data['TransactionId']
            CompanyProductId = get_instance(pk, web_model.CompanyProduct)
            auto_id = get_auto_id(web_model.SaleMaster)
            # print(CompanyProductId.ProductId.Name,'name')
            tran_data = []
            salesdetails = data["SalesDetails"]
            is_ok = True
            today = datetime.datetime.now()
            if web_model.SaleMaster.objects.filter(TransactionId=data['TransactionId'], VanId=data['VanId']):
                instances = web_model.SaleMaster.objects.filter(
                    TransactionId=data['TransactionId'], VanId=data['VanId'])
                for i in instances:
                    print(i.check_date, "EXISST%====================================", str(
                        today.strftime('%Y-%m-%d %H:%M')))
                    if i.check_date == str(today.strftime('%Y-%m-%d %H:%M')) and i.VanId == data['VanId'] and i.TransactionId == data['TransactionId']:
                        is_ok = False

            if salesdetails:
                try:
                    PlaceofSupply = data['PlaceofSupply']
                except:
                    PlaceofSupply = ""
                if is_ok:
                    saleid = web_model.SaleMaster.objects.create(
                        check_date=str(today.strftime('%Y-%m-%d %H:%M')),
                        auto_id=auto_id,
                        MasterId=auto_id,
                        creator=request.user,
                        updater=request.user,
                        CompanyProductId=CompanyProductId,
                        salesOrderMasterID=salesOrderMasterID,
                        TransactionTypeId=data['TransactionTypeId'],
                        TransactionId=data['TransactionId'],
                        BranchId=data['BranchId'],
                        LedgerId=data['LedgerId'],
                        PriceCategoryId=data['PriceCategoryId'],
                        SaleAccount=data['SaleAccount'],
                        TaxId=data['TaxId'],
                        TaxType=data['TaxType'],
                        Date=data['Date'],
                        TotalGrossAmt=data['TotalGrossAmt'],
                        AddlDiscPercent=data['AddlDiscPercent'],
                        AddlDiscAmt=data['AddlDiscAmt'],
                        BillDiscPercent=data['BillDiscPercent'],
                        BillDiscAmt=data['BillDiscAmt'],
                        TotalDiscount=data['TotalDiscount'],
                        VATAmount=data['VATAmount'],
                        SGSTAmount=data['SGSTAmount'],
                        CGSTAmount=data['CGSTAmount'],
                        IGSTAmount=data['IGSTAmount'],
                        TAX1Amount=data['TAX1Amount'],
                        TAX2Amount=data['TAX2Amount'],
                        TAX3Amount=data['TAX3Amount'],
                        TotalTax=data['TotalTax'],
                        NetTotal=data['NetTotal'],
                        AdditionalCost=data['AdditionalCost'],
                        GrandTotal=data['GrandTotal'],
                        RoundOff=data['RoundOff'],
                        CashReceived=data['CashReceived'],
                        CashAmount=data['CashAmount'],
                        BankAmount=data['BankAmount'],
                        Balance=data['Balance'],
                        VanId=data['VanId'],
                        Address1=data['Address1'],
                        Address2=data['Address2'],
                        Notes=data['Notes'],
                        CardNumber=data['CardNumber'],
                        CustomerName=data['CustomerName'],
                        PlaceofSupply=PlaceofSupply,
                        GUID=GUID,

                        Treatment=Treatment,
                        TaxableAmount=TaxableAmount,
                        NonTaxableAmount=NonTaxableAmount,
                    )
                    tran_data.append(saleid.TransactionId)
                    sale_count = 0
                    for salesdetail in salesdetails:

                        # TransactionId = salesdetail['TransactionId']
                        ProductId = salesdetail['ProductId']
                        Qty = salesdetail['Qty']
                        FreeQty = salesdetail['FreeQty']
                        UnitPrice = salesdetail['UnitPrice']
                        InclusivePrice = salesdetail['InclusivePrice']
                        PriceListID = salesdetail['PriceListID']
                        DiscountPerc = salesdetail['DiscountPerc']
                        DiscountAmount = salesdetail['DiscountAmount']
                        AddlDiscPercent = salesdetail['AddlDiscPercent']
                        AddlDiscAmt = salesdetail['AddlDiscAmt']
                        GrossAmount = salesdetail['GrossAmount']
                        TaxableAmount = salesdetail['TaxableAmount']
                        VATPerc = salesdetail['VATPerc']
                        VATAmount = salesdetail['VATAmount']
                        SGSTPerc = salesdetail['SGSTPerc']
                        SGSTAmount = salesdetail['SGSTAmount']
                        CGSTPerc = salesdetail['CGSTPerc']
                        CGSTAmount = salesdetail['CGSTAmount']
                        IGSTPerc = salesdetail['IGSTPerc']
                        IGSTAmount = salesdetail['IGSTAmount']
                        TAX1Perc = salesdetail['TAX1Perc']
                        TAX1Amount = salesdetail['TAX1Amount']
                        TAX2Perc = salesdetail['TAX2Perc']
                        TAX2Amount = salesdetail['TAX2Amount']
                        TAX3Perc = salesdetail['TAX3Perc']
                        TAX3Amount = salesdetail['TAX3Amount']
                        NetAmount = salesdetail['NetAmount']
                        try:
                            OrderStatus = salesdetail['OrderStatus']
                        except:
                            OrderStatus = False
                        try:
                            CostPerPrice = salesdetail['CostPerPrice']
                        except:
                            CostPerPrice = 0
                        try:
                            StockOrderNo = salesdetail['StockOrderNo']
                        except:
                            StockOrderNo = ""

                        sales_details = web_model.SaleDetails.objects.create(
                            MasterId=auto_id,
                            SaleId=saleid,
                            # TransactionId=TransactionId,
                            ProductId=ProductId,
                            Qty=Qty,
                            FreeQty=FreeQty,
                            UnitPrice=UnitPrice,
                            InclusivePrice=InclusivePrice,
                            PriceListId=PriceListID,
                            DiscountPerc=DiscountPerc,
                            DiscountAmount=DiscountAmount,
                            AddlDiscPercent=AddlDiscPercent,
                            AddlDiscAmt=AddlDiscAmt,
                            GrossAmount=GrossAmount,
                            TaxableAmount=TaxableAmount,
                            VATPerc=VATPerc,
                            VATAmount=VATAmount,
                            SGSTPerc=SGSTPerc,
                            SGSTAmount=SGSTAmount,
                            CGSTPerc=CGSTPerc,
                            CGSTAmount=CGSTAmount,
                            IGSTPerc=IGSTPerc,
                            IGSTAmount=IGSTAmount,
                            TAX1Perc=TAX1Perc,
                            TAX1Amount=TAX1Amount,
                            TAX2Perc=TAX2Perc,
                            TAX2Amount=TAX2Amount,
                            TAX3Perc=TAX3Perc,
                            TAX3Amount=TAX3Amount,
                            NetAmount=NetAmount,
                            OrderStatus=OrderStatus,
                            CostPerPrice=CostPerPrice,
                            StockOrderNo=StockOrderNo,

                        )
                        sale_count += 1
                    if not sale_count == count:
                        error = error1
                        

                    # ins = web_model.SaleMaster.objects.filter(date_added=saleid.date_added,TransactionId=saleid.TransactionId,CompanyProductId=saleid.CompanyProductId,status=False).exclude(pk=saleid.pk)
                    # for i in ins:
                    #     print(i.date_added)
                    # ins.delete()
                response_data = {
                    "StatusCode": 6000,
                    "message": "Sales created Successfully!!!",
                    "data": tran_data,
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": 'Data does not exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_descrb = str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
        response_data = {
            "StatusCode": 6001,
            "message": "some error occured..please try again"
        }
        user_model.ActivityLog.objects.create(
            CompanyId=data['CompanyProductId']+str('CompanyProductId'),
            log_type="create sale",
            message=str(e),
            description=err_descrb,

        )

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_sales(request):
    data = request.data
    Sales = data["Sales"]
    if data:
        for data in Sales:
            instance = None
            CompanyProductId = data['CompanyProductId']
            print(CompanyProductId)
            if web_model.SaleMaster.objects.filter(is_deleted=False, CompanyProductId=CompanyProductId, status=False).exists():
                instance = get_object_or_404(web_model.SaleMaster.objects.filter(
                    is_deleted=False, CompanyProductId=CompanyProductId, status=False))
                print(instance)
                instance.status = True
                instance.save()

        response_data = {
            "StatusCode": 6000,
            "message": "Sale Updated Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Last Sale Price is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def sale_returns(request):
    data = request.data
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    comp_instance = None

    if web_model.CompanyProduct.objects.filter(ProductId__Name=CompanyProductName).exists():
        print("YESSSSSSS")
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)

    instances = web_model.SaleReturnMaster.objects.filter(
        CompanyProductId=comp_instance, status=False)
    print(instances, 'lkkkkkkkkkk')
    serialized = sale_serializers.SaleReturnRestSerializer(
        instances, many=True)

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
                'message': error
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def create_single_sale_return(request):
    data = request.data
    tran_data = []
    try:
        with transaction.atomic():
            pk = data['CompanyProductId']
            CompanyProductId = get_instance(pk, web_model.CompanyProduct)
            auto_id = get_auto_id(web_model.SaleReturnMaster)

            if CompanyProductId:
                try:
                    count = data['count']
                except:
                    count = None
                try:
                    Address1 = data['Address1']
                except:
                    Address1 = None
                try:
                    Address2 = data['Address2']
                except:
                    Address2 = None
                try:
                    Notes = data['Notes']
                except:
                    Notes = None
                try:
                    CustomerName = data['CustomerName']
                except:
                    CustomerName = None
                
                try:
                    GUID = data['GUID']
                except:
                    GUID = None

                try:
                    Treatment = data['Treatment']
                except:
                    Treatment = None
                try:
                    TaxableAmount = data['TaxableAmount']
                except:
                    TaxableAmount = 0
                try:
                    NonTaxableAmount = data['NonTaxableAmount']
                except:
                    NonTaxableAmount = 0


                salemasterid = web_model.SaleReturnMaster.objects.create(
                    auto_id=auto_id,
                    creator=request.user,
                    updater=request.user,
                    CompanyProductId=CompanyProductId,
                    TransactionId=data['TransactionId'],
                    Date=data['Date'],
                    RefferenceBillNo=data['RefferenceBillNo'],
                    RefferenceBillDate=data['RefferenceBillDate'],
                    LedgerId=data['LedgerId'],
                    PriceCategoryId=data['PriceCategoryId'],
                    EmployeeId=data['EmployeeId'],
                    SaleAccount=data['SaleAccount'],
                    TaxId=data['TaxId'],
                    TaxType=data['TaxType'],
                    VATAmount=data['VATAmount'],
                    SGSTAmount=data['SGSTAmount'],
                    CGSTAmount=data['CGSTAmount'],
                    IGSTAmount=data['IGSTAmount'],
                    TAX1Amount=data['TAX1Amount'],
                    TAX2Amount=data['TAX2Amount'],
                    TAX3Amount=data['TAX3Amount'],
                    TotalTax=data['TotalTax'],
                    NetTotal=data['NetTotal'],
                    AdditionalCost=data['AdditionalCost'],
                    TotalGrossAmt=data['TotalGrossAmt'],
                    AddlDiscPercent=data['AddlDiscPercent'],
                    AddlDiscAmt=data['AddlDiscAmt'],
                    TotalDiscount=data['TotalDiscount'],
                    BillDiscPercent=data['BillDiscPercent'],
                    BillDiscAmt=data['BillDiscAmt'],
                    GrandTotal=data['GrandTotal'],
                    RoundOff=data['RoundOff'],
                    VanId=data['VanId'],

                    Address1=data['Address1'],
                    Address2=data['Address2'],
                    Notes=data['Notes'],
                    CustomerName=data['CustomerName'],
                    Treatment=Treatment,
                    TaxableAmount=TaxableAmount,
                    NonTaxableAmount=NonTaxableAmount,
                    GUID=GUID,
                )

                salesdetails = data["SaleReturnDetails"]

                tran_data.append(salemasterid.TransactionId)
                
                return_instance_count = 0
                for salesdetail in salesdetails:

                    ProductId = salesdetail['ProductId']
                    Qty = salesdetail['Qty']
                    FreeQty = salesdetail['FreeQty']
                    UnitPrice = salesdetail['UnitPrice']
                    RateWithTax = salesdetail['RateWithTax']
                    CostPerPrice = salesdetail['CostPerPrice']
                    PriceListId = salesdetail['PriceListId']
                    DiscountAmount = salesdetail['DiscountAmount']
                    DiscountPerc = salesdetail['DiscountPerc']
                    GrossAmount = salesdetail['GrossAmount']
                    AddlDiscPercent = salesdetail['AddlDiscPercent']
                    AddlDiscAmt = salesdetail['AddlDiscAmt']
                    TaxableAmount = salesdetail['TaxableAmount']
                    VATPerc = salesdetail['VATPerc']
                    VATAmount = salesdetail['VATAmount']
                    SGSTPerc = salesdetail['SGSTPerc']
                    SGSTAmount = salesdetail['SGSTAmount']
                    CGSTPerc = salesdetail['CGSTPerc']
                    CGSTAmount = salesdetail['CGSTAmount']
                    IGSTPerc = salesdetail['IGSTPerc']
                    IGSTAmount = salesdetail['IGSTAmount']
                    TAX1Perc = salesdetail['TAX1Perc']
                    TAX1Amount = salesdetail['TAX1Amount']
                    TAX2Perc = salesdetail['TAX2Perc']
                    TAX2Amount = salesdetail['TAX2Amount']
                    TAX3Perc = salesdetail['TAX3Perc']
                    TAX3Amount = salesdetail['TAX3Amount']
                    NetAmount = salesdetail['NetAmount']

                    web_model.SaleReturnDetails.objects.create(
                        SaleReturnMasterId=salemasterid,
                        ProductId=ProductId,
                        Qty=Qty,
                        FreeQty=FreeQty,
                        UnitPrice=UnitPrice,
                        RateWithTax=RateWithTax,
                        CostPerPrice=CostPerPrice,
                        PriceListId=PriceListId,
                        DiscountAmount=DiscountAmount,
                        DiscountPerc=DiscountPerc,
                        GrossAmount=GrossAmount,
                        AddlDiscPercent=AddlDiscPercent,
                        AddlDiscAmt=AddlDiscAmt,
                        TaxableAmount=TaxableAmount,
                        VATPerc=VATPerc,
                        VATAmount=VATAmount,
                        SGSTPerc=SGSTPerc,
                        SGSTAmount=SGSTAmount,
                        CGSTPerc=CGSTPerc,
                        CGSTAmount=CGSTAmount,
                        IGSTPerc=IGSTPerc,
                        IGSTAmount=IGSTAmount,
                        TAX1Perc=TAX1Perc,
                        TAX1Amount=TAX1Amount,
                        TAX2Perc=TAX2Perc,
                        TAX2Amount=TAX2Amount,
                        TAX3Perc=TAX3Perc,
                        TAX3Amount=TAX3Amount,
                        NetAmount=NetAmount,

                    )
                    return_instance_count +=1

                if not return_instance_count == count:
                    error = error1

                try:
                    sales_billwise_details = data["SaleReturnBillWiseDetails"]
                except:
                    sales_billwise_details = None

                if sales_billwise_details:
                    for billwise in sales_billwise_details:

                        Amount = billwise['Amount']
                        VoucherNumber = billwise['VoucherNumber']
                        VoucherType = billwise['VoucherType']
                        Due_Date = billwise['Due_Date']
                        Date = billwise['Date']
                        DueAmount = billwise['DueAmount']
                        Invoice_Amount = billwise['Invoice_Amount']
                        print(
                            salemasterid, "HABEEEEEEEEEEEEEEEEEBBBBBBBBB RAHMAAAAAAANNNNNNN")

                        web_model.SalesReturnBillWiseDetails.objects.create(
                            SaleReturnMasterId=salemasterid,
                            Amount=Amount,
                            VoucherNumber=VoucherNumber,
                            VoucherType=VoucherType,
                            Due_Date=Due_Date,
                            Date=Date,
                            DueAmount=DueAmount,
                            Invoice_Amount=Invoice_Amount,

                        )
                    # else:
                    #   response_data = {
                    #           "StatusCode" : 6001,
                    #            "message" : 'Data does not exists'
                    #           }

                    #   return Response(response_data, status=status.HTTP_200_OK)

                response_data = {
                    "StatusCode": 6000,
                    "data": tran_data,
                    "message": "Sale Returns created Successfully!!!"
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": 'Data does not exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_descrb = str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
        response_data = {
            "StatusCode": 6001,
            "message": "some error occured..please try again"
        }
        user_model.ActivityLog.objects.create(
            CompanyId=data['CompanyProductId']+str('CompanyProductId'),
            log_type="create sale",
            message=str(e),
            description=err_descrb,

        )

        return Response(response_data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_sale_returns(request):
    data = request.data
    Salereturns = data["Salereturns"]
    tran_data = []
    if Salereturns:
        for i in Salereturns:
            salesdetails = i["SaleReturnDetails"]
            if Salereturns:
                pk = i['CompanyProductId']
                CompanyProductId = get_instance(pk, web_model.CompanyProduct)
                auto_id = get_auto_id(web_model.SaleReturnMaster)

                if CompanyProductId:
                    try:
                        Address1 = i['Address1']
                    except:
                        Address1 = None
                    try:
                        Address2 = i['Address2']
                    except:
                        Address2 = None
                    try:
                        Notes = i['Notes']
                    except:
                        Notes = None
                    try:
                        CustomerName = i['CustomerName']
                    except:
                        CustomerName = None
                    
                    try:
                        GUID = i['GUID']
                    except:
                        GUID = None

                    try:
                        Treatment = i['Treatment']
                    except:
                        Treatment = None
                    try:
                        TaxableAmount = i['TaxableAmount']
                    except:
                        TaxableAmount = 0
                    try:
                        NonTaxableAmount = i['NonTaxableAmount']
                    except:
                        NonTaxableAmount = 0


                    salemasterid = web_model.SaleReturnMaster.objects.create(
                        auto_id=auto_id,
                        creator=request.user,
                        updater=request.user,
                        CompanyProductId=CompanyProductId,
                        TransactionId=i['TransactionId'],
                        Date=i['Date'],
                        RefferenceBillNo=i['RefferenceBillNo'],
                        RefferenceBillDate=i['RefferenceBillDate'],
                        LedgerId=i['LedgerId'],
                        PriceCategoryId=i['PriceCategoryId'],
                        EmployeeId=i['EmployeeId'],
                        SaleAccount=i['SaleAccount'],
                        TaxId=i['TaxId'],
                        TaxType=i['TaxType'],
                        VATAmount=i['VATAmount'],
                        SGSTAmount=i['SGSTAmount'],
                        CGSTAmount=i['CGSTAmount'],
                        IGSTAmount=i['IGSTAmount'],
                        TAX1Amount=i['TAX1Amount'],
                        TAX2Amount=i['TAX2Amount'],
                        TAX3Amount=i['TAX3Amount'],
                        TotalTax=i['TotalTax'],
                        NetTotal=i['NetTotal'],
                        AdditionalCost=i['AdditionalCost'],
                        TotalGrossAmt=i['TotalGrossAmt'],
                        AddlDiscPercent=i['AddlDiscPercent'],
                        AddlDiscAmt=i['AddlDiscAmt'],
                        TotalDiscount=i['TotalDiscount'],
                        BillDiscPercent=i['BillDiscPercent'],
                        BillDiscAmt=i['BillDiscAmt'],
                        GrandTotal=i['GrandTotal'],
                        RoundOff=i['RoundOff'],
                        VanId=i['VanId'],

                        Address1=i['Address1'],
                        Address2=i['Address2'],
                        Notes=i['Notes'],
                        CustomerName=i['CustomerName'],
                        Treatment=Treatment,
                        TaxableAmount=TaxableAmount,
                        NonTaxableAmount=NonTaxableAmount,
                        GUID=GUID,
                    )

                    salesdetails = i["SaleReturnDetails"]

                    tran_data.append(salemasterid.TransactionId)

                    for salesdetail in salesdetails:

                        ProductId = salesdetail['ProductId']
                        Qty = salesdetail['Qty']
                        FreeQty = salesdetail['FreeQty']
                        UnitPrice = salesdetail['UnitPrice']
                        RateWithTax = salesdetail['RateWithTax']
                        CostPerPrice = salesdetail['CostPerPrice']
                        PriceListId = salesdetail['PriceListId']
                        DiscountAmount = salesdetail['DiscountAmount']
                        DiscountPerc = salesdetail['DiscountPerc']
                        GrossAmount = salesdetail['GrossAmount']
                        AddlDiscPercent = salesdetail['AddlDiscPercent']
                        AddlDiscAmt = salesdetail['AddlDiscAmt']
                        TaxableAmount = salesdetail['TaxableAmount']
                        VATPerc = salesdetail['VATPerc']
                        VATAmount = salesdetail['VATAmount']
                        SGSTPerc = salesdetail['SGSTPerc']
                        SGSTAmount = salesdetail['SGSTAmount']
                        CGSTPerc = salesdetail['CGSTPerc']
                        CGSTAmount = salesdetail['CGSTAmount']
                        IGSTPerc = salesdetail['IGSTPerc']
                        IGSTAmount = salesdetail['IGSTAmount']
                        TAX1Perc = salesdetail['TAX1Perc']
                        TAX1Amount = salesdetail['TAX1Amount']
                        TAX2Perc = salesdetail['TAX2Perc']
                        TAX2Amount = salesdetail['TAX2Amount']
                        TAX3Perc = salesdetail['TAX3Perc']
                        TAX3Amount = salesdetail['TAX3Amount']
                        NetAmount = salesdetail['NetAmount']

                        web_model.SaleReturnDetails.objects.create(
                            SaleReturnMasterId=salemasterid,
                            ProductId=ProductId,
                            Qty=Qty,
                            FreeQty=FreeQty,
                            UnitPrice=UnitPrice,
                            RateWithTax=RateWithTax,
                            CostPerPrice=CostPerPrice,
                            PriceListId=PriceListId,
                            DiscountAmount=DiscountAmount,
                            DiscountPerc=DiscountPerc,
                            GrossAmount=GrossAmount,
                            AddlDiscPercent=AddlDiscPercent,
                            AddlDiscAmt=AddlDiscAmt,
                            TaxableAmount=TaxableAmount,
                            VATPerc=VATPerc,
                            VATAmount=VATAmount,
                            SGSTPerc=SGSTPerc,
                            SGSTAmount=SGSTAmount,
                            CGSTPerc=CGSTPerc,
                            CGSTAmount=CGSTAmount,
                            IGSTPerc=IGSTPerc,
                            IGSTAmount=IGSTAmount,
                            TAX1Perc=TAX1Perc,
                            TAX1Amount=TAX1Amount,
                            TAX2Perc=TAX2Perc,
                            TAX2Amount=TAX2Amount,
                            TAX3Perc=TAX3Perc,
                            TAX3Amount=TAX3Amount,
                            NetAmount=NetAmount,

                        )

                    try:
                        sales_billwise_details = i["SaleReturnBillWiseDetails"]
                    except:
                        sales_billwise_details = None

                    if sales_billwise_details:
                        for billwise in sales_billwise_details:

                            Amount = billwise['Amount']
                            VoucherNumber = billwise['VoucherNumber']
                            VoucherType = billwise['VoucherType']
                            Due_Date = billwise['Due_Date']
                            Date = billwise['Date']
                            DueAmount = billwise['DueAmount']
                            Invoice_Amount = billwise['Invoice_Amount']
                            print(
                                salemasterid, "HABEEEEEEEEEEEEEEEEEBBBBBBBBB RAHMAAAAAAANNNNNNN")

                            web_model.SalesReturnBillWiseDetails.objects.create(
                                SaleReturnMasterId=salemasterid,
                                Amount=Amount,
                                VoucherNumber=VoucherNumber,
                                VoucherType=VoucherType,
                                Due_Date=Due_Date,
                                Date=Date,
                                DueAmount=DueAmount,
                                Invoice_Amount=Invoice_Amount,

                            )
            # else:
            #   response_data = {
            #           "StatusCode" : 6001,
            #            "message" : 'Data does not exists'
            #           }

            #   return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            "StatusCode": 6000,
            "data": tran_data,
            "message": "Sale Returns created Successfully!!!"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def edit_sale_returns(request):
    data = request.data
    pk = data['id']
    instance = None
    if pk:
        if web_model.SaleReturnMaster.objects.filter(is_deleted=False, status=False, pk=pk).exists():
            instance = get_object_or_404(web_model.SaleReturnMaster.objects.filter(
                is_deleted=False, status=False, pk=pk))
            instance.status = True
            instance.save()

        response_data = {
            "StatusCode": 6000,
            "message": "Sale Return Updated Successfully!"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": "Last Sale Return is not exists!"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def sale_orders(request):
    data = request.data
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    comp_instance = None

    print("Uvaisssssssss.........................ESSSSSSS")
    if web_model.CompanyProduct.objects.filter(ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)

    instances = web_model.SaleOrder.objects.filter(
        status=False, is_deleted=False, CompanyProductId=comp_instance)
    print(instances, 'lkkkkkkkkkk')
    serialized = sale_serializers.SaleOrderRestSerializer(instances, many=True)

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
                'message': error
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_sale_orders(request):
    data = request.data
    print(data)
    Saleorders = data["Saleorders"]
    tran_data = []
    if Saleorders:
        for i in Saleorders:
            pk = i['CompanyProductId']
            CompanyProductId = get_instance(pk, web_model.CompanyProduct)
            auto_id = get_auto_id(web_model.SaleOrder)

            salesdetails = i["SaleorderDetails"]
            if salesdetails:
                saleorderid = web_model.SaleOrder.objects.create(
                    auto_id=auto_id,
                    creator=request.user,
                    updater=request.user,
                    CompanyProductId=CompanyProductId,

                    TransactionId=i['TransactionId'],
                    Date=i['Date'],
                    LedgerId=i['LedgerId'],
                    PriceCategoryId=i['PriceCategoryId'],
                    SaleAccount=i['SaleAccount'],
                    TaxId=i['TaxId'],
                    TaxType=i['TaxType'],
                    VATAmount=i['VATAmount'],
                    SGSTAmount=i['SGSTAmount'],
                    CGSTAmount=i['CGSTAmount'],
                    IGSTAmount=i['IGSTAmount'],
                    TAX1Amount=i['TAX1Amount'],
                    TAX2Amount=i['TAX2Amount'],
                    TAX3Amount=i['TAX3Amount'],
                    TotalTax=i['TotalTax'],
                    NetTotal=i['NetTotal'],
                    BillDiscount=i['BillDiscount'],
                    GrandTotal=i['GrandTotal'],
                    RoundOff=i['RoundOff'],
                    IsInvoiced=i['IsInvoiced'],
                    Address1=i['Address1'],
                    Address2=i['Address2'],
                    Notes=i['Notes'],
                    CustomerName=i['CustomerName'],
                    VanId=i['VanId'],
                )

                tran_data.append(saleorderid.TransactionId)
                salesdetails = i["SaleorderDetails"]

                for salesdetail in salesdetails:

                    try:
                        stockOrderMasterID = salesdetail['stockOrderMasterID']
                    except:
                        stockOrderMasterID = None

                    ProductId = salesdetail['ProductId']
                    Qty = salesdetail['Qty']
                    FreeQty = salesdetail['FreeQty']
                    UnitPrice = salesdetail['UnitPrice']
                    RateWithTax = salesdetail['RateWithTax']
                    CostPerPrice = salesdetail['CostPerPrice']
                    PriceListId = salesdetail['PriceListId']
                    DiscountAmount = salesdetail['DiscountAmount']
                    DiscountPerc = salesdetail['DiscountPerc']
                    GrossAmount = salesdetail['GrossAmount']
                    AddlDiscPercent = salesdetail['AddlDiscPercent']
                    AddlDiscAmt = salesdetail['AddlDiscAmt']
                    TaxableAmount = salesdetail['TaxableAmount']
                    VATPerc = salesdetail['VATPerc']
                    VATAmount = salesdetail['VATAmount']
                    SGSTPerc = salesdetail['SGSTPerc']
                    SGSTAmount = salesdetail['SGSTAmount']
                    CGSTPerc = salesdetail['CGSTPerc']
                    CGSTAmount = salesdetail['CGSTAmount']
                    IGSTPerc = salesdetail['IGSTPerc']
                    IGSTAmount = salesdetail['IGSTAmount']
                    TAX1Perc = salesdetail['TAX1Perc']
                    TAX1Amount = salesdetail['TAX1Amount']
                    TAX2Perc = salesdetail['TAX2Perc']
                    TAX2Amount = salesdetail['TAX2Amount']
                    TAX3Perc = salesdetail['TAX3Perc']
                    TAX3Amount = salesdetail['TAX3Amount']
                    NetAmount = salesdetail['NetAmount']

                    web_model.SaleOrderDetails.objects.create(
                        SaleOrderId=saleorderid,

                        stockOrderMasterID=stockOrderMasterID,
                        ProductId=ProductId,
                        Qty=Qty,
                        FreeQty=FreeQty,
                        UnitPrice=UnitPrice,
                        RateWithTax=RateWithTax,
                        CostPerPrice=CostPerPrice,
                        PriceListId=PriceListId,
                        DiscountAmount=DiscountAmount,
                        DiscountPerc=DiscountPerc,
                        GrossAmount=GrossAmount,
                        AddlDiscPercent=AddlDiscPercent,
                        AddlDiscAmt=AddlDiscAmt,
                        TaxableAmount=TaxableAmount,
                        VATPerc=VATPerc,
                        VATAmount=VATAmount,
                        SGSTPerc=SGSTPerc,
                        SGSTAmount=SGSTAmount,
                        CGSTPerc=CGSTPerc,
                        CGSTAmount=CGSTAmount,
                        IGSTPerc=IGSTPerc,
                        IGSTAmount=IGSTAmount,
                        TAX1Perc=TAX1Perc,
                        TAX1Amount=TAX1Amount,
                        TAX2Perc=TAX2Perc,
                        TAX2Amount=TAX2Amount,
                        TAX3Perc=TAX3Perc,
                        TAX3Amount=TAX3Amount,
                        NetAmount=NetAmount,

                    )

        response_data = {
            "data": tran_data,
            "StatusCode": 6000,
            "message": "Sale Order created Successfully!!!"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def edit_sale_orders(request):
    data = request.data
    MasterID = data['MasterID']
    if web_model.SaleOrder.objects.filter(pk=MasterID).exists():
        print("YESSSSSSS")
        instance = web_model.SaleOrder.objects.get(pk=MasterID)
        instance.status = True
        instance.save()

        return Response(
            {
                'success': 6000,
                "message": "Sale Order updated successfully!!!",
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
                'message': error
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_bill_wise(request):
    data = request.data
    print(data, '@@@@@@@@@########')
    CompanyProductId = data['CompanyProductId']
    VanId = data['VanId']
    if CompanyProductId:
        # for data in saleproducts:
        instances = web_model.BillWise.objects.filter(
            is_deleted=False, CompanyProductId=CompanyProductId, VanId=VanId)
        serialized = sale_serializers.BillWiseSerializer(instances, many=True)
        data = serialized.data
        if data:

            data = {
                "results": data,
                "count": len(instances)
            }
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
def create_bill_wise(request):
    today = datetime.datetime.now()
    data = request.data
    Billwise = data["Billwise"]
    companyproduct_ins = None
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']

    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        companyproduct_ins = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        instances = web_model.BillWise.objects.filter(
            CompanyProductId=companyproduct_ins)
        instances.delete()

    if Billwise and companyproduct_ins:
        count = 0
        instances_arr = []
        auto_id = get_auto_id(web_model.BillWise)
        for data in Billwise:
            TransactionID = data['TransactionID']
            VoucherNo = data['VoucherNo']
            Date = data['Date']
            print(Date[0:9])
            # str(Date).index(sub[, start[, end]] )
            Due_Date = data['Due_Date']
            Invoice_Amount = data['Invoice_Amount']
            CustomerID = data['CustomerID']
            VanId = data['Van_ID']
            Due_Amount = data['Due_Amount']
            Date = Date[0:9]
            print(Date, 'DateDate')

            # SyncDate = data['SyncDate']
            try:
                VoucherType = data['VoucherType']
            except:
                VoucherType = None

            # web_model.BillWise.objects.create(
            #     auto_id=get_auto_id(web_model.BillWise),
            #     creator=request.user,
            #     updater=request.user,
            #     CompanyProductId=companyproduct_ins,
            #     TransactionID=TransactionID,
            #     VoucherType=VoucherType,
            #     VoucherNo=VoucherNo,
            #     Date=Date,
            #     Due_Date=Due_Date,
            #     Invoice_Amount=Invoice_Amount,
            #     CustomerID=CustomerID,
            #     Due_Amount=Due_Amount,
            #     VanId=VanId,

            # )
            instances_arr.append({
                "auto_id":int(auto_id)+count,
                "TransactionID":TransactionID,
                "VoucherType":VoucherType,
                "VoucherNo":VoucherNo,
                "Date":Date,
                "Due_Date":Due_Date,
                "Invoice_Amount":Invoice_Amount,
                "CustomerID":CustomerID,
                "Due_Amount":Due_Amount,
                "VanId":VanId,                                        
            })
            count += 1
        bulkCreate(instances_arr,companyproduct_ins,request,web_model.BillWise)

        response_data = {
            "StatusCode": 6000,
            "message": 'Successfully Created'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_sale_product_price(request):
    print("KAYARYYYYYYYYYYYYYYYYYYYYYY")
    today = datetime.datetime.now()
    data = request.data
    Saleproduct = data["Saleproduct"]
    companyproduct_ins = None
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']

    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        companyproduct_ins = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        instances = web_model.SaleProductPrice.objects.filter(
            CompanyProductId=companyproduct_ins)
        for i in instances:
            i.delete()
        instances1 = web_model.SalePrice.objects.filter(
            CompanyProductId=companyproduct_ins)
        for i in instances1:
            i.delete()
        instances2 = web_model.SaleProduct.objects.filter(
            CompanyProductId=companyproduct_ins)
        for i in instances2:
            i.delete()

    if Saleproduct:
        if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
            for data in Saleproduct:
                # product_ins = web_model.Product.objects.get(Name=CompanyProductName,user=request.user)
                if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
                    companyproduct_ins = web_model.CompanyProduct.objects.get(
                        CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)

                    ProductId = data['ProductID']

                    VatId = data['VAT_ID']
                    GstId = data['GST_ID']
                    Tax1Id = data['Tax1_ID']
                    Tax2Id = data['Tax2_ID']
                    Tax3Id = data['Tax3_ID']
                    Productcode = data['ProductCode']
                    Productname = data['ProductName']

                    # SyncDate = data['SyncDate']
                    try:
                        Displayname = data['DisplayName']
                    except:
                        Displayname = None
                    try:
                        Description = data['Description']
                    except:
                        Description = None
                    try:
                        BranchId = data['BranchID']
                    except:
                        BranchId = 0
                    try:
                        minimumSalesPrice = data['minimumSalesPrice']
                    except:
                        minimumSalesPrice = 0
                    # auto_id = get_auto_id(web_model.SaleProduct)

                    saleproduct_ins = web_model.SaleProduct.objects.create(
                        auto_id=get_auto_id(web_model.SaleProduct),
                        creator=request.user,
                        updater=request.user,
                        CompanyProductId=companyproduct_ins,
                        ProductId=ProductId,
                        BranchId=BranchId,
                        VatId=VatId,
                        GstId=GstId,
                        Tax1Id=Tax1Id,
                        Tax2Id=Tax2Id,
                        Tax3Id=Tax3Id,
                        Productcode=Productcode,
                        Productname=Productname,
                        Displayname=Displayname,
                        Description=Description,
                        minimumSalesPrice=minimumSalesPrice,
                        SyncDate=today,
                    )
                    Saleprice = data['Saleprice']
                    if Saleprice:
                        test = 0
                        for data in Saleprice:
                            test += 1
                            print(test, 'test')
                            # if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName).exists():
                            #   companyproduct_ins = web_model.CompanyProduct.objects.get(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName)

                            try:
                                Barcode = data['Barcode']
                            except:
                                Barcode = None

                            try:
                                IsDefault = data['IsDefault']
                            except:
                                IsDefault = False

                            web_model.SalePrice.objects.create(
                                auto_id=get_auto_id(web_model.SalePrice),
                                creator=request.user,
                                updater=request.user,
                                CompanyProductId=companyproduct_ins,
                                ProductId=data['ProductID'],
                                PriceListId=data['PriceListID'],
                                BranchId=data['BranchID'],
                                UnitName=data['UnitName'],
                                SalePrice=data['SalesPrice'],
                                PurchasePrice=data['PurchasePrice'],
                                SalePrice1=data['SalesPrice1'],
                                SalePrice2=data['SalesPrice2'],
                                SalePrice3=data['SalesPrice3'],
                                MultiFactor=data['MultiFactor'],
                                AutoBarcode=data['AutoBarcode'],
                                IsDefault=IsDefault,
                                Barcode=Barcode,
                                SyncDate=today
                            )
                            web_model.SaleProductPrice.objects.create(
                                auto_id=get_auto_id(web_model.SalePrice),
                                creator=request.user,
                                updater=request.user,
                                CompanyProductId=companyproduct_ins,
                                SaleProductId=saleproduct_ins,
                                ProductId=data['ProductID'],
                                PriceListId=data['PriceListID'],
                                BranchId=data['BranchID'],
                                UnitName=data['UnitName'],
                                SalePrice=data['SalesPrice'],
                                PurchasePrice=data['PurchasePrice'],
                                SalePrice1=data['SalesPrice1'],
                                SalePrice2=data['SalesPrice2'],
                                SalePrice3=data['SalesPrice3'],
                                MultiFactor=data['MultiFactor'],
                                AutoBarcode=data['AutoBarcode'],
                                IsDefault=IsDefault,
                                Barcode=Barcode,
                                SyncDate=today
                            )

                            # else:
                            #   response_data = {
                            #       "StatusCode" : 6001,
                            #       "message" : 'product is not exist!'
                            #   }

                            #   return Response(response_data, status=status.HTTP_200_OK)

            response_data = {
                "StatusCode": 6000,
                "data": data,
                "message": 'Successfully Created'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                "StatusCode": 6001,
                "message": 'company product is not exist!'
            }

            return Response(response_data, status=status.HTTP_200_OK)

    # elif Saleprice:
    #   test = 0
    #   for data in Saleprice:
    #       test +=1
    #       print(test,'test')
    #       if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName).exists():
    #           companyproduct_ins = web_model.CompanyProduct.objects.get(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName)

    #           try:
    #               Barcode = data['Barcode']
    #           except:
    #               Barcode = None

    #           try:
    #               IsDefault = data['IsDefault']
    #           except:
    #               IsDefault = False

    #           web_model.SalePrice.objects.create(
    #               auto_id = get_auto_id(web_model.SalePrice),
    #               creator = request.user,
    #               updater = request.user,
    #               CompanyProductId = companyproduct_ins,
    #               ProductId = data['ProductID'],
    #               PriceListId = data['PriceListID'],
    #               BranchId = data['BranchID'],
    #               UnitName = data['UnitName'],
    #               SalePrice = data['SalesPrice'],
    #               PurchasePrice = data['PurchasePrice'],
    #               SalePrice1 = data['SalesPrice1'],
    #               SalePrice2 = data['SalesPrice2'],
    #               SalePrice3 = data['SalesPrice3'],
    #               MultiFactor = data['MultiFactor'],
    #               AutoBarcode = data['AutoBarcode'],
    #               IsDefault = IsDefault,
    #               Barcode = Barcode,
    #               SyncDate = today
    #           )

    #       else:
    #           response_data = {
    #               "StatusCode" : 6001,
    #               "message" : 'product is not exist!'
    #           }

    #           return Response(response_data, status=status.HTTP_200_OK)

    #   response_data = {
    #       "StatusCode" : 6000,
    #       "message" : 'Successfully Created'
    #   }

    #   return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)
