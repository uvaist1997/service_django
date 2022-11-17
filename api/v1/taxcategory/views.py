from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from api.v1.general.functions import generate_serializer_errors, call_paginator_all, list_pagination
from api.v1.taxcategory import serializers
import datetime
from web import models as web_model
from users import models as user_model
from api.v1.users.functions import get_auto_id
# from main.functions import get_auto_id


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def list_tax_category(request):
	data = request.data
	CompanyProductId = data['CompanyProductId']
	instances = web_model.TaxCategory.objects.filter(CompanyProductId=CompanyProductId,is_deleted=False)
	serialized = serializers.TaxCategorySerializer(instances,many=True)
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
def create_tax_category(request):
	today = datetime.datetime.now()
	data = request.data
	comp_instance = None
	CompanyID = data['CompanyID']
	CompanyProductName = data['CompanyProductName']
	if web_model.CompanyProduct.objects.filter(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName).exists():
		comp_instance = web_model.CompanyProduct.objects.get(CompanyId__pk=CompanyID,ProductId__Name=CompanyProductName)
		instances = web_model.TaxCategory.objects.filter(CompanyProductId=comp_instance)
		for i in instances:
			i.delete()


	Taxcategory = data["Taxcategory"]
	if Taxcategory:
		for data in Taxcategory:			

			TaxId = data['TaxID']
			BranchId = data['BranchID']
			TaxName = data['TaxName']
			TaxType = data['TaxType']
			PurchaseTax = data['PurchaseTax']
			SalesTax = data['SalesTax']

			try:
				Inclusive = data['Inclusive']				
			except:
				Inclusive = False				
			print(get_auto_id(web_model.TaxCategory),'get_auto_id(web_model.TaxCategory)')
			web_model.TaxCategory.objects.create(
				auto_id = get_auto_id(web_model.TaxCategory),
				creator = request.user,
				updater = request.user,
				TaxId = TaxId,
				BranchId = BranchId,
				CompanyProductId = comp_instance,
				TaxName = TaxName,
				TaxType = TaxType,
				PurchaseTax = PurchaseTax,
				SalesTax = SalesTax,
				SyncDate = today,
				Inclusive = Inclusive
			)


		response_data = {
			"StatusCode" : 6000,
			"message" : 'Successfully Created'
		}

		return Response(response_data, status=status.HTTP_200_OK)
			

		# response_data = {
		# 	"StatusCode" : 6000,
		# 	"data" : Saleproduct,
		# 	"message" : 'Successfully Created'
		# }

		# return Response(response_data, status=status.HTTP_200_OK)
	else:
		response_data = {
			"StatusCode" : 6001,
			# "message" : generate_serializer_errors(serialized._errors)
			 "message" : 'Data does not exists'
		}

		return Response(response_data, status=status.HTTP_200_OK)