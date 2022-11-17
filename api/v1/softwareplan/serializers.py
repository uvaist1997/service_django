from rest_framework import serializers
from web import models as web_model
from users import models as user_model
from django.utils.text import Truncator


class SoftwarePlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model.SoftwarePlan
        fields = ('id','Name','Description','Action')