# from users.models import CreateUser,CreateSoft,CreateProduct,CreateService,CreateCurrency,CreatePeriod
from django.db.models import Max

# def generate_form_errors(args,formset=False):
#     message = ''
#     if not formset:
#         for field in args:
#             if field.errors:
#                 message += field.errors
#         for err in args.non_field_errors():
#             message += str(err)

#     elif formset:
#         for form in args:
#             for field in form:
#                 if field.errors:
#                     message += field.errors
#             for err in form.non_field_errors():
#                 message +=str(err)
#     return message


def generate_form_errors(args, formset=False):
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



def get_auto_ID(model):
    ID = 1
    if model.objects.filter().exists():
        latest_autoId = model.objects.filter().aggregate(Max('ID'))
        ID_r = latest_autoId.get('ID__max',0)
        ID = ID_r + 1
    return ID


def get_auto_id(model):
    id = 1
    if model.objects.filter().exists():
        latest_autoid = model.objects.filter().aggregate(Max('id'))
        id_r = latest_autoid.get('id__max',0)
        id = id_r + 1
    return id
