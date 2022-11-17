from rest_framework import serializers
from web import models as web_model
from web import models as web_model
from django.utils.text import Truncator


class CompaniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.Companies
        fields = ('id','CompanyName','Country','State','OfficePhoneNumber','Email')


class CompanyProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.CompanyProduct
        fields = ('id','CompanyID','ProudctID','No_ofDevice','ProductExpiryDate','AMCActive','AMCExpiry','IsTrialVersion','Action')




