from users.models import UserDetails
from web import models
# from products import models as pro_models
# from customers.models import Customer
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.v1.users.serializers import LoginSerializer, DatabaseDetailSerializer, UserDeviceDetailsSerializer, OTPSerializer, CustomerSerializer, ProfileSerializer
from api.v1.users.functions import generate_serializer_errors, get_auto_id, get_otp, get_ip
from api.v1.general.functions import generate_serializer_errors, call_paginator_all, list_pagination
from rest_framework import status
import requests
from api.v1.general.functions import get_current_role, get_auto_id
from django.views.decorators.csrf import csrf_exempt
import json
from web import models as web_model
from users import models as user_model
from api.v1.users import serializers as user_serializers
import re
import datetime


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@csrf_exempt
def user_login(request):
    print(request.data)
    serialized = LoginSerializer(data=request.data)

    if serialized.is_valid():
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        username = serialized.data['username']
        print(username, "USERNAME")
        password = serialized.data['password']
        if username and password:
            # if models.Register.objects.filter(user__username=username).exists():
            # if(re.search(regex,username)):
            if User.objects.filter(email=username).exists():
                print('email')
                user = User.objects.get(email=username)
            elif User.objects.filter(username=username).exists():
                print('username')
                user = User.objects.get(username=username)
            else:
                print('user')
                user = None

            if user is not None:
                user = authenticate(username=username, password=password)
                if user is not None:
                    print(
                        user, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    login(request, user)

                    request.session['current_role'] = get_current_role(request)

                    headers = {
                        'Content-Type': 'application/json',
                    }

                    data = '{"username": "' + user.username + \
                        '", "password": "' + password + '" }'

                    # protocol = "http://"
                    # if request.is_secure():
                    protocol = "https://"

                    web_host = request.get_host()
                    request_url = protocol + web_host + "/api/v1/auth/token/"
                    response = requests.post(
                        request_url, headers=headers, data=data)
                    print(response.status_code, 'GGGGGGGGGGGg')
                    if response.status_code == 200:
                        user_instance = User.objects.get(username=username)
                        if not UserDetails.objects.filter(user=user_instance).exists():
                            UserDetails.objects.create(
                                user=user_instance,
                                password=password,
                            )
                        data = response.json()
                        success = 6000
                        message = "Login successfully"

                        response_data = {
                            'success': success,
                            'data': data,
                            'message': "Login successfully",
                            'error': None
                        }
                        status_code = status.HTTP_200_OK
                    else:
                        success = 6001
                        error = "Some error occured please contact admin to solve this problem."

                        response_data = {
                            'success': success,
                            'data': None,
                            'error': error
                        }
                        status_code = status.HTTP_400_BAD_REQUEST

                    return Response(
                        response_data,
                        status=status_code
                    )
                else:
                    success = 6001
                    data = None
                    error = "username or password not correct"
                    return Response(
                        {
                            'success': success,
                            'data': data,
                            'error': error
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                success = 6001
                data = None
                error = "User not found"
                return Response(
                    {
                        'success': success,
                        'data': data,
                        'error': error
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            message = "user is not exists"
            success = 6001
            data = None
            return Response(
                {
                    'success': success,
                    'data': data,
                    'error': message
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # else:
        #   user = User.objects.create_user(
        #       username=phone,
        #       password=password
        #   )

        #   auto_id = get_auto_id(models.RegistrationProfile)
        #   profile = models.RegistrationProfile(
        #       phone=phone,
        #       auto_id=auto_id,
        #       user=user,
        #   )
        #   profile.save()

        #   if Group.objects.filter(name="customer_user").exists():
        #       group = Group.objects.get(name="customer_user")
        #   else:
        #       group = Group.objects.create(name="customer_user")

        #   user.groups.add(group)

        #   auto_id = get_auto_id(models.UserLogin)
        #   otp = get_otp()

        #   userLogin = models.UserLogin(
        #       auto_id = auto_id,
        #       ip = get_ip(request),
        #       user = user,
        #       otp = otp
        #   )
        #   userLogin.save()

        #   data = {
        #       "otp" : userLogin.otp,
        #       "pk" : userLogin.pk
        #   }

        #   success = 6000
        #   return Response(
        #       {
        #           'success': success,
        #           'data': data,
        #           'error' : None
        #       },
        #       status=status.HTTP_200_OK
        #   )
    else:
        print(serialized.errors)
        print('serialized._errors')
        message = generate_serializer_errors(serialized.errors)
        success = 6001
        data = None
        return Response(
            {
                'success': success,
                'data': data,
                'error': message
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def verify(request, pk):
    serialized = OTPSerializer(data=request.data)

    if serialized.is_valid():

        # Getting user instance
        if models.UserLogin.objects.filter(pk=pk).exists():
            instance = models.UserLogin.objects.get(pk=pk)
        else:
            instance = None

        # Getting otp
        otp = serialized.data['otp']
        phone = serialized.data['phone']
        password = serialized.data['password']

        # Verify user
        if instance is not None and otp == instance.otp:
            instance.is_activated = True
            instance.save()
            user = authenticate(username=phone, password=password)

            if user is not None:
                login(request, user)

                headers = {
                    'Content-Type': 'application/json',
                }

                data = '{"username": "' + phone + \
                    '", "password": "' + password + '" }'

                # protocol = "http://"
                # if request.is_secure():
                protocol = "https://"

                web_host = request.get_host()
                request_url = protocol + web_host + "/api/v1/auth/token/"
                response = requests.post(
                    request_url, headers=headers, data=data)

                if response.status_code == 200:
                    data = response.json()
                    success = 6000
                    message = "Login successfully"
                    return Response(
                        {
                            'success': success,
                            'data': data,
                            'message': message,
                            'error': None
                        },
                        status=status.HTTP_200_OK)
                else:
                    success = 6001
                    data = None
                    error = "Some error occured please contact admin to solve this problem."
                    return Response(
                        {
                            'success': success,
                            'data': data,
                            'error': error
                        },
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                success = 6001
                data = None
                error = "User not found"
                return Response(
                    {
                        'success': success,
                        'data': data,
                        'error': error
                    },
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            success = 6001
            data = None
            error = "Invalid OTP. Please try again"
            return Response(
                {
                    'success': success,
                    'data': data,
                    'error': error
                },
                status=status.HTTP_400_BAD_REQUEST)
    else:
        message = generate_serializer_errors(serialized._errors)
        success = 6001
        data = None
        return Response(
            {
                'success': success,
                'data': data,
                'error': message
            },
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def user_registration(request):

    data = request.data
    print(data, '@@@@@@@@@@@@@@@@')
    # Customers = data["Customers"]
    if data:
        first_name = data['FirstName']
        last_name = data['LastName']
        username = data['Username']
        email = data['Email']
        password = data['Password']
        phone = data['Phone']
        auto_id = get_auto_id(models.Register)
        if not User.objects.filter(email=email).exists():
            if not User.objects.filter(username=username).exists():

                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                    is_superuser=False
                )

                models.Register.objects.create(

                    PhoneNumber=phone,
                    auto_id=auto_id,
                    creator=user,
                    user=user
                )
            # data = [{
            #   "results": data,
            # }]
            # response_data = {
            #   "StatusCode" : 6000,
            #   "data" : data,
            #   "message" : 'Successfully Created'
            # }
                data = {
                    "results": data,
                }
                return Response(
                    {
                        'success': 6000,
                        'data': data,
                        'message': "success"
                    },
                    status=status.HTTP_200_OK)

        # return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "success": 6001,
                    # "message" : generate_serializer_errors(serialized._errors)
                    "message": 'Username already exists'
                }

                return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "success": 6001,
                # "message" : generate_serializer_errors(serialized._errors)
                "message": 'Email already exists'
            }

            return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "success": 6001,
            # "message" : generate_serializer_errors(serialized._errors)
            "message": 'Data does not exists'
        }

        return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
# def user_registration(request):
#     today = datetime.date.today()
#     serialized = SignupSerializer(data=request.data)

#     if serialized.is_valid():
#         first_name = serialized.validated_data['first_name']
#         last_name = serialized.validated_data['last_name']
#         username = serialized.validated_data['username']
#         email = serialized.validated_data['email']
#         password1 = serialized.validated_data['password1']
#         password2 = serialized.validated_data['password2']
#         message = ""
#         error = False

#         bad_domains = ['guerrillamail.com']

#         email_domain = email.split('@')[1]
#         if User.objects.filter(email__iexact=email,is_active=True):
#             message = "This email address is already in use."
#             error = True
#         elif email_domain in bad_domains:
#             message = ("Registration using %s email addresses is not allowed. Please supply a different email address.") %email_domain
#             error = True
#             email = email

#         min_password_length = 6

#         if len(password1) < min_password_length:
#             message = ("Password must have at least %i characters" % min_password_length)
#             error = True
#         else:
#             password1 = password1

#         if password1 and password2 and password1 != password2:
#             message = 'password_mismatch'
#             error = True
#             password2 = password2

#         min_username_length = 6

#         existing = User.objects.filter(username__iexact=username)
#         if existing.exists():
#             message = "A user with that username already exists."
#             error = True
#         elif len(username) < min_username_length:
#             message = ("Username must have at least %i characters" % min_password_length)
#             error = True
#         else:
#             username = username


#         if not error:
#             # serialized.save()
#             user = User.objects.create_user(
#                 first_name = first_name,
#                 last_name = last_name,
#                 email = email,
#                 username = username,
#                 password = password1,
#                 is_superuser = False,
#                 )
#             # Customer.objects.create(
#             #     user = user,
#             #     )

#             response_data = {
#                 "StatusCode" : 6000,
#                 "data" : serialized.data
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             response_data = {
#             "StatusCode" : 6001,
#             "message" : message
#         }

#         return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         response_data = {
#             "StatusCode" : 6001,
#             "message" : generate_serializer_errors(serialized._errors)
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


# =========================
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((JSONRenderer,))
# @csrf_exempt
# def customer_entry(request):
#   print(request.data)
#   data = request.data.dict()

#   if 'photo' in request.data:
#       data['photo'] = request.data['photo']

#   serialized = CustomerSerializer(data=data)

#   if serialized.is_valid():
#       name = serialized.data['name']
#       gender = serialized.data['gender']
#       email = serialized.data['email']
#       address = serialized.data['address']

#       if 'photo' in request.data:
#           photo = request.data['photo']

#       auto_id = get_auto_id(Customer)
#       is_edit = False

#       if Customer.objects.filter(is_deleted=False,user=request.user).exists():
#           customer = Customer.objects.get(is_deleted=False,user=request.user)
#           is_edit = True
#       else:
#           customer = Customer()

#       user_profile = models.RegistrationProfile.objects.get(is_deleted=False,user=request.user)

#       customer.name=name
#       customer.gender=gender
#       customer.email=email
#       customer.address=address
#       customer.photo=photo
#       if not is_edit:
#           customer.phone=user_profile.phone
#           customer.auto_id=auto_id
#           customer.user=request.user
#           customer.creator=request.user
#       customer.updater=request.user

#       customer.save()

#       data = serialized.data
#       success = 6000
#       message = "Profile Updated"

#       response_data = {
#           'success': success,
#           'data': data,
#           'message' : message,
#           'error' : None
#       }
#       status_code=status.HTTP_200_OK

#       return Response(
#           response_data,
#           status=status_code
#       )
#   else:
#       message = generate_serializer_errors(serialized._errors)
#       success = 6001
#       data = None
#       return Response(
#           {
#               'success': success,
#               'data': data,
#               'error': message
#           },
#           status=status.HTTP_400_BAD_REQUEST
#       )


# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((JSONRenderer,))
# def single_customer(request):
#   if Customer.objects.filter(is_deleted=False,user=request.user).exists():
#       instances = Customer.objects.get(is_deleted=False,user=request.user)
#       order_serializer = ProfileSerializer(instances,context={"request":request})
#       data = order_serializer.data
#       return Response(
#           {
#               'success': 6000,
#               'data': data,
#               'error': None
#           },
#           status=status.HTTP_200_OK
#       )
#   else:
#       success = 6001
#       data = None
#       message = 'No user details available'
#       return Response(
#           {
#               'success': success,
#               'data': data,
#               'error': message
#           },
#           status=status.HTTP_400_BAD_REQUEST
#       )


# @api_view(['GET'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
# def categories(request):
#   if 'page_no' in request.GET:
#       page_number = int(request.GET['page_no'])
#   else:
#       page_number = None

#   if 'items_per_page' in request.GET:
#       items_per_page = int(request.GET['items_per_page'])
#   else:
#       items_per_page = None

#   if page_number and items_per_page:
#       category_object = pro_models.Category.objects.filter(is_deleted=False)

#       category_sort_pagination = list_pagination(
#           category_object,
#           items_per_page,
#           page_number
#       )
#       category_serializer = CategorySerializer(
#           category_sort_pagination,
#           many=True
#       )
#       data = category_serializer.data

#       data = {
#           "results": data,
#           "count": len(category_object)
#       }
#       return Response(
#           {
#               'success': 6000,
#               'data': data,
#               'error': None
#           },
#           status=status.HTTP_200_OK
#       )
#   else:
#       success = 6001
#       error = "No Parameter Passed. Parameters are (items_per_page & page_number)"
#       return Response(
#           {
#               'success': success,
#               'data': None,
#               'error': error
#           },
#           status=status.HTTP_400_BAD_REQUEST
#       )


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def list_users(request):
    # data = request.data
    # print(data,'@@@@@@@@@########')
    # saleproducts = data['saleproducts']
    # if saleproducts:
    # for data in saleproducts:
    instances = User.objects.filter(is_active=True, is_superuser=False)
    serialized = user_serializers.UserSerializer(instances, many=True)
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

    # else:
    #   success = 6001
    #   error = "error"
    #   return Response(
    #       {
    #           'success': success,
    #           'data': None,
    #           'error': error
    #       },
    #       status=status.HTTP_400_BAD_REQUEST
    #   )


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
# def database_detail(request):

#     data = request.data
#     companyproduct = None
#     if data:
#         file = data['file']
#         print(file)
#         CompanyProductId = data['CompanyProductId']
#         VanId = data['VanId']
#         if web_model.CompanyProduct.objects.filter(pk=CompanyProductId).exists():
#             companyproduct = web_model.CompanyProduct.objects.get(pk=CompanyProductId)
#         if companyproduct:
#             web_model.DatabaseDetail.objects.create(
#                 file=file,
#                 CompanyProductId=companyproduct,
#                 VanId=VanId,
#                 )


#             return Response(
#                 {
#                     'success': 6000,
#                     'data': data,
#                     'message': "success"
#                 },
#                 status=status.HTTP_200_OK)

#         else:
#             response_data = {
#                 "success" : 6001,
#                  "message" : 'error'
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         response_data = {
#             "success" : 6001,
#              "message" : 'Data does not exists'
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def database_detail(request):
    data = request.data

    serialized = DatabaseDetailSerializer(
        data=request.data, context={"request": request})
    companyproduct = None
    if serialized.is_valid():
        file = data['file']
        today = datetime.datetime.now()
        print(data['file'], "FILEEEEEE")
        CompanyProductId = data['CompanyProductId']
        if web_model.CompanyProduct.objects.filter(pk=CompanyProductId).exists():
            companyproduct = web_model.CompanyProduct.objects.get(
                pk=CompanyProductId)
        VanId = data['VanId']
        if companyproduct:
            web_model.DatabaseDetail.objects.create(
                CreatedDate=today,
                file=file,
                CompanyProductId=companyproduct,
                VanId=VanId,
            )
            # serialized.save(using=CompanyID)
            response_data = {
                "StatusCode": 6000,
                "message": "Successfully Created"
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "StatusCode": 6001,
                "message": "CompanyProduct not exists"
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": serialized._errors
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_user_device_detail(request):
    data = request.data

    companyproduct = None

    Device_Code = data['Device_Code']
    Application_Version = data['Application_Version']
    Device_Name = data['Device_Name']
    today = datetime.datetime.now()
    CompanyProductId = data['CompanyProductId']
    if web_model.CompanyProduct.objects.filter(pk=CompanyProductId).exists():
        companyproduct = web_model.CompanyProduct.objects.get(
            pk=CompanyProductId)
    # remove UserDeviceDetails
    VanId = data['VanId']
    if user_model.UserDeviceDetails.objects.filter(CompanyProductId=companyproduct.pk, VanId=VanId).exists():
        user_device_detail = user_model.UserDeviceDetails.objects.get(
            CompanyProductId=companyproduct.pk, VanId=VanId)
        user_device_detail.delete()
    if companyproduct:
        user_model.UserDeviceDetails.objects.create(
            auto_id=get_auto_id(user_model.UserDeviceDetails),
            creator=request.user,
            updater=request.user,
            Device_Code=Device_Code,
            Application_Version=Application_Version,
            Device_Name=Device_Name,
            CompanyProductId=companyproduct,
            VanId=VanId,
        )
        # serialized.save(using=CompanyID)
        response_data = {
            "StatusCode": 6000,
            "message": "Successfully Created"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "CompanyProduct not exists"
        }
    return Response(response_data, status=status.HTTP_200_OK)
