import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from api.v1.general.functions import generate_serializer_errors, call_paginator_all, list_pagination, get_instance
from api.v1.vansettings import serializers as van_serializers
from api.v1.users.functions import get_auto_id
from api.v1.vansettings.functions import get_van_password

from web import models as web_model
from users import models as user_model
from web.functions import generate_random_password
import datetime


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_van_settings(request):
    data = request.data
    CompanyID = data['CompanyID']
    Device_Code = data['Device_Code']
    CompanyProductName = data['CompanyProductName']
    comp_instance = None
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
    instances = web_model.VanSettings.objects.filter(
        Device_Code=Device_Code, is_deleted=False, CompanyProductId=comp_instance)
    serialized = van_serializers.VanSettingsSerializer(instances, many=True)
    data = serialized.data

    Version = None
    Status = None
    CurrentVersion = None
    MinimumVersion = None

    if web_model.Version.objects.filter().exists():
        instance = web_model.Version.objects.filter().first()
        Version = instance.version
        Status = instance.status
    if user_model.SoftwareVersion.objects.filter().exists():
        instance = user_model.SoftwareVersion.objects.filter().first()
        CurrentVersion = instance.CurrentVersion
        MinimumVersion = instance.MinimumVersion
    if data:
        data = {
            "results": data,
            "count": len(instances)
        }
        return Response(
            {
                'success': 6000,
                'data': data,
                'version': Version,
                'CurrentVersion': CurrentVersion,
                'MinimumVersion': MinimumVersion,
                'data_status':True,
                'status': Status,
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
                'data_status':False,
                'error': error
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_van_settings(request):
    data = request.data
    Vansettings = data["Vansettings"]
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        instances = web_model.VanSettings.objects.filter(
            CompanyProductId=comp_instance)
        for i in instances:
            i.delete()

    if Vansettings:
        for data in Vansettings:
            auto_id = get_auto_id(web_model.VanSettings)
            if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
                instance = web_model.CompanyProduct.objects.get(
                    CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
                try:
                    EmployeeID = data['EmployeeID']
                    if not EmployeeID:
                        EmployeeID = 0
                except:
                    EmployeeID = 0
                try:
                    CashBalance = data['CashBalance']
                except:
                    CashBalance = 0
                try:
                    VanSaleRoundoff = data['VanSaleRoundoff']
                except:
                    VanSaleRoundoff = 0
                try:
                    PriceCategoryID = data['PriceCategoryID']
                except:
                    PriceCategoryID = 0

                try:
                    VoucherPrefix = data['VoucherPrefix']
                except:
                    VoucherPrefix = None

                try:
                    Sales_Invoice_Edit = data['Sales_Invoice_Edit']
                except:
                    Sales_Invoice_Edit = False

                try:
                    Sales_price_lessthan_Purchase_price = data['Sales_price_lessthan_Purchase_price']
                except:
                    Sales_price_lessthan_Purchase_price = None

                try:
                    PriceDecimalPoint = data['PriceDecimalPoint']
                except:
                    PriceDecimalPoint = None

                try:
                    QtyDecimalPoint = data['PriceDecimalPoint']
                except:
                    QtyDecimalPoint = None

                    # 'EditPaymentinsalesbeforeSync', 'EditExpensebeforeSync', 'EditReceiptbeforeSync',
                try:
                    EditPaymentinsalesbeforeSync = data['EditPaymentinsalesbeforeSync']
                except:
                    EditPaymentinsalesbeforeSync = False

                try:
                    EditExpensebeforeSync = data['EditExpensebeforeSync']
                except:
                    EditExpensebeforeSync = False

                try:
                    EditReceiptbeforeSync = data['EditReceiptbeforeSync']
                except:
                    EditReceiptbeforeSync = False

                # =====
                try:
                    EditsalesReturnbeforeSync = data['EditsalesReturnbeforeSync']
                except:
                    EditsalesReturnbeforeSync = False

                try:
                    EditsalesOrderbeforeSync = data['EditsalesOrderbeforeSync']
                except:
                    EditsalesOrderbeforeSync = False

                # =====
                try:
                    CountryId = data['CountryId']
                except:
                    CountryId = 0

                try:
                    PlaceofSupply = data['PlaceofSupply']
                except:
                    PlaceofSupply = ""

                try:
                    EnablePortForward = data['EnablePortForward']
                except:
                    EnablePortForward = False

                try:
                    IPAddress = data['IPAddress']
                except:
                    IPAddress = ""

                try:
                    Port = data['Port']
                except:
                    Port = ""

                try:
                    DatabaseName = data['DatabaseName']
                except:
                    DatabaseName = ""

                try:
                    DBUserName = data['DBUserName']
                except:
                    DBUserName = ""

                try:
                    DBPassword = data['DBPassword']
                except:
                    DBPassword = ""


                try:
                    ServerName = data['ServerName']
                except:
                    ServerName = ""

                try:
                    BranchID = data['BranchID']
                except:
                    BranchID = None

                try:
                    Enable_ZATCA_Rules = data['Enable_ZATCA_Rules']
                except:
                    Enable_ZATCA_Rules = False

                web_model.VanSettings.objects.create(
                    auto_id=auto_id,
                    creator=request.user,
                    updater=request.user,
                    user=request.user,
                    CompanyProductId=instance,
                    UserName=data['UserName'],
                    PriceCategoryID=PriceCategoryID,
                    VanSaleRoundoff=VanSaleRoundoff,
                    CashBalance=CashBalance,
                    EmployeeID=EmployeeID,

                    VoucherPrefix=VoucherPrefix,
                    VatSalesType=data['Sales_Tax_Type'],
                    # GSTSalesType = data['GSTSalesType'],
                    VanId=data['Van_ID'],
                    WarehouseId=data['WarehouseID'],
                    VanName=data['Van_Name'],
                    Device_Code=data['Device_Code'],
                    Password=data['Password'],
                    # CreditLimit = data['Credit_Limit'],
                    DiscountPercentPerBill=data['Discount_Percent_Per_Bill'],


                    ShowNegativeStockItem=data['Show_Negative_Stock_Item'],
                    CanEditUnitPrice=data['Can_Edit_Unit_Price'],
                    AllowBillDiscount=data['Allow_Bill_Discount'],
                    Allow_Sales_Below_Min_Sales_Price=data['Allow_Sales_Below_Min_Sales_Price'],
                    AllowNegativeStockSale=data['Allow_Negative_Stock_Sale'],
                    Allow_Sales_Below_Purchase_Price=data['Allow_Sales_Below_Purchase_Price'],
                    AllowItemwiseDiscount=data['Allow_Item_wise_Discount'],
                    Show_Last_Sales_Price=data['Show_Last_Sales_Price'],
                    ShowSalesType=data['Show_Sales_Type'],

                    UserID=data['UserID'],
                    CashAccountID=data['CashAccountID'],
                    BankAccountID=data['BankAccountID'],
                    sales_account=data['sales_account'],
                    Allow_Receipt_Discount=data['Allow_Receipt_Discount'],
                    sales_return_account=data['sales_return_account'],
                    Allow_Cash_Sales=data['Allow_Cash_Sales'],
                    Show_Inclusive_Field=data['Show_Inclusive_Field'],

                    Show_Cost_In_Stock_Order=data['Show_Cost_In_Stock_Order'],
                    StockOrderWarehouseFromId=data['StockOrderWarehouseFromId'],

                    Sales_Invoice_Edit=data['Sales_Invoice_Edit'],
                    Sales_price_lessthan_Purchase_price=data['Sales_price_lessthan_Purchase_price'],
                    PriceDecimalPoint=data['PriceDecimalPoint'],
                    QtyDecimalPoint=data['QtyDecimalPoint'],

                    EditPaymentinsalesbeforeSync=EditPaymentinsalesbeforeSync,
                    EditExpensebeforeSync=EditExpensebeforeSync,
                    EditReceiptbeforeSync=EditReceiptbeforeSync,

                    EditsalesReturnbeforeSync=EditsalesReturnbeforeSync,
                    EditsalesOrderbeforeSync=EditsalesOrderbeforeSync,

                    CountryId=CountryId,
                    PlaceofSupply=PlaceofSupply,

                    EnablePortForward=EnablePortForward,
                    IPAddress=IPAddress,
                    Port=Port,
                    DatabaseName=DatabaseName,
                    DBUserName=DBUserName,
                    DBPassword=DBPassword,
                    ServerName=ServerName,
                    BranchID=BranchID,
                    Enable_ZATCA_Rules=Enable_ZATCA_Rules,
                )
            else:

                response_data = {
                    "StatusCode": 6001,
                    "message": 'product is not exist!'
                }

                return Response(response_data, status=status.HTTP_200_OK)

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
def create_van_password(request):
    data = request.data
    VanId = data["VanId"]
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    today = datetime.date.today()
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        if web_model.VanSettings.objects.filter(CompanyProductId=comp_instance, VanId=VanId).exists():

            van_instance = web_model.VanSettings.objects.get(
                CompanyProductId=comp_instance, VanId=VanId)

            # generate_random_password
            now_time = time.time()
            time_str = str(now_time)
            print(now_time, time_str, "OOOOOOOOOOOOppp")
            if web_model.VanPassword.objects.filter(vansettings=van_instance):
                password = get_van_password(van_instance)
                web_model.VanPassword.objects.filter(
                    vansettings=van_instance).update(password=password, date_added=today, date_updated=today,
                                                     time_str=time_str, is_expired=False)

            else:
                password = get_van_password(van_instance)
                web_model.VanPassword.objects.create(
                    vansettings=van_instance,
                    password=password,
                    auto_id=get_auto_id(web_model.VanPassword),
                    creator=request.user,
                    updater=request.user,
                    # time=time_str,
                    time_str=time_str
                )

            response_data = {
                "StatusCode": 6000,
                "password": password,
                "message": 'Successfully generated'
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "message": 'VanSettings is not exists!'
            }
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            "message": 'Company is not registered!'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_van_password_expire(request):
    data = request.data
    VanId = data["VanId"]
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    today = datetime.date.today()
    if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName).exists():
        comp_instance = web_model.CompanyProduct.objects.get(
            CompanyId__pk=CompanyID, ProductId__Name=CompanyProductName)
        if web_model.VanSettings.objects.filter(CompanyProductId=comp_instance, VanId=VanId).exists():
            van_instance = web_model.VanSettings.objects.get(
                CompanyProductId=comp_instance, VanId=VanId)

            # generate_random_password
            now_time = time.time()
            time_str = str(now_time)
            print(now_time, time_str, "OOOOOOOOOOOOppp")
            if web_model.VanPassword.objects.filter(vansettings=van_instance):
                is_expired = web_model.VanPassword.objects.get(
                    vansettings=van_instance).is_expired
                response_data = {
                    "StatusCode": 6000,
                    "is_expired": is_expired,
                }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": 'in this van password is not generated'
                }

        else:
            response_data = {
                "StatusCode": 6001,
                "message": 'VanSettings is not exists!'
            }
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            "message": 'Company is not registered!'
        }

        return Response(response_data, status=status.HTTP_200_OK)
