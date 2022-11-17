import string
import random


def generate_serializer_errors(args):
	message = ""
	for key, values in args.items():
		error_message = ""
		for value in values:
			error_message += value + ","
		error_message = error_message[:-1]

		message += "%s : %s | " %(key,error_message)
	return message[:-3]


def get_otp(size=4,chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    return ipaddress


def get_auto_id(Model):
    auto_id = 1
    latest_auto_id =  Model.objects.all().order_by("-auto_id")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            print(auto.auto_id,'latest_auto_id')
            auto_id = auto.auto_id + 1
    return auto_id