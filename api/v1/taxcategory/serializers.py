from rest_framework import serializers
from users import models as user_model
from web import models as web_model
from django.utils.text import Truncator


class TaxCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.TaxCategory
        fields = ('id','CompanyProductId','TaxId','BranchId','TaxName','TaxType','PurchaseTax','SalesTax','Inclusive','SyncDate')


