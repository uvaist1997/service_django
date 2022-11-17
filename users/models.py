from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User
from main.models import BaseModel
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MinValueValidator
from decimal import Decimal

# class CustomUser(AbstractUser):
#     email = models.EmailField(_('email address'), unique=True)
# # business type
#     class Meta:
#         db_table = 'users'
#         verbose_name = ('users')
#         verbose_name_plural = ('users')

#     def __unicode__(self):
#         return self.email


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'user_details'
        verbose_name = ('user_details')
        verbose_name_plural = ('user_details')

    def __unicode__(self):
        return self.user.username


class UserDeviceDetails(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    Device_Code = models.CharField(max_length=50)
    Application_Version = models.CharField(max_length=50)
    Device_Name = models.CharField(max_length=50)
    VanId = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_device_details'
        verbose_name = ('user_device_details')
        verbose_name_plural = ('user_device_details')

    def __unicode__(self):
        return self.Device_Code


class ActivityLog(models.Model):
    CompanyId = models.CharField(max_length=200)
    log_type = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    message = models.CharField(max_length=512)
    description = models.CharField(max_length=512, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'activity_log'
        verbose_name = ('activity_log')
        verbose_name_plural = ('activity_log')

    def __unicode__(self):
        return self.message


class SoftwareVersion(BaseModel):
    CurrentVersion = models.CharField(max_length=50)
    MinimumVersion = models.CharField(max_length=200)

    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'software_version'
        verbose_name = ('software_version')
        verbose_name_plural = ('software_version')

    def __unicode__(self):
        return self.CurrentVersion


class BusinessType(BaseModel):
    # ID = models.BigIntegerField(blank=True,null=True)
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    # CreatedUserID = models.ForeignKey(User, default=1,related_name="created", verbose_name="Category", on_delete=models.SET_DEFAULT)
    # CreatedDate = models.DateTimeField(blank=True,null=True)
    # UpdatedUserID = models.ForeignKey(User, default=1,related_name="updated", verbose_name="Categoryupdated", on_delete=models.SET_DEFAULT)
    # UpdatedDate = models.DateTimeField(blank=True,null=True)
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'business_types'
        verbose_name = ('business_type')
        verbose_name_plural = ('business_type')

    def __unicode__(self):
        return self.Name


class BusinessTypeLog(BaseModel):
    BusinessTypeid = models.BigIntegerField(blank=True, null=True)
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'business_type_logs'
        verbose_name = ('business_type_log')
        verbose_name_plural = ('business_type_logs')

    def __unicode__(self):
        return self.Name


# software plan


class SoftwarePlan(BaseModel):
    product = models.ForeignKey(
        'users.Product', related_name="product", on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'software_plans'
        verbose_name = ('software_plan')
        verbose_name_plural = ('software_plans')

    def __str__(self):
        return self.Name


class SoftwarePlanLog(BaseModel):
    product = models.ForeignKey(
        'users.Product', related_name="product_log", on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)

    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'software_plans_log'
        verbose_name = ('software_plan_log')
        verbose_name_plural = ('software_plans_log')

    def __unicode__(self):
        return self.Name


# products


class Product(BaseModel):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'products'
        verbose_name = ('product')
        verbose_name_plural = ('products')

    def __str__(self):
        return self.Name


class ProductLog(BaseModel):
    Productid = models.BigIntegerField(blank=True, null=True)
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'product_logs'
        verbose_name = ('product_log')
        verbose_name_plural = ('product_logs')

    def __unicode__(self):
        return self.Name


# services


class Service(BaseModel):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)

    Action = models.CharField(max_length=50)
    Price = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'services'
        verbose_name = ('service')
        verbose_name_plural = ('services')

    def __unicode__(self):
        return self.Name


class ServiceLog(BaseModel):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)
    Price = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'service_logs'
        verbose_name = ('service_log')
        verbose_name_plural = ('service_logs')

    def __unicode__(self):
        return self.Name


# currency


class Currency(BaseModel):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'currency'
        verbose_name = ('currency')
        verbose_name_plural = ('currency')

    def __unicode__(self):
        return self.Name


class CurrencyLog(BaseModel):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'currency_log'
        verbose_name = ('currency_logs')
        verbose_name_plural = ('currency_log')

    def __unicode__(self):
        return self.ID


# period


class Period(BaseModel):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Action = models.CharField(max_length=50)
    NoOfDays = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'periods'
        verbose_name = ('period')
        verbose_name_plural = ('periods')

    def __str__(self):
        return self.Name


class PeriodLog(BaseModel):
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)

    Action = models.CharField(max_length=50)
    NoOfDays = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'period_logs'
        verbose_name = ('period_log')
        verbose_name_plural = ('period_logs')

    def __str__(self):
        return self.Name


class EInvoice(BaseModel):
    CompanyID = models.ForeignKey(
        'web.Companies', on_delete=models.CASCADE, blank=True, null=True)
    InvoiceID = models.CharField(max_length=128)
    TransactionDate = models.DateTimeField()
    VoucherNo = models.CharField(max_length=128)
    VoucherType = models.CharField(max_length=128)
    TaxAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    GrandTotal = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'e_invoice'
        verbose_name = ('e_invoice')

    def __unicode__(self):
        return self.InvoiceID
