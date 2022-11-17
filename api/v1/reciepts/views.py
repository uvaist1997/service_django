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
from api.v1.reciepts import serializers as reciept_serializers
from users import models as user_model
from web import models as web_model
from django.shortcuts import render, get_object_or_404


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def list_reciepts(request):
	data = request.data
	CompanyID = data['CompanyID']
	CompanyProductName = data['CompanyProductName']
	if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName).exists():
		companyproduct_ins = web_model.CompanyProduct.objects.get(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName)
		
	instances = web_model.Reciept.objects.filter(is_deleted=False,CompanyProductId=companyproduct_ins,status=False)
	print(instances,'ddddddddddddddddddddddddddd')
	serialized = reciept_serializers.RecieptSerializer(instances,many=True)
	data = serialized.data
	if data:
		# data = {
		# 	"results": data,
		# 	"count": len(instances)
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
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_reciepts(request):

	data = request.data
	Reciepts = data["Reciepts"]
	if Reciepts:
		print(Reciepts)
		tran_data = []
		for data in Reciepts:
			pk = data['CompanyProductId']
			print(data['Date'],"RECIEPT DATE..........")
			CompanyProductId = get_instance(pk,web_model.CompanyProduct)
			print(CompanyProductId,'CompanyProductId')
			auto_id = get_auto_id(web_model.Reciept)
			try:
				PaymentGateway = data['PaymentGateway']
			except:
				PaymentGateway = None
			try:
				RefferenceNo = data['RefferenceNo']
			except:
				RefferenceNo = None
			try:
				CardNetwork = data['CardNetwork']
			except:
				CardNetwork = None
			try:
				PaymentStatus = data['PaymentStatus']
			except:
				PaymentStatus = None
			reciept_instance = web_model.Reciept.objects.create(
				auto_id = auto_id,
				creator = request.user,
				updater = request.user,
				CompanyProductId = CompanyProductId,
				VoucherType = data['VoucherType'],
				TransactionId = data['TransactionId'],
				CashOrBankId = data['CashOrBankId'],
				Date = data['Date'],
				PaymentGateway = PaymentGateway,
				RefferenceNo = RefferenceNo,
				CardNetwork = CardNetwork,
				PaymentStatus = PaymentStatus,
				DueDate = data['DueDate'],
				LedgerId = data['LedgerId'],
				Amount = data['Amount'],
				Discount = data['Discount'],
				TotalAmount = data['TotalAmount'],
				Balance = data['Balance'],
				Van_ID = data['Van_ID'],
				Narration = data['Narration'],
				Advance_Payment = data['Advance_Payment'],
				CashAccountID = data['CashAccountID'],
				
			)
			tran_data.append(reciept_instance.TransactionId)
			recieptdetails = data["RecieptDetails"]

			for recieptdetail in recieptdetails:

				TransactionId = recieptdetail['TransactionId']
				amount = recieptdetail['amount']
				voucherNumber = recieptdetail['voucherNumber']
				Due_Amount = recieptdetail['Due_Amount']
				web_model.RecieptDetail.objects.create(
					TransactionId=TransactionId,
					amount=amount,
					VoucherNumber=voucherNumber,
					RecieptId=reciept_instance,
					Due_Amount=Due_Amount,
					)

		response_data = {
			"StatusCode" : 6000,
			"data" : tran_data,
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
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def create_single_reciept(request):

	data = request.data
	tran_data = []
	if data:
		pk = data['CompanyProductId']
		print(data['Date'],"RECIEPT DATE..........")
		CompanyProductId = get_instance(pk,web_model.CompanyProduct)
		print(CompanyProductId,'CompanyProductId')
		auto_id = get_auto_id(web_model.Reciept)
		try:
			PaymentGateway = data['PaymentGateway']
		except:
			PaymentGateway = None
		try:
			RefferenceNo = data['RefferenceNo']
		except:
			RefferenceNo = None
		try:
			CardNetwork = data['CardNetwork']
		except:
			CardNetwork = None
		try:
			PaymentStatus = data['PaymentStatus']
		except:
			PaymentStatus = None
		try:
			GUID = data['GUID']
		except:
			GUID = None

		reciept_instance = web_model.Reciept.objects.create(
			auto_id = auto_id,
			creator = request.user,
			updater = request.user,
			CompanyProductId = CompanyProductId,
			VoucherType = data['VoucherType'],
			TransactionId = data['TransactionId'],
			CashOrBankId = data['CashOrBankId'],
			Date = data['Date'],
			PaymentGateway = PaymentGateway,
			RefferenceNo = RefferenceNo,
			CardNetwork = CardNetwork,
			PaymentStatus = PaymentStatus,
			DueDate = data['DueDate'],
			LedgerId = data['LedgerId'],
			Amount = data['Amount'],
			Discount = data['Discount'],
			TotalAmount = data['TotalAmount'],
			Balance = data['Balance'],
			Van_ID = data['Van_ID'],
			Narration = data['Narration'],
			Advance_Payment = data['Advance_Payment'],
			CashAccountID = data['CashAccountID'],
			GUID=GUID,
			
		)
		tran_data.append(reciept_instance.TransactionId)
		recieptdetails = data["RecieptDetails"]

		for recieptdetail in recieptdetails:

			TransactionId = recieptdetail['TransactionId']
			amount = recieptdetail['amount']
			voucherNumber = recieptdetail['voucherNumber']
			Due_Amount = recieptdetail['Due_Amount']
			web_model.RecieptDetail.objects.create(
				TransactionId=TransactionId,
				amount=amount,
				VoucherNumber=voucherNumber,
				RecieptId=reciept_instance,
				Due_Amount=Due_Amount,
				)

		response_data = {
			"StatusCode" : 6000,
			"data" : tran_data,
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
def edit_reciepts(request):
	data = request.data
	pk = data['id']
	# Reciepts = data["Reciepts"]
	if pk:
		# for data in Reciepts:

		if web_model.Reciept.objects.filter(status=False,pk=pk).exists():
			# instance = get_object_or_404(web_model.Reciept.objects.filter(status=False,CompanyProductId=CompanyProductId))
			instance = get_object_or_404(web_model.Reciept.objects.filter(status=False,pk=pk))			
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