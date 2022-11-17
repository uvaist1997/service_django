from rest_framework import serializers
from users import models as user_model
from web import models as web_model
from django.utils.text import Truncator


# class RecieptSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = web_model.Reciept
#         fields = ('id','CompanyProductId','TransactionId','CashOrBankId','Date','PaymentGateway','RefferenceNo','CardNetwork','PaymentStatus','DueDate','LedgerId',)


# class CompanyProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = web_model.CompanyProduct
#         fields = ('id','CompanyID','ProudctID','No_ofDevice','ProductExpiryDate','AMCActive','AMCExpiry','IsTrialVersion','Action')




class RecieptSerializer(serializers.ModelSerializer):

    RecieptDetails = serializers.SerializerMethodField()

    class Meta:
        model = web_model.Reciept
        fields = ('id','GUID','status','Van_ID','Advance_Payment','CompanyProductId','CashAccountID','TransactionId','CashOrBankId','Date','PaymentGateway','RefferenceNo','CardNetwork','PaymentStatus','DueDate','LedgerId','TotalAmount','Discount','RecieptDetails')
        

    def get_RecieptDetails(self, instances):
        RecieptId = instances.id
        reciept_details = web_model.RecieptDetail.objects.filter(RecieptId=RecieptId)
        serialized = RecieptDetailsSerializer(reciept_details,many=True,)

        return serialized.data 


class RecieptDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.RecieptDetail
        fields = ('id','TransactionId','amount','VoucherNumber','Due_Amount')