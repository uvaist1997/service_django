from rest_framework import serializers
from users import models as user_model
from web import models as web_model
from django.utils.text import Truncator


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.Payment
        fields = ('id','GUID','VoucherType','TransactionId','Van_ID','Route_ID','CashOrBankId','Date','PaymentGateway','RefferenceNo','CardNetwork','PaymentStatus','DueDate','LedgerId','Amount','Discount','NetAmount','Balance','Narration','status',)




class PaymentSerializer(serializers.ModelSerializer):

    PaymentDetails = serializers.SerializerMethodField()

    class Meta:
        model = web_model.Payment
        fields = ('id','GUID','status','CompanyProductId','Date','TotalAmount','CashAccountId','Van_ID','Route_ID','TransactionId','PaymentDetails')
        

    def get_PaymentDetails(self, instances):
        PaymentId = instances.id
        payment_details = web_model.PaymentDetail.objects.filter(PaymentId=PaymentId)
        serialized = PaymentDetailsSerializer(payment_details,many=True,)

        return serialized.data 


class PaymentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.PaymentDetail
        fields = ('id','TransactionId','amount','notes','LedgerId')