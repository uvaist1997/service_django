from web.functions import generate_random_password
from web.models import VanPassword


def get_van_password(van):
    password = generate_random_password()
    if VanPassword.objects.filter(vansettings=van, password=password):
        password = generate_random_password()
    return password
