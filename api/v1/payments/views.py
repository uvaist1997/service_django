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
from api.v1.payments import serializers as payment_serializers
from users import models as user_model
from web import models as web_model
from django.shortcuts import render, get_object_or_404


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_payments(request):
	data = request.data
	CompanyID = data['CompanyID']
	CompanyProductName = data['CompanyProductName']

	if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName).exists():
		companyproduct_ins = web_model.CompanyProduct.objects.get(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName)
	
		instances = web_model.Payment.objects.filter(status=False,CompanyProductId=companyproduct_ins)
		serialized = payment_serializers.PaymentSerializer(instances,many=True)
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
def create_payments(request):

	data = request.data
	Payments = data["Payments"]
	tran_data=[]
	if Payments:
		print(Payments)

		for data in Payments:
			pk = data['CompanyProductId']

			try:
				GUID = data['GUID']
			except:
				GUID = None


			CompanyProductId = get_instance(pk,web_model.CompanyProduct)
			print(CompanyProductId,'CompanyProductId')
			auto_id = get_auto_id(web_model.Payment)
			paymentdetails = data["PaymentDetails"]
			if paymentdetails:
				payment = web_model.Payment.objects.create(
					auto_id = auto_id,
					creator = request.user,
					updater = request.user,
					CompanyProductId = CompanyProductId,
					Date = data['Date'],
					TotalAmount = data['TotalAmount'],
					CashAccountId = data['CashAccountId'],
					TransactionId = data['TransactionId'],
					Van_ID = data['Van_ID'],
					Route_ID = data['Route_ID'],
					GUID=GUID

				)
				tran_data.append(payment.TransactionId)

				for paymentdetail in paymentdetails:
					TransactionId = paymentdetail['TransactionId']
					print(TransactionId,'TransactionId')
					amount = paymentdetail['amount']
					LedgerId = paymentdetail['LedgerId']
					notes = paymentdetail['notes']
					web_model.PaymentDetail.objects.create(
						TransactionId=TransactionId,
						amount=amount,
						notes=notes,
						LedgerId=LedgerId,
						PaymentId=payment,
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
def edit_payment(request):
	data = request.data
	pk = data['id']
	if pk:
		if web_model.Payment.objects.filter(status=False,pk=pk).exists():
			instance = get_object_or_404(web_model.Payment.objects.filter(status=False,pk=pk))			
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