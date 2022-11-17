from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
import os
import uuid
from main.models import BaseModel
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.utils.timezone import now
import datetime
from django.contrib.auth.models import User
from web import models as web_model
from users import models as user_model
# from versatileimagefield.fields import VersatileImageField


AC_CHOICES = (
    ('credit', 'Credit'),
    ('debit', 'Debit'),
)


class Account(models.Model):
    AccountName = models.CharField(max_length=128)
    Description = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_account'
        verbose_name = ('account')

    def __str__(self):
        return self.AccountName


class DatabaseDetail(models.Model):
    # file = models.FileField(blank=True,null=True)
    file = models.FileField(upload_to='DB/', blank=False, null=True)
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    VanId = models.BigIntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'database_detail'
        verbose_name = ('database_detail')

    def __str__(self):
        return self.VanId


class AccountLog(models.Model):
    # tutorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    AccountName = models.CharField(max_length=128)
    Description = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_account_log'
        verbose_name = ('account_log')

    def __unicode__(self):
        return self.name


class AccountGroup(BaseModel):
    AccountGroupName = models.CharField(max_length=128)
    ParentGroup = models.ForeignKey(
        Account, default=1, verbose_name="ParentGroup", on_delete=models.SET_DEFAULT)
    Description = models.CharField(max_length=128)

    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_account_group'
        verbose_name = ('account_group')

    def __str__(self):
        return self.AccountGroupName


class AccountGroupLog(BaseModel):
    # TutorialCategoryorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    AccountGroupName = models.CharField(max_length=128)
    ParentGroup = models.ForeignKey(
        Account, default=1, verbose_name="ParentGroup", on_delete=models.SET_DEFAULT)
    Description = models.CharField(max_length=128)

    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_account_group_log'
        verbose_name = ('account_group_log')

    def __unicode__(self):
        return self.AccountGroupName


class AccountLedger(BaseModel):
    LedgerName = models.CharField(max_length=128)
    ParentGroup = models.ForeignKey(
        AccountGroup, default=1, verbose_name="ParentGroup", on_delete=models.SET_DEFAULT)
    OpeningBalanceType = models.CharField(choices=AC_CHOICES, max_length=128)
    OpeningBalanceAmount = models.CharField(max_length=128)
    Description = models.CharField(max_length=128)
    PlaceofSupply = models.CharField(max_length=128, blank=True, null=True)

    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_account_ledger'
        verbose_name = ('account_ledger')

    def __unicode__(self):
        return self.name


class AccountLedgerLog(BaseModel):
    LedgerName = models.CharField(max_length=128)
    ParentGroup = models.CharField(max_length=128)
    OpeningBalanceType = models.CharField(max_length=128)
    OpeningBalanceAmount = models.CharField(max_length=128)
    Description = models.CharField(max_length=128)
    PlaceofSupply = models.CharField(max_length=128, blank=True, null=True)

    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_account_ledger_log'
        verbose_name = ('account_ledger_log')

    def __unicode__(self):
        return self.LedgerName


class Customer(BaseModel):
    UserName = models.CharField(max_length=128)
    FirstName = models.CharField(max_length=128)
    LastName = models.CharField(max_length=128)
    Email = models.EmailField(max_length=128)
    Country = models.CharField(max_length=128)
    State = models.CharField(max_length=128)
    CompanyName = models.CharField(max_length=128)
    PhoneNumber = models.BigIntegerField(blank=True, null=True)
    Description = models.CharField(max_length=128)

    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_customer'
        verbose_name = ('customer')

    def __str__(self):
        return self.name


class CustomerLog(BaseModel):
    FirstName = models.CharField(max_length=128)
    LastName = models.CharField(max_length=128)
    UserName = models.CharField(max_length=128)
    Country = models.CharField(max_length=128)
    State = models.CharField(max_length=128)
    PhoneNumber = models.BigIntegerField(blank=True, null=True)

    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_customer_log'
        verbose_name = ('customer_log')

    def __unicode__(self):
        return self.FirstName


class Companies(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_type = models.ForeignKey(
        'users.BusinessType', related_name="business_type", on_delete=models.CASCADE)
    CompanyName = models.CharField(max_length=128)
    Country = models.CharField(max_length=128)
    State = models.CharField(max_length=128)
    OfficePhoneNumber = models.BigIntegerField(blank=True, null=True)
    Email = models.EmailField(max_length=128)
    Action = models.CharField(max_length=128)

    logo = models.ImageField(blank=True, null=True)
    register_name = models.CharField(max_length=128, blank=True, null=True)
    tagline = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    trn_vat_gst = models.CharField(max_length=128, blank=True, null=True)
    cr_cin_number = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'web_companies'
        verbose_name = ('companies')

    def __str__(self):
        return str(self.CompanyName)


class CompaniesLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_type = models.ForeignKey(
        'users.BusinessType', related_name="business_type_log", on_delete=models.CASCADE)
    # user = models.OneToOneField("masters.User", related_name='logged_in_user',on_delete=models.CASCADE)
    Companyid = models.BigIntegerField(blank=True, null=True)
    CompanyName = models.CharField(max_length=128)
    Country = models.CharField(max_length=128)
    State = models.CharField(max_length=128)
    OfficePhoneNumber = models.BigIntegerField(blank=True, null=True)
    Email = models.EmailField(max_length=128)

    Action = models.CharField(max_length=128)

    logo = models.ImageField(blank=True, null=True)
    register_name = models.CharField(max_length=128, blank=True, null=True)
    tagline = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    trn_vat_gst = models.CharField(max_length=128, blank=True, null=True)
    cr_cin_number = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'web_companies_log'
        verbose_name = ('companies_log')

    def __str__(self):
        return str(self.CompanyName)


TRIAL_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)


class CompanyProduct(BaseModel):
    # CompanyId = models.CharField(max_length=128)
    # ProductId = models.CharField(max_length=128)
    ProductId = models.ForeignKey('users.Product', on_delete=models.CASCADE)
    CompanyId = models.ForeignKey('web.Companies', on_delete=models.CASCADE)
    No_ofDevice = models.BigIntegerField(blank=True, null=True)
    IsTrialVersion = models.BooleanField(default=False)
    Action = models.CharField(max_length=128)
    software_plan = models.ForeignKey(
        'users.SoftwarePlan', related_name="software_plan", on_delete=models.CASCADE, blank=True, null=True)

    ProductExpiryDate = models.DateTimeField(blank=True, null=True)
    AMCActive = models.DateTimeField(blank=True, null=True)
    AMCExpiry = models.DateTimeField(blank=True, null=True)
    service_date = models.DateTimeField(blank=True, null=True)

    service = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = 'web_company_product'
        verbose_name = ('company_product')

    def __str__(self):
        return str(self.ProductId.Name)


class CompanyProductLog(BaseModel):
    CompanyProductId = models.BigIntegerField(blank=True, null=True)
    CompanyId = models.ForeignKey('web.Companies', on_delete=models.CASCADE)

    ProductId = models.ForeignKey('users.Product', on_delete=models.CASCADE)
    No_ofDevice = models.BigIntegerField(blank=True, null=True)
    ProductExpiryDate = models.DateTimeField(blank=True, null=True)
    AMCActive = models.DateTimeField(blank=True, null=True)
    AMCExpiry = models.DateTimeField(blank=True, null=True)
    IsTrialVersion = models.BooleanField(default=False)
    Action = models.CharField(max_length=128)
    software_plan = models.ForeignKey(
        'users.SoftwarePlan', related_name="software_plan_log", on_delete=models.CASCADE, blank=True, null=True)

    service_date = models.DateTimeField(blank=True, null=True)
    service = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = 'web_companyproductlog'
        verbose_name = ('companyproductlog')

    def __unicode__(self):
        return self.CompanyProductId


TYPE_CHOICES = (
    ('client', 'Client'),
    ('server', 'Server'),
)


class CompanyDevices(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    DeviceName = models.CharField(max_length=128)
    DeviceCode = models.CharField(max_length=128)

    IsTrialVersion = models.BooleanField(default=False)
    ProductExpiryDate = models.DateTimeField(blank=True, null=True)

    Type = models.CharField(choices=TYPE_CHOICES, max_length=128)
    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_company_device'
        verbose_name = ('companydevice')

    def __str__(self):
        return str(self.DeviceName)


class CompanyDevicesLog(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    DeviceName = models.CharField(max_length=128)
    DeviceCode = models.CharField(max_length=128)

    IsTrialVersion = models.BooleanField(default=False)
    ProductExpiryDate = models.DateTimeField(blank=True, null=True)

    Type = models.CharField(max_length=128)
    Action = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_company_devicelog'
        verbose_name = ('company_devicelog')

    def __unicode__(self):
        return self.name


# Register
class Register(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    PhoneNumber = models.CharField(max_length=128)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey(
        "auth.User", blank=True, related_name="creator_%(class)s_objects", on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User", blank=True, null=True,
                                related_name="updater_%(class)s_objects", on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'web_register'
        verbose_name = ('register')

    def __unicode__(self):
        return self.user


class SaleProduct(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    ProductId = models.BigIntegerField()
    BranchId = models.BigIntegerField()
    Productcode = models.CharField(max_length=128)
    Productname = models.CharField(max_length=128)
    Displayname = models.CharField(max_length=128, null=True, blank=True)
    Description = models.CharField(max_length=600, null=True, blank=True)
    minimumSalesPrice = models.DecimalField(
        default=0, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])

    VatId = models.BigIntegerField()
    GstId = models.BigIntegerField()
    Tax1Id = models.BigIntegerField()
    Tax2Id = models.BigIntegerField()
    Tax3Id = models.BigIntegerField()
    SyncDate = models.DateTimeField()

    class Meta:
        db_table = 'web_sale_product'
        verbose_name = ('sale_product')

    def __unicode__(self):
        return self.Productid


class SalePrice(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    ProductId = models.BigIntegerField()
    PriceListId = models.BigIntegerField()
    BranchId = models.BigIntegerField()
    UnitName = models.CharField(max_length=128)
    PurchasePrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    SalePrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SalePrice1 = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    SalePrice2 = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    SalePrice3 = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    MultiFactor = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    AutoBarcode = models.BigIntegerField()
    Barcode = models.CharField(max_length=128, blank=True, null=True)
    SyncDate = models.DateTimeField()
    IsDefault = models.BooleanField(default=False)

    class Meta:
        db_table = 'web_sale_price'
        verbose_name = ('sale_price')

    def __unicode__(self):
        return self.Productid


class SaleProductPrice(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    SaleProductId = models.ForeignKey(
        'web.SaleProduct', on_delete=models.CASCADE, blank=True, null=True)
    ProductId = models.BigIntegerField()
    PriceListId = models.BigIntegerField()
    BranchId = models.BigIntegerField()
    UnitName = models.CharField(max_length=128)
    PurchasePrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    SalePrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SalePrice1 = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    SalePrice2 = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    SalePrice3 = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    MultiFactor = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    AutoBarcode = models.BigIntegerField()
    Barcode = models.CharField(max_length=128, blank=True, null=True)
    SyncDate = models.DateTimeField()
    IsDefault = models.BooleanField(default=False)

    class Meta:
        db_table = 'web_sale_product_price'
        verbose_name = ('sale_product_price')

    def __unicode__(self):
        return self.Productid


class SaleAccountLedger(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    LedgerId = models.BigIntegerField()
    PartyName = models.CharField(max_length=128)
    LedgerCode = models.CharField(max_length=128, blank=True, null=True)

    RouteId = models.BigIntegerField()
    PriceCategoryID = models.BigIntegerField()
    GroupId = models.BigIntegerField()
    Credit_Limit = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    Balance = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])

    DisplayName = models.CharField(max_length=128, blank=True, null=True)
    VatNum = models.CharField(max_length=128, blank=True, null=True)
    GstNum = models.CharField(max_length=128, blank=True, null=True)
    Tax1Number = models.CharField(max_length=128, blank=True, null=True)
    Tax2Number = models.CharField(max_length=128, blank=True, null=True)
    Tax3Number = models.CharField(max_length=128, blank=True, null=True)
    BillwiseApplicable = models.BooleanField(default=False)
    CrNum = models.CharField(max_length=128, blank=True, null=True)
    PlaceofSupply = models.CharField(max_length=128, blank=True, null=True)

    Address1 = models.CharField(max_length=128, blank=True, null=True)
    City = models.CharField(max_length=128, blank=True, null=True)
    State = models.CharField(max_length=128, blank=True, null=True)
    Country = models.CharField(max_length=128, blank=True, null=True)
    BuildingNumber = models.CharField(max_length=128, blank=True, null=True)
    District = models.CharField(max_length=128, blank=True, null=True)
    StreetName = models.CharField(max_length=128, blank=True, null=True)
    AdditionalNo = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'web_sale_account_ledger'
        verbose_name = ('sale_account_ledger')

    def __unicode__(self):
        return self.PartyName


class WarehouseStock(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    ProductId = models.BigIntegerField()
    PriceListId = models.BigIntegerField()
    WarehouseId = models.BigIntegerField()
    Stock = models.DecimalField(default=0, decimal_places=8, max_digits=20, validators=[
                                MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'web_warehouse_stock'
        verbose_name = ('warehouse_stock')

    def __unicode__(self):
        return self.WarehouseId


class ExpenseLedger(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    LedgerId = models.BigIntegerField()
    VanId = models.BigIntegerField()
    LedgerName = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_expense_ledger'
        verbose_name = ('expense_ledger')

    def __unicode__(self):
        return self.LedgerId


class LastSalesPrice(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    LedgerId = models.BigIntegerField()
    SalePrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    PriceListId = models.BigIntegerField()
    Van_ID = models.BigIntegerField()

    class Meta:
        db_table = 'web_last_sale_price'
        verbose_name = ('last_sale_price')

    def __unicode__(self):
        return self.SalePrice


class SaleRoute(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    RouteId = models.BigIntegerField()
    RouteName = models.CharField(max_length=128)

    class Meta:
        db_table = 'web_sale_route'
        verbose_name = ('sale_route')

    def __unicode__(self):
        return self.RouteId


class TransactionType(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    TransactionTypeId = models.BigIntegerField()
    MasterTypeId = models.BigIntegerField()
    TransactionTypeName = models.CharField(max_length=128)
    SyncDate = models.DateTimeField()

    class Meta:
        db_table = 'web_transaction_type'
        verbose_name = ('transaction_type')

    def __unicode__(self):
        return self.TransactionTypeId


class VanRoute(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE, blank=True, null=True)
    RouteId = models.BigIntegerField()
    RouteName = models.CharField(max_length=128)
    VanId = models.BigIntegerField()

    class Meta:
        db_table = 'web_van_route'
        verbose_name = ('van_route')

    def __unicode__(self):
        return self.RouteId


# master

class SaleMaster(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    GUID = models.CharField(
        max_length=128, blank=True, null=True)
    MasterId = models.BigIntegerField()
    TransactionTypeId = models.BigIntegerField()
    BranchId = models.BigIntegerField()
    salesOrderMasterID = models.CharField(
        max_length=128, blank=True, null=True)

    LedgerId = models.BigIntegerField()
    PriceCategoryId = models.BigIntegerField()
    SaleAccount = models.BigIntegerField()
    TaxId = models.BigIntegerField()
    TaxType = models.CharField(max_length=128)

    check_date = models.CharField(max_length=128, blank=True, null=True)
    Date = models.DateField(blank=True, null=True)
    TotalGrossAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    AddlDiscPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])
    AddlDiscAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    BillDiscPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])
    BillDiscAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    TotalDiscount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    VATAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    CGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    IGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX1Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX2Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX3Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TotalTax = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    NetTotal = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    AdditionalCost = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])
    GrandTotal = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    RoundOff = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    CashReceived = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    CashAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    BankAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    Balance = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    VanId = models.BigIntegerField()
    TransactionId = models.BigIntegerField()
    status = models.BooleanField(default=False)

    Address1 = models.CharField(max_length=128, blank=True, null=True)
    Address2 = models.CharField(max_length=128, blank=True, null=True)
    Notes = models.CharField(max_length=128, blank=True, null=True)
    CardNumber = models.CharField(max_length=128, blank=True, null=True)
    CustomerName = models.CharField(max_length=128, blank=True, null=True)

    PlaceofSupply = models.CharField(max_length=128, blank=True, null=True)

    Treatment = models.CharField(max_length=128, blank=True, null=True)
    TaxableAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    NonTaxableAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        db_table = 'web_sales_masters'
        verbose_name = ('sales_master')
        ordering = ('Date',)
        verbose_name_plural = ('sales_masters')

    def __unicode__(self):
        return self.Voucher_No


class SaleDetails(models.Model):
    MasterId = models.BigIntegerField()
    SaleId = models.ForeignKey(SaleMaster, related_name="sale_master",
                               verbose_name="sale_master", on_delete=models.CASCADE)
    # TransactionId = models.BigIntegerField()
    ProductId = models.BigIntegerField()
    Qty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                              MinValueValidator(Decimal('0.00'))])
    FreeQty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    UnitPrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    InclusivePrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])

    PriceListId = models.BigIntegerField()

    DiscountPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    DiscountAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])
    AddlDiscPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])
    AddlDiscAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    GrossAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    TaxableAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    VATPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    VATAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    SGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    CGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    CGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    IGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    IGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX1Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX1Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX2Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX2Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX3Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX3Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    NetAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    CostPerPrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    OrderStatus = models.BooleanField(default=False)
    StockOrderNo = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'web_sales_details'
        verbose_name = ('sales_detail')
        verbose_name_plural = ('sales_details')

    def __unicode__(self):
        return self.SaleId


class SaleReturnMaster(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    GUID = models.CharField(
        max_length=128, blank=True, null=True)
    TransactionId = models.BigIntegerField()
    Date = models.DateField(blank=True, null=True)
    RefferenceBillNo = models.CharField(max_length=128)
    RefferenceBillDate = models.DateField(auto_now_add=True)
    LedgerId = models.BigIntegerField()
    PriceCategoryId = models.BigIntegerField()
    EmployeeId = models.BigIntegerField()
    SaleAccount = models.BigIntegerField()
    TaxId = models.BigIntegerField()
    TaxType = models.CharField(max_length=128, blank=True, null=True)
    VATAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    CGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    IGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX1Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX2Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX3Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TotalTax = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    NetTotal = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    AdditionalCost = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])
    TotalGrossAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    AddlDiscPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])
    AddlDiscAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    TotalDiscount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    BillDiscPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])
    BillDiscAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    GrandTotal = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    RoundOff = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    VanId = models.BigIntegerField()
    status = models.BooleanField(default=False)

    Address1 = models.CharField(max_length=128, blank=True, null=True)
    Address2 = models.CharField(max_length=128, blank=True, null=True)
    Notes = models.CharField(max_length=128, blank=True, null=True)
    CustomerName = models.CharField(max_length=128, blank=True, null=True)

    Treatment = models.CharField(max_length=128, blank=True, null=True)
    TaxableAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    NonTaxableAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        db_table = 'web_sales_return_masters'
        verbose_name = ('sales_return_master')
        ordering = ('Date',)
        verbose_name_plural = ('sales_return_masters')

    def __unicode__(self):
        return self.Voucher_No


class SaleReturnDetails(models.Model):
    SaleReturnMasterId = models.ForeignKey(
        SaleReturnMaster, related_name="sale_return_master", verbose_name="sale_return_master", on_delete=models.CASCADE)
    ProductId = models.BigIntegerField()
    Qty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                              MinValueValidator(Decimal('0.00'))])
    FreeQty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    UnitPrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    RateWithTax = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    CostPerPrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    PriceListId = models.BigIntegerField()
    DiscountAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])
    DiscountPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    GrossAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    AddlDiscPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])
    AddlDiscAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    TaxableAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    VATPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    VATAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    SGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    CGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    CGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    IGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    IGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX1Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX1Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX2Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX2Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX3Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX3Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    NetAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])

    # TransactionId = models.BigIntegerField()
    # InclusivePrice = models.DecimalField(default=0,decimal_places=2, max_digits=20,validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'web_sales_return_details'
        verbose_name = ('sales_return_detail')
        verbose_name_plural = ('sales_return_details')

    def __unicode__(self):
        return self.SaleReturnMasterId


class SalesReturnBillWiseDetails(models.Model):
    SaleReturnMasterId = models.ForeignKey(
        SaleReturnMaster, related_name="sale_return_master1", verbose_name="sale_return_master1", on_delete=models.CASCADE)
    Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                 MinValueValidator(Decimal('0.00'))])
    VoucherNumber = models.CharField(max_length=128)
    VoucherType = models.CharField(max_length=128)
    Due_Date = models.DateField(blank=True, null=True)
    Date = models.DateField(blank=True, null=True)
    DueAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    Invoice_Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'return_billwise_details'
        verbose_name = ('return_billwise_detail')
        verbose_name_plural = ('return_billwise_details')

    def __unicode__(self):
        return self.SaleReturnMasterId


class SaleOrder(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    TransactionId = models.BigIntegerField()
    Date = models.DateField(blank=True, null=True)
    LedgerId = models.BigIntegerField()
    PriceCategoryId = models.BigIntegerField()
    SaleAccount = models.BigIntegerField()
    TaxId = models.BigIntegerField()
    VanId = models.BigIntegerField()
    TaxType = models.CharField(max_length=128)
    VATAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    CGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    IGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX1Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX2Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX3Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TotalTax = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    NetTotal = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    BillDiscount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    GrandTotal = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    RoundOff = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    IsInvoiced = models.CharField(max_length=128)
    status = models.BooleanField(default=False)

    Address1 = models.CharField(max_length=128, blank=True, null=True)
    Address2 = models.CharField(max_length=128, blank=True, null=True)
    Notes = models.CharField(max_length=128, blank=True, null=True)
    CustomerName = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'web_sales_order'
        verbose_name = ('sales_order')
        ordering = ('Date',)

        verbose_name_plural = ('sales_orders')

    def __unicode__(self):
        return self.CompanyProductId


class SaleOrderDetails(models.Model):
    stockOrderMasterID = models.CharField(
        max_length=128, blank=True, null=True)
    SaleOrderId = models.ForeignKey(SaleOrder, related_name="sale_oredr_master",
                                    verbose_name="sale_oredr_master", on_delete=models.CASCADE)
    ProductId = models.BigIntegerField()
    Qty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                              MinValueValidator(Decimal('0.00'))])
    FreeQty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    UnitPrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    RateWithTax = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    CostPerPrice = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    PriceListId = models.BigIntegerField()
    DiscountAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])
    DiscountPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                       MinValueValidator(Decimal('0.00'))])
    GrossAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    AddlDiscPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])
    AddlDiscAmt = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    TaxableAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                        MinValueValidator(Decimal('0.00'))])
    VATPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                  MinValueValidator(Decimal('0.00'))])
    VATAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    SGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    SGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    CGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    CGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    IGSTPerc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    IGSTAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX1Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX1Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX2Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX2Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    TAX3Perc = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    TAX3Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    NetAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'web_sales_order_details'
        verbose_name = ('sales_order_detail')
        verbose_name_plural = ('sales_order_details')

    def __unicode__(self):
        return self.SaleOrderId


class Reciept(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    GUID = models.CharField(
        max_length=128, blank=True, null=True)
    VoucherType = models.CharField(max_length=128)
    TransactionId = models.BigIntegerField()
    CashOrBankId = models.BigIntegerField()
    Van_ID = models.BigIntegerField()
    Date = models.CharField(max_length=128, blank=True, null=True)
    PaymentGateway = models.BigIntegerField(blank=True, null=True)
    CashAccountID = models.BigIntegerField(blank=True, null=True)
    RefferenceNo = models.CharField(max_length=128, blank=True, null=True)
    CardNetwork = models.BigIntegerField(blank=True, null=True)
    PaymentStatus = models.BigIntegerField(blank=True, null=True)

    DueDate = models.CharField(max_length=128, blank=True, null=True)
    LedgerId = models.BigIntegerField()
    Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                 MinValueValidator(Decimal('0.00'))])
    Discount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])
    Advance_Payment = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                          MinValueValidator(Decimal('0.00'))])

    TotalAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    Balance = models.CharField(max_length=128)
    Narration = models.CharField(max_length=128)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'web_reciept'
        verbose_name = ('web_reciept')
        ordering = ('Date',)
        verbose_name_plural = ('web_reciepts')

    def __unicode__(self):
        return self.TransactionId


class RecieptDetail(models.Model):
    RecieptId = models.ForeignKey('web.Reciept', on_delete=models.CASCADE)
    TransactionId = models.BigIntegerField()
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                 MinValueValidator(Decimal('0.00'))])
    Due_Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    VoucherNumber = models.BigIntegerField()

    class Meta:
        db_table = 'web_reciept_details'
        verbose_name = ('web_reciept_detail')
        verbose_name_plural = ('web_reciept_details')

    def __unicode__(self):
        return self.TransactionId


# class Payment(BaseModel):
#     CompanyProductId = models.ForeignKey('web.CompanyProduct',on_delete=models.CASCADE)

#     VoucherType = models.CharField(max_length=128)
#     TransactionId = models.BigIntegerField()
#     CashOrBankId = models.BigIntegerField()
#     Date =models.DateTimeField(auto_now_add=True)

#     PaymentGateway = models.BigIntegerField(blank=True,null=True)
#     RefferenceNo = models.CharField(max_length=128,blank=True,null=True)
#     CardNetwork = models.BigIntegerField(blank=True,null=True)
#     PaymentStatus = models.BigIntegerField(blank=True,null=True)
#     DueDate =models.DateTimeField(auto_now_add=True)

#     LedgerId = models.BigIntegerField()
#     Amount = models.DecimalField(default=0,decimal_places=2, max_digits=20,validators=[MinValueValidator(Decimal('0.00'))])

#     Discount = models.DecimalField(default=0,decimal_places=2, max_digits=20,validators=[MinValueValidator(Decimal('0.00'))])
#     NetAmount = models.DecimalField(default=0,decimal_places=2, max_digits=20,validators=[MinValueValidator(Decimal('0.00'))])
#     Balance = models.CharField(max_length=128)
#     Narration = models.CharField(max_length=128)
#     status = models.BooleanField(default=False)

#     class Meta:
#         db_table = 'web_payment'
#         verbose_name = ('web_payment')
#         verbose_name_plural = ('web_payments')

#     def __unicode__(self):
#         return self.VoucherType


class Payment(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    GUID = models.CharField(
        max_length=128, blank=True, null=True)
    Date = models.DateField(blank=True, null=True)
    TotalAmount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    CashAccountId = models.BigIntegerField()
    TransactionId = models.BigIntegerField()
    Van_ID = models.BigIntegerField()
    Route_ID = models.BigIntegerField()

    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'web_payment'
        verbose_name = ('web_payment')
        ordering = ('Date',)
        verbose_name_plural = ('web_payments')

    def __unicode__(self):
        return self.CashAccountId


class PaymentDetail(models.Model):
    PaymentId = models.ForeignKey('web.Payment', on_delete=models.CASCADE)
    TransactionId = models.BigIntegerField()
    LedgerId = models.BigIntegerField()
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                 MinValueValidator(Decimal('0.00'))])
    notes = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'web_payment_details'
        verbose_name = ('web_payment_detail')
        verbose_name_plural = ('web_payment_details')

    def __unicode__(self):
        return self.TransactionId


class VanPassword(BaseModel):
    vansettings = models.ForeignKey(
        'web.VanSettings', on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    time = models.TimeField(blank=True, null=True)
    time_str = models.CharField(max_length=128, blank=True, null=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        db_table = 'van_settigns_passwords'
        verbose_name = ('van_settigns_password')
        verbose_name_plural = ('van_settigns_passwords')

    def __unicode__(self):
        return self.password


class VanSettings(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)

    VanSaleRoundoff = models.BigIntegerField(blank=True, null=True)
    UserID = models.BigIntegerField()
    UserName = models.CharField(max_length=128)
    CashAccountID = models.BigIntegerField()
    Allow_Receipt_Discount = models.BooleanField(default=False)
    # Allow_Receipt_Discount1 = models.BooleanField(default=False)
    BankAccountID = models.BigIntegerField()
    PriceCategoryID = models.BigIntegerField()
    sales_account = models.BigIntegerField()
    Device_Code = models.CharField(max_length=128)
    sales_return_account = models.BigIntegerField()

    VatSalesType = models.BigIntegerField()
    VanId = models.BigIntegerField()
    WarehouseId = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # userId = models.BigIntegerField()
    VanName = models.CharField(max_length=128, blank=True, null=True)
    VoucherPrefix = models.CharField(max_length=128, blank=True, null=True)
    Password = models.CharField(max_length=128, blank=True, null=True)
    CreditLimit = models.DecimalField(default=0,decimal_places=2, max_digits=20,validators=[MinValueValidator(Decimal('0.00'))])
    DiscountPercentPerBill = models.DecimalField(
        default=0, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    CashBalance = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    ShowNegativeStockItem = models.BooleanField(default=False)
    CanEditUnitPrice = models.BooleanField(default=False)
    AllowBillDiscount = models.BooleanField(default=False)
    Allow_Sales_Below_Min_Sales_Price = models.BooleanField(default=False)
    AllowNegativeStockSale = models.BooleanField(default=False)
    Allow_Sales_Below_Purchase_Price = models.BooleanField(default=False)
    AllowItemwiseDiscount = models.BooleanField(default=False)
    ShowSalesType = models.BooleanField(default=False)
    Allow_Cash_Sales = models.BooleanField(default=False)
    Show_Last_Sales_Price = models.BooleanField(default=False)
    Show_Inclusive_Field = models.BooleanField(default=False)

    Show_Cost_In_Stock_Order = models.BooleanField(default=False)
    StockOrderWarehouseFromId = models.BigIntegerField()

    Sales_Invoice_Edit = models.BooleanField(default=False)
    Sales_price_lessthan_Purchase_price = models.CharField(
        max_length=128, blank=True, null=True)
    PriceDecimalPoint = models.BigIntegerField(blank=True, null=True)
    QtyDecimalPoint = models.BigIntegerField(blank=True, null=True)

    EditPaymentinsalesbeforeSync = models.BooleanField(default=False)
    EditExpensebeforeSync = models.BooleanField(default=False)
    EditReceiptbeforeSync = models.BooleanField(default=False)

    EditsalesReturnbeforeSync = models.BooleanField(default=False)
    EditsalesOrderbeforeSync = models.BooleanField(default=False)

    CountryId = models.BigIntegerField(blank=True, null=True)
    PlaceofSupply = models.CharField(max_length=128, blank=True, null=True)

    EnablePortForward = models.BooleanField(default=False)
    IPAddress = models.CharField(max_length=128, blank=True, null=True)
    Port = models.CharField(max_length=128, blank=True, null=True)
    DatabaseName = models.CharField(max_length=128, blank=True, null=True)
    DBUserName = models.CharField(max_length=128, blank=True, null=True)
    DBPassword = models.CharField(max_length=128, blank=True, null=True)
    ServerName = models.CharField(max_length=128, blank=True, null=True)
    BranchID = models.BigIntegerField(blank=True, null=True)
    Enable_ZATCA_Rules = models.BooleanField(default=False)
    EmployeeID = models.BigIntegerField(blank=True, null=True)
 
    class Meta:
        db_table = 'web_van_settings'
        verbose_name = ('web_van_settings')
        verbose_name_plural = ('web_van_settings')

    def __unicode__(self):
        return self.VoucherType


class TaxCategory(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    TaxId = models.BigIntegerField()
    BranchId = models.BigIntegerField()
    TaxName = models.CharField(max_length=128)
    TaxType = models.CharField(max_length=128)
    PurchaseTax = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    SalesTax = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                   MinValueValidator(Decimal('0.00'))])

    Inclusive = models.BooleanField(default=False)
    SyncDate = models.DateTimeField()

    class Meta:
        db_table = 'web_tax_category'
        verbose_name = ('tax_category')

    def __unicode__(self):
        return self.TaxId


class BillWise(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    CustomerID = models.BigIntegerField()
    TransactionID = models.BigIntegerField()
    VoucherType = models.CharField(max_length=128)
    VoucherNo = models.BigIntegerField()
    Date = models.CharField(max_length=128, blank=True, null=True)
    Due_Date = models.CharField(max_length=128, blank=True, null=True)
    Invoice_Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                         MinValueValidator(Decimal('0.00'))])
    Due_Amount = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    VanId = models.BigIntegerField()

    class Meta:
        db_table = 'web_bill_wise'
        verbose_name = ('bill_wise')

    def __unicode__(self):
        return self.TransactionID


class StockOrder(BaseModel):
    CompanyProductId = models.ForeignKey(
        'web.CompanyProduct', on_delete=models.CASCADE)
    GUID = models.CharField(
        max_length=128, blank=True, null=True)
    TransactionID = models.BigIntegerField()
    WarehouseTo_id = models.BigIntegerField()
    WarehouseFrom_id = models.BigIntegerField()
    VanID = models.BigIntegerField()
    Date = models.DateField(blank=True, null=True)
    Notes = models.CharField(max_length=128)
    Total_qty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                    MinValueValidator(Decimal('0.00'))])
    Total_cost = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                                     MinValueValidator(Decimal('0.00'))])
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'web_stock_order'
        verbose_name = ('stock_order')

    def __unicode__(self):
        return self.CompanyProductId


class StockOrderDetail(models.Model):
    StockOrderId = models.ForeignKey(
        'web.StockOrder', on_delete=models.CASCADE)
    ProductId = models.BigIntegerField()
    PricelistId = models.BigIntegerField()

    qty = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                              MinValueValidator(Decimal('0.00'))])
    cost = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[
                               MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'web_stock_order_details'
        verbose_name = ('web_stock_order_detail')
        verbose_name_plural = ('web_stock_order_details')

    def __unicode__(self):
        return self.StockOrderId


# Version
class Version(models.Model):
    version = models.CharField(max_length=128)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'build_version'
        verbose_name = ('build_version')

    def __unicode__(self):
        return self.version
