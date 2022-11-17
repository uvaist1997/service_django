from django import forms
from django.forms.widgets import TextInput,Textarea,DateInput,Select
from django.utils.translation import ugettext_lazy as _
from users import models as user_models
from web import models as web_models


# business type

class SoftwareVersionForm(forms.ModelForm):

    class Meta:
        model = user_models.SoftwareVersion
        exclude = ['creator','updater','auto_id','is_deleted','Action',]
        widgets = {
            'CurrentVersion': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'MinimumVersion': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
        }


class BusinessTypeForm(forms.ModelForm):

    class Meta:
        model = user_models.BusinessType
        exclude = ['creator','updater','auto_id','is_deleted','Action',]
        widgets = {
            'Name': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'Description': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
        }


# software plan


class SoftwarePlanForm(forms.ModelForm):

    class Meta:
        model = user_models.SoftwarePlan
        exclude = ['creator','updater','auto_id','is_deleted','Action',]
        widgets = {
            'product': Select(attrs={'class' : 'required select form-control w-50', 'placeholder': 'Product'}),
            'Name': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'Description': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
        }


# products


class ProductForm(forms.ModelForm):

    class Meta:
        model = user_models.Product
        exclude = ['creator','updater','auto_id','is_deleted','Action',]
        widgets = {
            'Name': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'Description': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
        }


# service


class ServiceForm(forms.ModelForm):

    class Meta:
        model = user_models.Service
        exclude = ['creator','updater','auto_id','is_deleted','Action',]
        widgets = {
            'Name': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'Description': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'Price': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''})
        }


# currency


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = user_models.Currency
        exclude = ['creator','updater','auto_id','is_deleted','Action',]
        widgets = {
            'Name': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'Description': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
        }


# service


class PeriodForm(forms.ModelForm):

    class Meta:
        model = user_models.Period
        exclude = ['creator','updater','auto_id','is_deleted','Action',]
        widgets = {
            'Name': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'Description': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''}),
            'NoOfDays': TextInput(attrs={'class' : 'required form-control w-50', 'placeholder': ''})
        }




class UserCompaniesForm(forms.ModelForm):

    class Meta:
        model = web_models.Companies
        exclude = ['business_type','CompanyName','Email','OfficePhoneNumber','creator','updater','auto_id','is_deleted','Action','user']
        widgets = {
            'Country': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Country')}),
            'State': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('State')}),
            
            'tagline': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Tag Line')}),
            'register_name': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('Register Name')}),
            'city': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('City')}),
            'trn_vat_gst': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('TRN')}),
            'cr_cin_number': TextInput(attrs={'class' :'required form-control form', 'placeholder' : _('CR Number')}),
        }

