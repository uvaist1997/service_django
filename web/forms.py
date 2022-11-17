from django import forms
from django.forms.widgets import TextInput, Textarea, FileInput, Select, RadioSelect, DateInput, CheckboxInput, EmailInput
from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm
from django import forms
from django.contrib.auth.models import User
from web import models as web_models


class VersionForm(forms.ModelForm):

    class Meta:
        model = web_models.Version
        fields = ['version','status']
        widgets = {
            'version': TextInput(attrs={'class' : 'required form-control w-50 mb-3', 'placeholder': 'Version'}),
            'status': CheckboxInput(attrs={'class' :'form', 'placeholder' : _('Status')}),

        }


class AccountGroupForm(forms.ModelForm):

    class Meta:
        model = web_models.AccountGroup
        exclude = ['ID','CreatedDate','UpdatedDate','Action','CreatedUserID','UpdatedUserID',]
        widgets = {
            'AccountGroupName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('AccountGroupName')}),
            'ParentGroup': Select(attrs={'class' :'required form-control form', 'placeholder' : _('ParentGroup')}),
            'Description': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Description')}),
            # 'ID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('ID')}),
            # 'CreatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('CreatedUserID')}),
            'CreatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),
            # 'UpdatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('UpdatedUserID')}),
            'UpdatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),

            
        }



class AccountLedgerForm(forms.ModelForm):

    class Meta:
        model = web_models.AccountLedger
        exclude = ['ID','CreatedDate','UpdatedDate','Action','CreatedUserID','UpdatedUserID',]
        widgets = {
            'LedgerName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('LedgerName')}),
            'ParentGroup': Select(attrs={'class' :'required form-control form', 'placeholder' : _('ParentGroup')}),
            'OpeningBalanceType': Select(attrs={'class' :'required form-control form', 'placeholder' : _('OpeningBalance')}),
            'OpeningBalanceAmount': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('OpeningBalanceAmount')}),
            'Description': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Description')}),
            'ID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('ID')}),
            # 'CreatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('CreatedUserID')}),
            'CreatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),
            # 'UpdatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('UpdatedUserID')}),
            'UpdatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),
            
            
        }


class CustomerTableForm(forms.ModelForm):

    class Meta:
        model = web_models.Customer
        exclude = ['ID','Action','UpdatedDate','CreatedDate','CreatedUserID','UpdatedUserID','CreatedUserID',]
        widgets = {
            'UserName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('UserName')}),
            'FirstName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('FirstName')}),
            'LastName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('LastName')}),
            'Email': EmailInput(attrs={'class' :'required form-control form', 'placeholder' : _('Email')}),
            'Country': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Country')}),
            'State': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('State')}),
            'PhoneNumber': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('PhoneNumber')}),
            'ID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('ID')}),
            # 'CreatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('CreatedUserID')}),
            'CreatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),
            # 'UpdatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('UpdatedUserID')}),
            'UpdatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),
            
        }


class CompaniesForm(forms.ModelForm):

    class Meta:
        model = web_models.Companies
        exclude = ['creator','updater','auto_id','is_deleted','Action','user']
        widgets = {
            'business_type': Select(attrs={'class' :'required form-control select', 'placeholder' : _('CompanyName')}),
            'CompanyName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('CompanyName')}),
            'Country': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Country')}),
            'State': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('State')}),
            'Country': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Country')}),
            'OfficePhoneNumber': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('OfficePhoneNumber')}),
            'Email': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Email')}),
            
        }


class CompanyProductForm(forms.ModelForm):

    class Meta:
        model = web_models.CompanyProduct
        exclude = ['creator','updater','auto_id','is_deleted','Action']
        widgets = {
            'software_plan': Select(attrs={'class' :'required select form-control form', 'placeholder' : _('Software Plan')}),
            'CompanyId': Select(attrs={'class' :'required select form-control form', 'placeholder' : _('Company')}),
            'ProductId': Select(attrs={'class' :'required select form-control form', 'placeholder' : _('Proudct')}),
            'No_ofDevice': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('No_ofDevice')}),
            'ProductExpiryDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _('ProductExpiryDate'), 'type' :'date'}),
            'AMCActive': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _('AMCActive'),'type' :'date'}),
            'AMCExpiry': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _('AMCExpiry'),'type' :'date'}),
            'IsTrialVersion': CheckboxInput(attrs={'class' :'form', 'placeholder' : _('IsTrialVersion')}),
            'service': CheckboxInput(attrs={'class' :'form', 'placeholder' : _('Service')}),
            'service_date': DateInput(attrs={'class' :'form-control form', 'placeholder' : _('Service Date'),'type' :'date'}),
            
        }


class CompanyDeviceForm(forms.ModelForm):

    class Meta:
        model = web_models.CompanyDevices 
        exclude = ['creator','updater','auto_id','is_deleted','Action']
        widgets = {
            'DeviceName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('DeviceName')}),
            'ProudctID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('ProudctID')}),
            'DeviceCode': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('DeviceCode')}),
            'Type': Select(attrs={'class' :'required form-control form', 'placeholder' : _('Type')}),
            'CompanyProductId': Select(attrs={'class' :'required form-control form', 'placeholder' : _('CompanyProductId')}),
            
        }


class UserForm(RegistrationForm):
    username = forms.CharField(label=_("Username"), 
                               max_length=254,
                               widget=forms.TextInput(
                                    attrs={'placeholder': 'Enter username','class':'required form-control'})
                               )

    first_name = forms.CharField(label=_("Firstname"), 
                               max_length=254,
                               widget=forms.TextInput(
                                    attrs={'placeholder': 'Enter firstname','class':'required form-control'})
                               )
    
    last_name = forms.CharField(label=_("Lastname"), 
                               max_length=254,
                               widget=forms.TextInput(
                                    attrs={'placeholder': 'Enter lastname','class':'required form-control'})
                               )
    email = forms.EmailField(label=_("Email"), 
                             max_length=254,
                             widget=forms.TextInput(
                                attrs={'placeholder': 'Enter email','class':'required form-control'})
                             )
    password1 = forms.CharField(label=_("Password"), 
                               widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password','class':'required form-control'})
                               )
    password2 = forms.CharField(label=_("Repeat Password"), 
                               widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password again','class':'required form-control'})
                               )
    
    bad_domains = ['guerrillamail.com']
    
    def clean_email(self):
        email_domain = self.cleaned_data['email'].split('@')[1]
        if User.objects.filter(email__iexact=self.cleaned_data['email'],is_active=True):
            raise forms.ValidationError(_("This email address is already in use."))        
        elif email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using %s email addresses is not allowed. Please supply a different email address." %email_domain))
        return self.cleaned_data['email']
    
    min_password_length = 6
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < self.min_password_length:
            raise forms.ValidationError("Password must have at least %i characters" % self.min_password_length)
        else:
            return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
        
    min_username_length = 6

    def clean_username(self):
        username = self.cleaned_data['username']
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        elif len(username) < self.min_username_length:
            raise forms.ValidationError("Username must have at least %i characters" % self.min_password_length)
        else:
            return self.cleaned_data['username']  


class RegForm(RegistrationForm):

    bad_domains = ['guerrillamail.com']

    def clean_email(self):
        email_domain = self.cleaned_data['email'].split('@')[1]
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use."))
        elif email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using %s email addresses is not allowed. Please supply a different email address." %email_domain))
        return self.cleaned_data['email']

    min_password_length = 6

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < self.min_password_length:
            raise forms.ValidationError("Password must have at least %i characters" % self.min_password_length)
        else:
            return password1

    min_username_length = 5

    def clean_username(self):
        username = self.cleaned_data['username']
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        elif len(username) < self.min_username_length:
            raise forms.ValidationError("Username must have at least %i characters" % self.min_password_length)
        else:
            return self.cleaned_data['username']




class RegisterForm(forms.ModelForm):

    class Meta:
        model = web_models.Register
        exclude = ['ID','user','UpdatedDate','CreatedDate','CreatedUserID','UpdatedUserID',]
        widgets = {
            'ID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('ID')}),
            'CompanyName': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('AccountGroupName')}),
            'Country': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('ParentGroup')}),
            'State': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Description')}),
            'PhoneNumber': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'number'}),
            'CreatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('CreatedUserID')}),
            'CreatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),
            'UpdatedUserID': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('UpdatedUserID')}),
            'UpdatedDate': DateInput(attrs={'class' :'required form-control form', 'placeholder' : _(''), 'type' : 'date'}),
            
        }
        

# master


class SaleMasterForm(forms.ModelForm):

    class Meta:
        model = web_models.SaleMaster
        exclude = ['Voucher_No','Date','ID']
        widgets = {
            'User': Select(attrs={'class' :'', 'placeholder' : _('IsTrialVersion')}),
            'total_amount': TextInput(attrs={'class' : '', 'placeholder': 'Total amount'}),
            'customer': TextInput(attrs={'class' :'', 'placeholder' : 'Customer'}),
        }


# details


class SaleDetailForm(forms.ModelForm):

    class Meta:
        model = web_models.SaleDetails
        exclude = ['Voucher',]
        widgets = {
            'Product': Select(attrs={'class' :'', 'placeholder' : _('IsTrialVersion')}),
            'Plan': Select(attrs={'class' :'', 'placeholder' : _('IsTrialVersion')}),
            'Year': Select(attrs={'class' :'', 'placeholder' : _('IsTrialVersion')}),
            'Price': TextInput(attrs={'class' : '', 'placeholder': ''}),
            'NoOfDevices': TextInput(attrs={'class' : '', 'placeholder': ''}),
        }