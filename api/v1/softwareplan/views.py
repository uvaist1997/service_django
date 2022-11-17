from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from api.v1.general.functions import generate_serializer_errors, call_paginator_all, list_pagination
from api.v1.softwareplan import serializers as soft_serializers

from web import models as web_model
from users import models as user_model


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def list_software_plans(request):
	instances = user_model.SoftwarePlan.objects.filter(is_deleted=False)
	serialized = soft_serializers.SoftwarePlanSerializer(instances,many=True)
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
