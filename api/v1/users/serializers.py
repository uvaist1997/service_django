from rest_framework import serializers
from users import models as user_model
from web import models as web_model
# from customers.models import Customer
# from products import models
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class DatabaseDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = web_model.DatabaseDetail
        fields = ('id','file','VanId')


class UserDeviceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model.UserDeviceDetails
        fields = ('id','Application_Version','Device_Code','Device_Name','VanId')

# class LoginSerializer(serializers.Serializer):
#     email_or_username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         email_or_username = attrs.get('email_or_username')
#         password = attrs.get('password')

#         if email_or_username and password:
#             # Check if user sent email
#             if validateEmail(email_or_username):
#                 user_request = get_object_or_404(
#                     User,
#                     email=email_or_username,
#                 )

#                 email_or_username = user_request.username

#             user = authenticate(username=email_or_username, password=password)

#             if user:
#                 if not user.is_active:
#                     msg = _('User account is disabled.')
#                     raise exceptions.ValidationError(msg)
#             else:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg = _('Must include "email or username" and "password"')
#             raise exceptions.ValidationError(msg)

#         attrs['user'] = user
#         return attrs


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)
    phone = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)


class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=100)
    photo = serializers.ImageField(max_length=100,required=False)


class ProfileSerializer(serializers.ModelSerializer):
	# customer_image = serializers.SerializerMethodField()

	def get_customer_image(self, instance):
		request = self.context.get('request')
		protocol = "http://"
		if request.is_secure():
			protocol = "https://"

		web_host = request.get_host()
		request_url = protocol + web_host + '/media/'

		image = request_url + str(instance.photo)
		return image

# 	class Meta:
# 		model = Customer
# 		fields = (
# 			'id',
# 			'name',
# 			'photo',
# 			'phone',
# 			'address',
# 			'district',
# 			'place',
# 		)


# class CategorySerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = models.Category
# 		fields = (
# 			'id',
# 			'name',
# 			# 'photo',
# 		)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email')


