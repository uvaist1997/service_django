from main.functions import get_current_role
# from web.models import Cart
from django.contrib.auth.models import User
from web import models as web_model


def main_context(request):
    current_role = get_current_role(request)
    user_type = 'User'
    current_user = None
    context_company_instance = None
    context_user_instance = None

    if current_role == 'superadmin':
        user_type = 'Admin User'
    elif current_role == 'vendor_user':
        user_type = 'Vendor User'
    elif current_role == 'customer_user':
        user_type = 'Customer User'

    if request.user.is_authenticated:
        current_user = request.user
        if request.user.is_superuser:
            context_company_instance = web_model.Companies.objects.filter()
            context_user_instance = User.objects.filter(is_superuser=False)
            print(context_user_instance,"LOOOOOOOOO")


    return {
        'context_company_instance' : context_company_instance,
        'context_user_instance' : context_user_instance,
        'current_user' : current_user

    }
