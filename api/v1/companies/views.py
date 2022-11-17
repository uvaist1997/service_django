from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from api.v1.general.functions import generate_serializer_errors, call_paginator_all, list_pagination, get_instance
from api.v1.companies import serializers as company_serializers
from main.functions import get_auto_id
from web import models as web_model
from datetime import datetime, timedelta
from users import models as user_model
from django.shortcuts import render, get_object_or_404


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_companies(request):
    print(request.user)
    instances = web_model.Companies.objects.filter(
        is_deleted=False, user=request.user)
    serialized = company_serializers.CompaniesSerializer(instances, many=True)
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
        error = "no data"
        return Response(
            {
                'success': success,
                'data': None,
                'error': error
            },
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_company(request):

    data = request.data
    if data:
        CompanyName = data['CompanyName']
        pk = data['BusinessType']
        BusinessType = get_instance(pk, user_model.BusinessType)
        Country = data['Country']
        print(BusinessType, 'BusinessType')
        State = data['State']
        OfficePhoneNumber = data['OfficePhoneNumber']
        Email = data['Email']
        auto_id = get_auto_id(web_model.Companies)
        print(request.user.username, "ADMIN")
        user = User.objects.get(username=request.user.username)

        company = web_model.Companies.objects.create(
            auto_id=auto_id,
            creator=user,
            updater=user,
            user=request.user,
            business_type=BusinessType,
            CompanyName=CompanyName,
            Country=Country,
            State=State,
            OfficePhoneNumber=OfficePhoneNumber,
            Email=Email,
            Action="A",
        )

        web_model.CompaniesLog.objects.create(
            Companyid=auto_id,
            auto_id=get_auto_id(web_model.CompaniesLog),
            creator=request.user,
            updater=request.user,
            business_type=BusinessType,
            CompanyName=CompanyName,
            user=request.user,
            Country=Country,
            State=State,
            OfficePhoneNumber=OfficePhoneNumber,
            Email=Email,
            Action="A",
        )
        data = {
            'CompanyId': company.pk,
            "CompanyName": company.CompanyName,
            "Country": company.Country,
            "State": company.State,
            "Email": company.Email,
            "OfficePhoneNumber": company.OfficePhoneNumber,
            "BusinessType": company.business_type.pk,
        }
        response_data = {
            "StatusCode": 6000,
            "data": data,
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
def edit_company(request, pk):
    data = request.data
    if data:
        serialized = company_serializers.CompaniesSerializer(data=request.data)
        instance = None
        if web_model.Companies.objects.filter(pk=pk, is_deleted=False).exists():
            instance = web_model.Companies.objects.get(pk=pk, is_deleted=False)
        if instance:
            if serialized.is_valid():
                OfficePhoneNumber = data['OfficePhoneNumber']
                CompanyName = data['CompanyName']
                Country = data['Country']
                State = data['State']
                Email = data['Email']
                instance.OfficePhoneNumber = OfficePhoneNumber
                instance.CompanyName = CompanyName
                instance.Country = Country
                instance.State = State
                instance.Email = Email
                instance.save()
                serialized.update(instance, serialized.data)

                print(Country, request.data)
                auto_id = get_auto_id(web_model.Companies)
                print(OfficePhoneNumber, "$$$$$$$$$$$$$$")
                user = User.objects.get(username=request.user.username)

                web_model.CompaniesLog.objects.create(
                    Companyid=auto_id,
                    auto_id=get_auto_id(web_model.CompaniesLog),
                    creator=request.user,
                    updater=request.user,
                    user=request.user,
                    CompanyName=CompanyName,
                    Country=Country,
                    State=State,
                    OfficePhoneNumber=OfficePhoneNumber,
                    Email=Email,
                    Action="M",
                )

                response_data = {
                    "StatusCode": 6000,
                    "data": data,
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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_company_product(request):
    today = datetime.now()
    data = request.data
    comp_array = []
    if data:
        exp_date = today+timedelta(days=7)
        ProductId = None
        pk = data['id']
        company_list = web_model.Companies.objects.filter(user=request.user)
        DeviceCode = data['DeviceCode']
        Productname = data['Productname']
        try:
            software_plan = data['software_plan']
            software_plan = user_model.SoftwarePlan.objects.get(
                Name=software_plan, product__Name=Productname)
        except:
            software_plan = ""

        # print("Munb===============","############",company_list)
        devices_company_name = 'Company'
        for i in company_list:
            comp_array.append(i.pk)
            ProductId = user_model.Product.objects.get(Name=Productname)
            if web_model.CompanyProduct.objects.filter(CompanyId__id=i.pk, ProductId=ProductId).exists():
                c = web_model.CompanyProduct.objects.get(
                    CompanyId__id=i.pk, ProductId=ProductId)
                if web_model.CompanyDevices.objects.filter(CompanyProductId=c.pk, DeviceCode=DeviceCode).exists():
                    devices_company_name = c.CompanyId.CompanyName

        com_prod_list = web_model.CompanyProduct.objects.filter(
            CompanyId__in=comp_array).values_list('id')
        CompanyId = get_instance(pk, web_model.Companies)
        divice_list = web_model.CompanyDevices.objects.filter(
            DeviceCode=DeviceCode, CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId=CompanyId)

        DeviceName = data['DeviceName']
        Type = data['Type']
        if user_model.Product.objects.filter(Name=Productname).exists():
            ProductId = user_model.Product.objects.get(Name=Productname)

            if web_model.CompanyProduct.objects.filter(CompanyId=CompanyId, ProductId=ProductId).exists():
                CompanyProductId = get_object_or_404(web_model.CompanyProduct.objects.filter(
                    CompanyId=CompanyId, ProductId=ProductId))
                try:
                    new_AMCActive = CompanyProductId.AMCActive.date()
                except:
                    new_AMCActive = None
                try:
                    new_AMCExpiry = CompanyProductId.AMCExpiry.date()
                except:
                    new_AMCExpiry = None
                try:
                    new_service_date = CompanyProductId.service_date.date()
                except:
                    new_service_date = None

                if web_model.CompanyDevices.objects.filter(CompanyProductId=CompanyProductId).exists():
                    company_devices = web_model.CompanyDevices.objects.filter(
                        CompanyProductId=CompanyProductId).count()
                else:
                    company_devices = 0
                if not CompanyProductId.IsTrialVersion:

                    # if CompanyProductId.No_ofDevice > company_devices:
                    if not web_model.CompanyDevices.objects.filter(is_deleted=False, CompanyProductId=CompanyProductId, DeviceCode=DeviceCode).exists():
                        if not web_model.CompanyDevices.objects.filter(is_deleted=False, Type="server", CompanyProductId__CompanyId=CompanyId, CompanyProductId__ProductId=ProductId).exists() or Type == "Client":
                            if not divice_list:
                                company_device = web_model.CompanyDevices.objects.create(
                                    auto_id=get_auto_id(
                                        web_model.CompanyDevices),
                                    creator=request.user,
                                    updater=request.user,
                                    CompanyProductId=CompanyProductId,
                                    DeviceName=DeviceName,
                                    DeviceCode=DeviceCode,
                                    Type=Type,

                                    Action="A",
                                    IsTrialVersion=CompanyProductId.IsTrialVersion,
                                    ProductExpiryDate=exp_date,

                                )
                                device_number_False = len(web_model.CompanyDevices.objects.filter(
                                    IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                                device_number_True = len(web_model.CompanyDevices.objects.filter(
                                    IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                                try:
                                    new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                                except:
                                    new_ProductExpiryDate = ""
                                data = {
                                    "device_number_True": device_number_True,
                                    "device_number_False": device_number_False,
                                    "username": request.user.username,
                                    "software_plan": CompanyProductId.software_plan.Name,
                                    "Trial": company_device.IsTrialVersion,
                                    "CompanyId": pk,
                                    "CompanyName": CompanyProductId.CompanyId.CompanyName,
                                    "ProductName": Productname,
                                    "BusinessType": CompanyProductId.CompanyId.business_type.Name,
                                    "Type": Type,
                                    "DeviceName": DeviceName,
                                    "DeviceCode": DeviceCode,
                                    "CompanyProductId": CompanyProductId.pk,
                                    "ProductExpiryDate": company_device.ProductExpiryDate,
                                    "ProductId": CompanyProductId.ProductId.pk,
                                    "AMCActive": CompanyProductId.AMCActive,
                                    "AMCExpiry": CompanyProductId.AMCExpiry,
                                    "service_date": CompanyProductId.service_date,
                                    "service": CompanyProductId.service,
                                    "new_ProductExpiryDate": new_ProductExpiryDate,
                                    "new_AMCActive": new_AMCActive,
                                    "new_AMCExpiry": new_AMCExpiry,
                                    "new_service_date": new_service_date,
                                }

                                response_data = {
                                    "StatusCode": 6000,
                                    "data": data,
                                    "message": 'Successfully Registerd'
                                }

                                return Response(response_data, status=status.HTTP_200_OK)
                            else:
                                data = []
                                for d in divice_list:
                                    company_device = d
                                    device_number_True = len(web_model.CompanyDevices.objects.filter(
                                        IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                                    device_number_False = len(web_model.CompanyDevices.objects.filter(
                                        IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                                    try:
                                        new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                                    except:
                                        new_ProductExpiryDate = ""
                                    dic = {
                                        "device_number_True": device_number_True,
                                        "device_number_False": device_number_False,
                                        "username": request.user.username,
                                        "software_plan": company_device.CompanyProductId.software_plan.Name,
                                        "Trial": company_device.IsTrialVersion,
                                        "CompanyId": company_device.CompanyProductId.CompanyId.pk,
                                        "CompanyName": company_device.CompanyProductId.CompanyId.CompanyName,
                                        "ProductName": company_device.CompanyProductId.ProductId.Name,
                                        "BusinessType": company_device.CompanyProductId.CompanyId.business_type.Name,
                                        "Type": company_device.Type,
                                        "DeviceName": company_device.DeviceName,
                                        "DeviceCode": company_device.DeviceCode,
                                        "CompanyProductId": company_device.CompanyProductId.pk,
                                        "ProductExpiryDate": company_device.ProductExpiryDate,
                                        "ProductId": company_device.CompanyProductId.ProductId.pk,
                                        "AMCActive": company_device.CompanyProductId.AMCActive,
                                        "AMCExpiry": company_device.CompanyProductId.AMCExpiry,
                                        "service_date": company_device.CompanyProductId.service_date,
                                        "service": company_device.CompanyProductId.service,
                                        "new_ProductExpiryDate": new_ProductExpiryDate,
                                        "new_AMCActive": new_AMCActive,
                                        "new_AMCExpiry": new_AMCExpiry,
                                        "new_service_date": new_service_date,
                                    }
                                    data.append(dic)

                                response_data = {
                                    "StatusCode": 6001,
                                    # "message" : generate_serializer_errors(serialized._errors)
                                    "data": data,
                                    "message": str('Device already Registered in')+str(" ")+str(devices_company_name)
                                }

                            return Response(response_data, status=status.HTTP_200_OK)

                        else:
                            response_data = {
                                "StatusCode": 6001,
                                "message": 'Server already exist'
                            }

                        return Response(response_data, status=status.HTTP_200_OK)

                    else:
                        company_device = web_model.CompanyDevices.objects.filter(
                            is_deleted=False, CompanyProductId=CompanyProductId, DeviceCode=DeviceCode).first()
                        device_number_True = len(web_model.CompanyDevices.objects.filter(
                            IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                        device_number_False = len(web_model.CompanyDevices.objects.filter(
                            IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                        try:
                            new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                        except:
                            new_ProductExpiryDate = ""
                        data = {
                            "device_number_True": device_number_True,
                            "device_number_False": device_number_False,
                            "username": request.user.username,
                            "software_plan": company_device.CompanyProductId.software_plan.Name,
                            "Trial": company_device.IsTrialVersion,
                            "CompanyId": company_device.CompanyProductId.CompanyId.pk,
                            "CompanyName": company_device.CompanyProductId.CompanyId.CompanyName,
                            "ProductName": company_device.CompanyProductId.ProductId.Name,
                            "BusinessType": company_device.CompanyProductId.CompanyId.business_type.Name,
                            "Type": company_device.Type,
                            "DeviceName": company_device.DeviceName,
                            "DeviceCode": company_device.DeviceCode,
                            "CompanyProductId": company_device.CompanyProductId.pk,
                            "ProductExpiryDate": company_device.ProductExpiryDate,
                            "ProductId": company_device.CompanyProductId.ProductId.pk,
                            "AMCActive": company_device.CompanyProductId.AMCActive,
                            "AMCExpiry": company_device.CompanyProductId.AMCExpiry,
                            "service_date": company_device.CompanyProductId.service_date,
                            "service": company_device.CompanyProductId.service,
                            "new_ProductExpiryDate": new_ProductExpiryDate,
                            "new_AMCActive": new_AMCActive,
                            "new_AMCExpiry": new_AMCExpiry,
                            "new_service_date": new_service_date,
                        }
                        response_data = {
                            "StatusCode": 6001,
                            "message": 'This device already exist',
                            "data": data
                        }

                    return Response(response_data, status=status.HTTP_200_OK)

                    # else:
                    # 	response_data = {
                    # 		"StatusCode" : 6001,
                    # 		"message" : 'Permission denied for this device'
                    # 	}

                    # return Response(response_data, status=status.HTTP_200_OK)
                else:
                    if not web_model.CompanyDevices.objects.filter(is_deleted=False, CompanyProductId=CompanyProductId, DeviceCode=DeviceCode).exists():
                        if not divice_list:
                            if Type == "server":
                                if web_model.CompanyDevices.objects.filter(is_deleted=False, Type=Type, CompanyProductId__CompanyId=CompanyId, CompanyProductId__ProductId=ProductId).exists():
                                    is_server = True
                                    d = web_model.CompanyDevices.objects.filter(
                                        is_deleted=False, Type=Type, CompanyProductId__CompanyId=CompanyId, CompanyProductId__ProductId=ProductId)
                                    print(d, "UVAIS====")
                                    response_data = {
                                        "StatusCode": 6001,
                                        "message": 'Server already exist'
                                    }

                                    return Response(response_data, status=status.HTTP_200_OK)
                                else:
                                    is_server = False
                                    CompanyProductId.No_ofDevice = CompanyProductId.No_ofDevice + 1
                                    CompanyProductId.save()
                                    company_device = web_model.CompanyDevices.objects.create(
                                        auto_id=get_auto_id(
                                            web_model.CompanyDevices),
                                        creator=request.user,
                                        updater=request.user,
                                        CompanyProductId=CompanyProductId,
                                        DeviceName=DeviceName,
                                        DeviceCode=DeviceCode,
                                        Type=Type,

                                        Action="A",

                                        IsTrialVersion=CompanyProductId.IsTrialVersion,
                                        ProductExpiryDate=exp_date,

                                    )
                                    device_number_True = len(web_model.CompanyDevices.objects.filter(
                                        IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                                    device_number_False = len(web_model.CompanyDevices.objects.filter(
                                        IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                                    try:
                                        new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                                    except:
                                        new_ProductExpiryDate = ""
                                    data = {
                                        "device_number_True": device_number_True,
                                        "device_number_False": device_number_False,
                                        "username": request.user.username,
                                        "software_plan": CompanyProductId.software_plan.Name,
                                        "Trial": CompanyProductId.IsTrialVersion,
                                        "CompanyId": pk,
                                        "CompanyName": CompanyProductId.CompanyId.CompanyName,
                                        "ProductName": CompanyProductId.ProductId.Name,
                                        "BusinessType": CompanyProductId.CompanyId.business_type.Name,
                                        "Type": Type,
                                        "DeviceName": DeviceName,
                                        "DeviceCode": DeviceCode,
                                        "CompanyProductId": CompanyProductId.pk,
                                        "ProductExpiryDate": company_device.ProductExpiryDate,
                                        "ProductId": CompanyProductId.ProductId.pk,
                                        "AMCActive": CompanyProductId.AMCActive,
                                        "AMCExpiry": CompanyProductId.AMCExpiry,
                                        "service_date": CompanyProductId.service_date,
                                        "service": CompanyProductId.service,
                                        "new_ProductExpiryDate": new_ProductExpiryDate,
                                        "new_AMCActive": new_AMCActive,
                                        "new_AMCExpiry": new_AMCExpiry,
                                        "new_service_date": new_service_date,
                                    }
                                    response_data = {
                                        "StatusCode": 6000,
                                        "data": data,
                                        "message": 'Successfully Registerd'
                                    }

                                    return Response(response_data, status=status.HTTP_200_OK)

                            else:
                                is_server = False
                                CompanyProductId.No_ofDevice = CompanyProductId.No_ofDevice + 1
                                print('CLIENT')
                                CompanyProductId.save()
                                print("SAVAD#########@@@@@@@#######")
                                company_device = web_model.CompanyDevices.objects.create(
                                    auto_id=get_auto_id(
                                        web_model.CompanyDevices),
                                    creator=request.user,
                                    updater=request.user,
                                    CompanyProductId=CompanyProductId,
                                    DeviceName=DeviceName,
                                    DeviceCode=DeviceCode,
                                    Type=Type,

                                    Action="A",

                                    IsTrialVersion=CompanyProductId.IsTrialVersion,
                                    ProductExpiryDate=exp_date,


                                )
                                device_number_True = len(web_model.CompanyDevices.objects.filter(
                                    IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                                device_number_False = len(web_model.CompanyDevices.objects.filter(
                                    IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                                try:
                                    new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                                except:
                                    new_ProductExpiryDate = ""
                                data = {
                                    "device_number_True": device_number_True,
                                    "device_number_False": device_number_False,
                                    "username": request.user.username,
                                    "software_plan": CompanyProductId.software_plan.Name,
                                    "Trial": CompanyProductId.IsTrialVersion,
                                    "CompanyId": pk,
                                    "CompanyName": CompanyProductId.CompanyId.CompanyName,
                                    "ProductName": CompanyProductId.ProductId.Name,
                                    "BusinessType": CompanyProductId.CompanyId.business_type.Name,
                                    "Type": Type,
                                    "DeviceName": DeviceName,
                                    "DeviceCode": DeviceCode,
                                    "CompanyProductId": CompanyProductId.pk,
                                    "ProductId": CompanyProductId.ProductId.pk,
                                    "service": CompanyProductId.service,
                                    "ProductExpiryDate": company_device.ProductExpiryDate,
                                    "AMCActive": CompanyProductId.AMCActive,
                                    "AMCExpiry": CompanyProductId.AMCExpiry,
                                    "service_date": CompanyProductId.service_date,
                                    "new_ProductExpiryDate": new_ProductExpiryDate,
                                    "new_AMCActive": new_AMCActive,
                                    "new_AMCExpiry": new_AMCExpiry,
                                    "new_service_date": new_service_date,
                                }
                                response_data = {
                                    "StatusCode": 6000,
                                    "data": data,
                                    "message": 'Successfully Registerd'
                                }

                                return Response(response_data, status=status.HTTP_200_OK)
                        else:
                            data = []
                            for d in divice_list:
                                company_device = d
                                device_number_True = len(web_model.CompanyDevices.objects.filter(
                                    IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                                device_number_False = len(web_model.CompanyDevices.objects.filter(
                                    IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                                try:
                                    new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                                except:
                                    new_ProductExpiryDate = ""
                                dic = {
                                    "device_number_True": device_number_True,
                                    "device_number_False": device_number_False,
                                    "username": request.user.username,
                                    "software_plan": company_device.CompanyProductId.software_plan.Name,
                                    "Trial": company_device.IsTrialVersion,
                                    "CompanyId": company_device.CompanyProductId.CompanyId.pk,
                                    "CompanyName": company_device.CompanyProductId.CompanyId.CompanyName,
                                    "ProductName": company_device.CompanyProductId.ProductId.Name,
                                    "BusinessType": company_device.CompanyProductId.CompanyId.business_type.Name,
                                    "Type": company_device.Type,
                                    "DeviceName": company_device.DeviceName,
                                    "DeviceCode": company_device.DeviceCode,
                                    "CompanyProductId": company_device.CompanyProductId.pk,
                                    "ProductExpiryDate": company_device.ProductExpiryDate,
                                    "ProductId": company_device.CompanyProductId.ProductId.pk,
                                    "AMCActive": company_device.CompanyProductId.AMCActive,
                                    "AMCExpiry": company_device.CompanyProductId.AMCExpiry,
                                    "service_date": company_device.CompanyProductId.service_date,
                                    "service": company_device.CompanyProductId.service,
                                    "new_ProductExpiryDate": new_ProductExpiryDate,
                                    "new_AMCActive": new_AMCActive,
                                    "new_AMCExpiry": new_AMCExpiry,
                                    "new_service_date": new_service_date,
                                }
                                data.append(dic)

                            response_data = {
                                "data": data,
                                "StatusCode": 6001,
                                # "message" : generate_serializer_errors(serialized._errors)
                                "message": str('Device already Registered in')+str(" ")+str(devices_company_name)
                            }

                            return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        company_device = web_model.CompanyDevices.objects.filter(
                            is_deleted=False, CompanyProductId=CompanyProductId, DeviceCode=DeviceCode).first()
                        device_number_True = len(web_model.CompanyDevices.objects.filter(
                            IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                        device_number_False = len(web_model.CompanyDevices.objects.filter(
                            IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                        try:
                            new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                        except:
                            new_ProductExpiryDate = ""
                        data = {
                            "device_number_True": device_number_True,
                            "device_number_False": device_number_False,
                            "username": request.user.username,
                            "software_plan": company_device.CompanyProductId.software_plan.Name,
                            "Trial": company_device.IsTrialVersion,
                            "CompanyId": company_device.CompanyProductId.CompanyId.pk,
                            "CompanyName": company_device.CompanyProductId.CompanyId.CompanyName,
                            "ProductName": company_device.CompanyProductId.ProductId.Name,
                            "BusinessType": company_device.CompanyProductId.CompanyId.business_type.Name,
                            "Type": company_device.Type,
                            "DeviceName": company_device.DeviceName,
                            "DeviceCode": company_device.DeviceCode,
                            "CompanyProductId": company_device.CompanyProductId.pk,
                            "ProductExpiryDate": company_device.ProductExpiryDate,
                            "ProductId": company_device.CompanyProductId.ProductId.pk,
                            "AMCActive": company_device.CompanyProductId.AMCActive,
                            "AMCExpiry": company_device.CompanyProductId.AMCExpiry,
                            "service_date": company_device.CompanyProductId.service_date,
                            "service": company_device.CompanyProductId.service,
                            "new_ProductExpiryDate": new_ProductExpiryDate,
                            "new_AMCActive": new_AMCActive,
                            "new_AMCExpiry": new_AMCExpiry,
                            "new_service_date": new_service_date,
                        }
                        response_data = {
                            "data": data,
                            "StatusCode": 6001,
                            "message": 'This device already exist'
                        }

                        return Response(response_data, status=status.HTTP_200_OK)
            else:
                CompanyProductId = web_model.CompanyProduct.objects.create(
                    auto_id=get_auto_id(web_model.CompanyProduct),
                    creator=request.user,
                    updater=request.user,
                    ProductId=ProductId,
                    CompanyId=CompanyId,

                    No_ofDevice=1,
                    AMCActive=today,
                    AMCExpiry=exp_date,
                    IsTrialVersion=True,
                    ProductExpiryDate=exp_date,
                    Action="A",
                    software_plan=software_plan,
                )
                company_device = web_model.CompanyDevices.objects.create(
                    auto_id=get_auto_id(web_model.CompanyDevices),
                    creator=request.user,
                    updater=request.user,
                    CompanyProductId=CompanyProductId,
                    DeviceName=DeviceName,
                    DeviceCode=DeviceCode,
                    Type=Type,

                    Action="A",
                    IsTrialVersion=True,
                    ProductExpiryDate=exp_date,
                )
                device_number_True = len(web_model.CompanyDevices.objects.filter(
                    IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                device_number_False = len(web_model.CompanyDevices.objects.filter(
                    IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                try:
                    new_AMCActive = CompanyProductId.AMCActive.date()
                except:
                    new_AMCActive = None
                try:
                    new_AMCExpiry = CompanyProductId.AMCExpiry.date()
                except:
                    new_AMCExpiry = None
                try:
                    new_service_date = CompanyProductId.service_date.date()
                except:
                    new_service_date = None
                try:
                    new_ProductExpiryDate = company_device.ProductExpiryDate.date()
                except:
                    new_ProductExpiryDate = ""
                data = {
                    "device_number_True": device_number_True,
                    "device_number_False": device_number_False,
                    "username": request.user.username,
                    "software_plan": CompanyProductId.software_plan.Name,
                    "Trial": company_device.IsTrialVersion,
                    "CompanyId": pk,
                    "CompanyName": CompanyProductId.CompanyId.CompanyName,
                    "ProductName": CompanyProductId.ProductId.Name,
                    "BusinessType": CompanyProductId.CompanyId.business_type.Name,
                    "Type": Type,
                    "DeviceName": DeviceName,
                    "DeviceCode": DeviceCode,
                    "CompanyProductId": CompanyProductId.pk,
                    "ProductExpiryDate": company_device.ProductExpiryDate,
                    "ProductId": CompanyProductId.ProductId.pk,
                    "AMCActive": CompanyProductId.AMCActive,
                    "AMCExpiry": CompanyProductId.AMCExpiry,
                    "service_date": CompanyProductId.service_date,
                    "service": CompanyProductId.service,
                    "new_ProductExpiryDate": new_ProductExpiryDate,
                    "new_AMCActive": new_AMCActive,
                    "new_AMCExpiry": new_AMCExpiry,
                    "new_service_date": new_service_date,
                }
            response_data = {
                "StatusCode": 6000,
                "data": data,
                "message": 'Successfully Registerd'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                "StatusCode": 6001,
                # "message" : generate_serializer_errors(serialized._errors)
                "message": 'Product does not exists'
            }

            return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def list_company_products(request):
    instances = web_model.CompanyProduct.objects.filter(is_deleted=False)
    serialized = company_serializers.CompanyProductSerializer(
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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_device_details(request):
    DeviceCode = request.GET.get('DeviceCode')
    Productname = request.GET.get('Productname')
    if DeviceCode and Productname:
        if user_model.Product.objects.filter(Name=Productname).exists():
            ProductId = user_model.Product.objects.get(Name=Productname)
            a = web_model.CompanyDevices.objects.filter(
                CompanyProductId__ProductId=ProductId, DeviceCode=DeviceCode)

            if web_model.CompanyDevices.objects.filter(CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__user=request.user, DeviceCode=DeviceCode).exists():
                test1 = web_model.CompanyDevices.objects.filter(
                    CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__user=request.user, DeviceCode=DeviceCode)
                for i in test1:
                    print(i.CompanyProductId.CompanyId)
                    print(i.DeviceCode)
                device = get_object_or_404(web_model.CompanyDevices.objects.filter(
                    CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__user=request.user, DeviceCode=DeviceCode))
                CompanyId = device.CompanyProductId.CompanyId
                Type = device.Type
                DeviceName = device.DeviceName
                DeviceCode = device.DeviceCode
                CompanyProductId = device.CompanyProductId
                ProductExpiryDate = device.CompanyProductId.ProductExpiryDate
                ProductId = device.CompanyProductId.ProductId
                AMCActive = device.CompanyProductId.AMCActive
                AMCExpiry = device.CompanyProductId.AMCExpiry
                service_date = device.CompanyProductId.service_date
                service = device.CompanyProductId.service

                device_number_True = len(web_model.CompanyDevices.objects.filter(
                    IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                device_number_False = len(web_model.CompanyDevices.objects.filter(
                    IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                try:
                    new_AMCActive = CompanyProductId.AMCActive.date()
                except:
                    new_AMCActive = None
                try:
                    new_AMCExpiry = CompanyProductId.AMCExpiry.date()
                except:
                    new_AMCExpiry = None
                try:
                    new_service_date = CompanyProductId.service_date.date()
                except:
                    new_service_date = None
                try:
                    new_ProductExpiryDate = device.ProductExpiryDate.date()
                except:
                    new_ProductExpiryDate = None

                data = {
                    "device_number_True": device_number_True,
                    "device_number_False": device_number_False,
                    "username": request.user.username,
                    "software_plan": CompanyProductId.software_plan.Name,
                    "Trial": device.IsTrialVersion,
                    "CompanyId": CompanyId.pk,
                    "CompanyName": CompanyProductId.CompanyId.CompanyName,
                    "ProductName": CompanyProductId.ProductId.Name,
                    "BusinessType": CompanyProductId.CompanyId.business_type.Name,
                    "Type": Type,
                    "DeviceName": DeviceName,
                    "DeviceCode": DeviceCode,
                    "CompanyProductId": CompanyProductId.pk,
                    "ProductExpiryDate": ProductExpiryDate,
                    "ProductId": ProductId.pk,
                    "AMCActive": AMCActive,
                    "AMCExpiry": AMCExpiry,
                    "service_date": service_date,
                    "service": service,
                    "new_ProductExpiryDate": new_ProductExpiryDate,
                    "new_AMCActive": new_AMCActive,
                    "new_AMCExpiry": new_AMCExpiry,
                    "new_service_date": new_service_date,
                }

                response_data = {
                    "StatusCode": 6000,
                    "data": data,
                    "message": 'Device Found'
                }

                return Response(response_data, status=status.HTTP_200_OK)

            response_data = {
                "StatusCode": 6001,
                "message": 'Device not Registerd'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            "StatusCode": 6001,
            "message": 'Product is not exist'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": 'Device not Registerd'
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_device_details1(request):
    DeviceCode = request.GET.get('DeviceCode')
    Productname = request.GET.get('Productname')
    CompanyId = request.GET.get('CompanyId')
    CompanyProductId = None
    if DeviceCode and Productname and CompanyId:
        if user_model.Product.objects.filter(Name=Productname).exists():
            ProductId = user_model.Product.objects.get(Name=Productname)
            print(ProductId.pk, CompanyId)
            if web_model.CompanyProduct.objects.filter(CompanyId__id=CompanyId, ProductId__id=ProductId.id).exists():
                CompanyProductId = get_object_or_404(web_model.CompanyProduct.objects.filter(
                    CompanyId=CompanyId, ProductId=ProductId))
            a = web_model.CompanyDevices.objects.filter(
                CompanyProductId__ProductId=ProductId, CompanyProductId=CompanyProductId, CompanyProductId__CompanyId__user=request.user, DeviceCode=DeviceCode)
            print(CompanyProductId)
            if web_model.CompanyDevices.objects.filter(CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__user=request.user, CompanyProductId=CompanyProductId, DeviceCode=DeviceCode).exists():
                device = get_object_or_404(web_model.CompanyDevices.objects.filter(CompanyProductId__ProductId=ProductId,
                                           CompanyProductId__CompanyId__user=request.user, CompanyProductId=CompanyProductId, DeviceCode=DeviceCode))
                CompanyId = device.CompanyProductId.CompanyId
                Type = device.Type
                DeviceName = device.DeviceName
                DeviceCode = device.DeviceCode
                CompanyProductId = device.CompanyProductId
                ProductExpiryDate = device.ProductExpiryDate
                ProductId = device.CompanyProductId.ProductId
                AMCActive = device.CompanyProductId.AMCActive
                AMCExpiry = device.CompanyProductId.AMCExpiry
                service_date = device.CompanyProductId.service_date
                service = device.CompanyProductId.service

                device_number_True = len(web_model.CompanyDevices.objects.filter(
                    IsTrialVersion=True, CompanyProductId__CompanyId=CompanyId))
                device_number_False = len(web_model.CompanyDevices.objects.filter(
                    IsTrialVersion=False, CompanyProductId__CompanyId=CompanyId))
                try:
                    new_AMCActive = CompanyProductId.AMCActive.date()
                except:
                    new_AMCActive = None
                try:
                    new_AMCExpiry = CompanyProductId.AMCExpiry.date()
                except:
                    new_AMCExpiry = None
                try:
                    new_service_date = CompanyProductId.service_date.date()
                except:
                    new_service_date = None
                try:
                    new_ProductExpiryDate = device.ProductExpiryDate.date()
                except:
                    new_ProductExpiryDate = None

                data = {
                    "device_number_True": device_number_True,
                    "device_number_False": device_number_False,
                    "username": request.user.username,
                    "software_plan": CompanyProductId.software_plan.Name,
                    "Trial": device.IsTrialVersion,
                    "CompanyId": CompanyId.pk,
                    "CompanyName": CompanyProductId.CompanyId.CompanyName,
                    "ProductName": CompanyProductId.ProductId.Name,
                    "BusinessType": CompanyProductId.CompanyId.business_type.Name,
                    "Type": Type,
                    "DeviceName": DeviceName,
                    "DeviceCode": DeviceCode,
                    "CompanyProductId": CompanyProductId.pk,
                    "ProductExpiryDate": ProductExpiryDate,
                    "ProductId": ProductId.pk,
                    "AMCActive": AMCActive,
                    "AMCExpiry": AMCExpiry,
                    "service_date": service_date,
                    "service": service,
                    "new_ProductExpiryDate": new_ProductExpiryDate,
                    "new_AMCActive": new_AMCActive,
                    "new_AMCExpiry": new_AMCExpiry,
                    "new_service_date": new_service_date,
                }

                response_data = {
                    "StatusCode": 6000,
                    "data": data,
                    "message": 'Device Found'
                }

                return Response(response_data, status=status.HTTP_200_OK)

            response_data = {
                "StatusCode": 6001,
                "message": 'Device not Registerd'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            "StatusCode": 6001,
            "message": 'Product is not exist'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": 'Device not Registerd'
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_device(request):
    data = request.data
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    data_arr = []
    if CompanyID and CompanyProductName:
        if user_model.Product.objects.filter(Name=CompanyProductName).exists():
            ProductId = user_model.Product.objects.get(Name=CompanyProductName)
            if web_model.CompanyDevices.objects.filter(CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__pk=CompanyID).exists():
                devices = web_model.CompanyDevices.objects.filter(
                    CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__pk=CompanyID)
                for i in devices:
                    data = {
                        "DeviceName": i.DeviceName,
                        "DeviceCode": i.DeviceCode,
                    }
                    data_arr.append(data)

                response_data = {
                    "StatusCode": 6000,
                    "data": data_arr,
                }

                return Response(response_data, status=status.HTTP_200_OK)

            response_data = {
                "StatusCode": 6001,
                "message": 'Device not Registerd'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            "StatusCode": 6001,
            "message": 'Product is not exist'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": 'Device not Registerd'
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def create_e_invoice(request):

    data = request.data
    if data:
        pk = data['CompanyID']
        Company_instance = get_instance(pk, web_model.Companies)
        TransactionDate = data['TransactionDate']
        VoucherNo = data['VoucherNo']
        TaxAmount = data['TaxAmount']
        GrandTotal = data['GrandTotal']
        InvoiceID = data['InvoiceID']
        VoucherType = data['VoucherType']

        data = user_model.EInvoice.objects.create(
            auto_id=get_auto_id(user_model.EInvoice),
            creator=request.user,
            updater=request.user,

            TransactionDate=TransactionDate,
            VoucherNo=VoucherNo,
            TaxAmount=TaxAmount,
            GrandTotal=GrandTotal,
            CompanyID=Company_instance,
            InvoiceID=InvoiceID,
            VoucherType=VoucherType,

        )

        response_data = {
            "StatusCode": 6000,
            "EInvoiceID": data.pk,
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
def update_device_code(request):
    data = request.data
    CompanyID = data['CompanyID']
    CompanyProductName = data['CompanyProductName']
    DeviceCode = data['DeviceCode']
    New_DeviceCode = data['NewDeviceCode']

    if CompanyID and CompanyProductName:
        if user_model.Product.objects.filter(Name=CompanyProductName).exists():
            ProductId = user_model.Product.objects.get(Name=CompanyProductName)
            a =web_model.CompanyDevices.objects.filter(CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__pk=CompanyID)
            for i in a:                
                print(i.CompanyProductId.pk)
            if web_model.CompanyDevices.objects.filter(DeviceCode=DeviceCode,CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__pk=CompanyID).exists():
                web_model.CompanyDevices.objects.filter(
                    DeviceCode=DeviceCode,CompanyProductId__ProductId=ProductId, CompanyProductId__CompanyId__pk=CompanyID).update(DeviceCode=New_DeviceCode)
                response_data = {
                    "StatusCode": 6000,
                    "message": "DeviceCode Updated Successfully",
                }
                return Response(response_data, status=status.HTTP_200_OK)

            response_data = {
                "StatusCode": 6001,
                "message": 'Device not Registerd'
            }

            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            "StatusCode": 6001,
            "message": 'Product is not exist'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "StatusCode": 6001,
        "message": 'Device not Registerd'
    }

    return Response(response_data, status=status.HTTP_200_OK)

