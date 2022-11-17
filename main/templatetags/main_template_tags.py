from web.models import SaleProduct, CompanyDevices
from users.models import UserDetails
from django.template.defaultfilters import stringfilter
from django.template import Library
from django.contrib.auth.models import User
register = Library()


@register.filter
def check_default(value):
    result = value
    if value == "default":
        result = "-"
    return result


@register.filter
@stringfilter
def underscore_smallletter(value):
    value = value.replace(" ", "_")
    return value


@register.filter
def to_fixed_two(value):
    return "{:10.2f}".format(value)


@register.filter
def tax_devide(value):
    return value/2


@register.filter
def to_positive(value):
    return (value * -1)


@register.filter
def warehouse_product_name(instance):
    if SaleProduct.objects.filter(ProductId=instance.ProductId, CompanyProductId=instance.CompanyProductId).exists():
        product_name = SaleProduct.objects.get(
            ProductId=instance.ProductId, CompanyProductId=instance.CompanyProductId)
        print(product_name, "WWWWWWWWWWW")
        return product_name.Productname
    else:
        return ''


@register.filter
def IsTrialVersion_True(instance):
    count = len(CompanyDevices.objects.filter(
        CompanyProductId__CompanyId=instance, IsTrialVersion=True))
    return count


@register.filter
def IsTrialVersion_False(instance):
    count = len(CompanyDevices.objects.filter(
        CompanyProductId__CompanyId=instance, IsTrialVersion=False))
    return count


@register.filter
def get_user_password(user):
    if UserDetails.objects.filter(user=user).exists():
        password = UserDetails.objects.get(user=user).password
        print(password, "WWWWWWWWWWW")
        return password
    else:
        return ''
