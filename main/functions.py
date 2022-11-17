import threading
import time
import string
import random
from django.http import HttpResponse
from decimal import Decimal
from main.models import Settings
import datetime
from django.conf import settings


def get_otp(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    return ipaddress


def generate_form_errors(args, formset=False):
    message = ''
    if not formset:
        for field in args:
            if field.errors:
                message += field.errors + "|"
        for err in args.non_field_errors():
            message += str(err) + "|"

    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += field.errors + "|"
            for err in form.non_field_errors():
                message += str(err) + "|"
    return message[:-1]


def get_auto_id(model):
    auto_id = 1
    latest_auto_id = model.objects.all().order_by("-date_added")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def get_a_id(model, request):
    a_id = 1
    latest_a_id = model.objects.all().order_by("-date_added")[:1]
    if latest_a_id:
        for auto in latest_a_id:
            a_id = auto.a_id + 1
    return a_id


def get_current_role(request):
    is_superadmin = False
    is_customer_user = False
    is_vendor_user = False

    current_role = "user"
    if request.user.is_authenticated:
        groups = request.user.groups.all()

        if request.user.is_superuser:
            is_superadmin = True
        elif groups.filter(name="customer_user").exists():
            is_customer_user = True
        elif groups.filter(name="vendor_user").exists():
            is_vendor_user = True

        if "current_role" in request.session:
            role = request.session['current_role']
            if role == "superadmin":
                current_role = "superadmin"
            elif role == "customer_user":
                current_role = "customer_user"
            elif role == "vendor_user":
                current_role = "vendor_user"
        else:
            if is_superadmin:
                current_role = "superadmin"
            elif is_customer_user:
                current_role = "customer_user"
            elif is_vendor_user:
                current_role = "vendor_user"

        return current_role


def get_purchase_no(Model):
    purchase_no = 1
    if Model.objects.all().exists():
        latest_purchase_no = Model.objects.all().latest("date_added")
        print(latest_purchase_no)
        purchase_no = latest_purchase_no.purchase_no + 1
    return purchase_no


def get_settings_sale():
    instance, created = Settings.objects.get_or_create(counter=1)
    return instance


def generate_form_errors_new(args, formset=False):
    i = 1
    message = ""
    if not formset:
        for field in args:
            if field.errors:
                message += "\n"
                message += field.label + " : "
                message += str(field.errors)

        for err in args.non_field_errors():
            message += str(err)
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += "\n"
                    message += field.label + " : "
                    message += str(field.errors)
            for err in form.non_field_errors():
                message += str(err)

    message = message.replace("<li>", "")
    message = message.replace("</li>", "")
    message = message.replace('<ul class="errorlist">', "")
    message = message.replace("</ul>", "")
    return message


def is_password_expired(StartTime):
    check_time = time.time()-float(StartTime)
    is_expired = False
    print('action ! -> time : {:.1f}s'.format(time.time()-float(StartTime)))
    if check_time > float(600):
        print(time.time()-float(StartTime))
        is_expired = True

    return is_expired
