from web.models import AccountGroup
from django.db.models import Max
import string
import random


def generate_form_errors(args, formset=False):
    message = ''
    if not formset:
        for field in args:
            if field.errors:
                message += field.errors
        for err in args.non_field_errors():
            message += str(err)

    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += field.errors
            for err in form.non_field_errors():
                message += str(err)
    return message


def get_auto_ID(model):
    ID = 1
    if model.objects.filter().exists():
        latest_autoId = model.objects.filter().aggregate(Max('ID'))
        ID_r = latest_autoId.get('ID__max', 0)
        ID = ID_r + 1
    return ID


def get_auto_id(model):
    auto_id = 1
    latest_auto_id = model.objects.all().order_by("-date_added")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def generate_random_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    # length of password from the user
    length = int(6)

    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

        # shuffling the resultant password
        random.shuffle(password)

        # converting the list to string
        # printing the list
        print("".join(password))

    return "".join(password)
