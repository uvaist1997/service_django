from rest_framework import serializers
from web import models as web_model
from users import models as user_model
from django.utils.text import Truncator


class BusinessTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model.BusinessType
        fields = ('id','Name','Description','Action')



class SingleBusinessSerializers(serializers.ModelSerializer):
	
	class Meta:
		model = user_model.BusinessType
		fields = (
			'id',
			'Name',
			'Description',
			'Action',
		)


