from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseRedirect
from django.urls import reverse 
from users.functions import generate_form_errors,get_auto_ID
from main.functions import get_auto_id
from users.forms import BusinessTypeForm
from users.forms import SoftwarePlanForm
from users.forms import ProductForm
from users.forms import ServiceForm
from users.forms import CurrencyForm
from web.forms import SaleMasterForm,SaleDetailForm
from users.forms import PeriodForm
from users.models import BusinessType
from users.models import BusinessTypeLog
from users.models import SoftwarePlan
from users.models import SoftwarePlanLog
from users.models import Product
from users.models import ProductLog
from users.models import Service
from users.models import ServiceLog
from users.models import Currency
from users.models import CurrencyLog
from users.models import Period
from users.models import PeriodLog
from web.models import SaleMaster
from web.models import SaleDetails
from web.models import Companies
from web import models as web_models
from web import forms as web_forms
from users import models as user_models
from users import forms as user_forms
import json
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from web import models as web_model
from django.template.loader import render_to_string, get_template
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import resolve_url, render, get_object_or_404


@login_required
def change_password(request,pk):
    instance = get_object_or_404(User.objects.filter(pk=pk,is_active=True))
    if request.method == "POST":
        response_data = {}
        form = PasswordChangeForm(user=instance, data=request.POST)
        if form.is_valid():
            form.save()

            response_data = {
                'status' : 'true',
                'title' : "Successfully Changed",
                'redirect' : 'true',
                "redirect_url" : reverse('auth_login'),
                'message' : "Password Successfully Changed."
            }
        else:
            message = generate_form_errors(form,formset=False)
            print(form.errors)

            response_data = {
                'status' : 'false',
                'stable' : 'true',
                'title' : "Form validation error",
                "message" : message,
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        title = "Change Password"
        change_password_form = PasswordChangeForm(user=instance)
        context = {
            "change_password_form" : change_password_form,
            "title" : title,
            "instance" : instance,
        }
        return render(request, 'users/change_password.html', context)


# business type
@login_required
def list_business_types(request):
    user_view = user_models.BusinessType.objects.all()
    query = request.GET.get("q")
    if query:
        user_view = user_view.filter(Q(ID__icontains=query) | Q(Name__icontains=query) | Q(Description__icontains=query) | Q(CreatedUserID__id__icontains=query) | Q(CreatedDate__icontains=query) | Q(UpdatedUserID__id__icontains=query) | Q(UpdatedDate__icontains=query) | Q(Action__icontains=query))
    context ={
        "user_view" : user_view,
    }
    return render(request,'users/list_business_types.html',context)


@login_required
def create_business_type(request):    
    today = datetime.now(timezone.utc)
    if request.method == "POST":
        form = user_forms.BusinessTypeForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            
            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            data.Action = 'A'
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(user_models.BusinessType)
            data.save()

            BusinessTypeLog.objects.create(
                BusinessTypeid = data.auto_id,
                Name = Name,
                Description = Description,
                creator = request.user,
                updater = request.user,
                auto_id = data.auto_id,
                Action = 'A',
            )

            response_data = {
                "status" : "true",
                "title" : "user created",
                "message" : "user Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_business_types')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = BusinessTypeForm()
        context ={
            "form" : form,
        }
        return render(request,'users/create_business_type.html',context)


@login_required
def create_software_version(request):    
    today = datetime.now(timezone.utc)
    instance = None
    if user_models.SoftwareVersion.objects.filter().exists():
        instance = user_models.SoftwareVersion.objects.filter().first()
    if request.method == "POST":
        form = user_forms.SoftwareVersionForm(request.POST,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            
            CurrentVersion = form.cleaned_data['CurrentVersion']
            MinimumVersion = form.cleaned_data['MinimumVersion']
            data.Action = 'A'
            if not instance:
                data.auto_id = get_auto_id(user_models.SoftwareVersion)
            else:
                data.date_updated = datetime.now()
            data.creator = request.user
            data.updater = request.user
            data.save()

            # BusinessTypeLog.objects.create(
            #     BusinessTypeid = data.auto_id,
            #     Name = Name,
            #     Description = Description,
            #     creator = request.user,
            #     updater = request.user,
            #     auto_id = data.auto_id,
            #     Action = 'A',
            # )

            response_data = {
                "status" : "true",
                "title" : "Software Version",
                "message" : "Version Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:create_software_version')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = user_forms.SoftwareVersionForm(instance=instance)
        context ={
            "form" : form,
            "title":"Software Version"
        }
        return render(request,'users/create_software_version.html',context)


@login_required
def single_business_type(request,pk):
    single_user = user_models.BusinessType.objects.get(pk=pk)
    context ={
        "instance" : single_user,
    }
    return render(request,'users/single_business_type.html',context)


@login_required
def edit_business_type(request,pk):
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    single_brand = BusinessType.objects.get(pk=pk)
    ID = single_brand.ID
    if request.method == "POST":
        form = BusinessTypeForm(request.POST,instance=single_brand)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.UpdatedUserID = userInstance
            a.Action = "E"
            a.UpdatedDate = today

            BusinessTypeLog.objects.create(
                ID = ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                Action = a.Action,
                UpdatedDate = today,
                CreatedDate = today
            )
            form.save()
            response_data = {
                "status" : "true",
                "title" : "User updated",
                "message" : "User Successfully Updated",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_user')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = BusinessTypeForm(instance=single_brand)
        context ={
            "form" : form,
        }
        return render(request,'users/create_user.html',context)


@login_required
def delete_business_type(request,pk):
    single_brand = BusinessType.objects.get(pk=pk)
    single_brand.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "User deleted",
        "message" : "User Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_user')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# software plan
@login_required
def list_software_plan(request):
    user_view = SoftwarePlan.objects.all()
    query = request.GET.get("q")
    if query:
        user_view = user_view.filter(Q(ID__icontains=query) | Q(Name__icontains=query) | Q(Description__icontains=query) | Q(CreatedUserID__icontains=query) | Q(CreatedDate__icontains=query) | Q(UpdatedUserID__icontains=query) | Q(UpdatedDate__icontains=query) | Q(CAction__icontains=query))
    context ={
        "user_view" : user_view,
    }
    return render(request,'users/list_software_plan.html',context)


@login_required
def create_software_plan(request):
    if request.method == "POST":
        form = user_forms.SoftwarePlanForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            product = form.cleaned_data['product']
            data.Action = 'A'
            data.auto_id = get_auto_id(user_models.SoftwarePlan)
            data.creator = request.user
            data.updater = request.user
            data.product = product
            data.save()

            SoftwarePlanLog.objects.create(
                Name = Name,
                product = product,
                Description = Description,
                auto_id = data.auto_id,
                creator = request.user,
                updater = request.user,
                Action = "A",
            )

            response_data = {
                "status" : "true",
                "title" : "plan created",
                "message" : "plan Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_software_plan')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = user_forms.SoftwarePlanForm()
        context ={
            "form" : form,
        }
        return render(request,'users/create_software_plan.html',context)


@login_required
def single_software_plan(request,pk):
    single_soft = SoftwarePlan.objects.get(pk=pk)
    context ={
        "instance" : single_soft,
    }
    return render(request,'users/single_software_plan.html',context)


@login_required
def edit_software_plan(request,pk):
    instance = SoftwarePlan.objects.get(pk=pk,is_deleted=False)
    if request.method == "POST":
        form = user_forms.SoftwarePlanForm(request.POST,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            product = form.cleaned_data['product']
            data.Action = 'M'
            data.updater = request.user
            data.product = product
            data.save()

            # SoftwarePlanLog.objects.create(
            #     Name = Name,
            #     product = product,
            #     Description = Description,
            #     auto_id = data.auto_id,
            #     creator = request.user,
            #     updater = request.user,
            #     Action = "M",
            # )

            response_data = {
                "status" : "true",
                "title" : "plan created",
                "message" : "plan Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_software_plan')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = user_forms.SoftwarePlanForm(instance=instance)
        context ={
            "form" : form,
        }
        return render(request,'users/create_software_plan.html',context)


@login_required
def delete_software_plan(request,pk):
    instance = SoftwarePlan.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Plan deleted",
        "message" : "Plan Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_software_plan')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

# products
@login_required
def list_product(request):
    user_view = Product.objects.all()
    query = request.GET.get("q")
    if query:
        user_view = user_view.filter(Q(ID__icontains=query) | Q(Name__icontains=query) | Q(Description__icontains=query) | Q(CreatedUserID__icontains=query) | Q(CreatedDate__icontains=query) | Q(UpdatedUserID__icontains=query) | Q(UpdatedDate__icontains=query) | Q(CAction__icontains=query))
    context ={
        "user_view" : user_view,
    }
    return render(request,'users/list_product.html',context)


@login_required
def create_product(request):
    # today = datetime.date.today()
    if request.method == "POST":
        form = user_forms.ProductForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)

            Name = form.cleaned_data['Name']
            if not user_models.Product.objects.filter(Name=Name).exists():
                Description = form.cleaned_data['Description']
                data.Action = 'A'
                data.auto_id = get_auto_id(Product)
                data.creator = request.user
                data.updater = request.user
                data.save()

                user_models.ProductLog.objects.create(
                    Productid = data.auto_id,
                    Name = Name,
                    Description = Description,
                    Action = "A",
                    auto_id = data.auto_id,
                    creator = request.user,
                    updater = request.user,
                )

                response_data = {
                    "status" : "true",
                    "title" : "product created",
                    "message" : "product Successfully Created",
                    "redirect" : "true",
                    "redirect_url" : reverse('users:list_product')
                } 
            else:
                response_data = {
                    "status" : "false",
                    "stable" : "true",
                    "title" : "Alredy exists",
                    "message" : "Product is Alredy Exists"
                }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ProductForm()
        context ={
            "form" : form,
        }
        return render(request,'users/create_product.html',context)


@login_required
def single_product(request,pk):
    single_soft = Product.objects.get(pk=pk)
    context ={
        "instance" : single_soft,
    }
    return render(request,'users/product.html',context)


@login_required
def edit_product(request,pk):
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    single_brand = Product.objects.get(pk=pk)
    ID = single_brand.ID
    if request.method == "POST":
        form = ProductForm(request.POST,instance=single_brand)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.UpdatedUserID = userInstance
            a.Action = "E"
            a.UpdatedDate = today

            ProductLog.objects.create(
                ID = a.ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                Action = a.Action,
                UpdatedDate = today,
                CreatedDate = today
            )
            form.save()
            response_data = {
                "status" : "true",
                "title" : "Product updated",
                "message" : "Product Successfully Updated",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_product')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ProductForm(instance=single_brand)
        context ={
            "form" : form,
        }
        return render(request,'users/create_product.html',context)


@login_required
def delete_product(request,pk):
    single_product = Product.objects.get(pk=pk)
    single_product.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Product deleted",
        "message" : "Product Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_product')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# services
@login_required
def list_service(request):
    user_view = Service.objects.all()
    query = request.GET.get("q")
    if query:
        user_view = user_view.filter(Q(ID__icontains=query) | Q(Name__icontains=query) | Q(Description__icontains=query) | Q(CreatedUserID__icontains=query) | Q(CreatedDate__icontains=query) | Q(UpdatedUserID__icontains=query) | Q(UpdatedDate__icontains=query) | Q(Action__icontains=query) | Q(Price__icontains=query))
    context ={
        "user_view" : user_view,
    }
    return render(request,'users/list_service.html',context)


@login_required
def create_service(request):
    userid = request.user.id
    today = datetime.date.today()
    if request.method == "POST":
        form = ServiceForm(request.POST)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.CreatedUserID = userInstance
            a.UpdatedUserID = userInstance
            Price = form.cleaned_data['Price']
            a.Action = 'A'
            a.ID = get_auto_ID(Product)
            a.CreatedDate = today
            a.UpdatedDate = today
            a.save()

            ServiceLog.objects.create(
                ID = a.ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                Price = Price,
                Action = a.Action,
                CreatedDate = a.CreatedDate,
                UpdatedDate = a.UpdatedDate,
            )

            response_data = {
                "status" : "true",
                "title" : "service created",
                "message" : "service Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_service')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ServiceForm()
        context ={
            "form" : form,
        }
        return render(request,'users/create_service.html',context)


@login_required
def single_service(request,pk):
    single_soft = Service.objects.get(pk=pk)
    context ={
        "instance" : single_soft,
    }
    return render(request,'users/service.html',context)


@login_required
def edit_service(request,pk):
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    single_brand = Service.objects.get(pk=pk)
    ID = single_brand.ID
    if request.method == "POST":
        form = ServiceForm(request.POST,instance=single_brand)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.UpdatedUserID = userInstance
            Price = form.cleaned_data['Price']
            a.Action = "E"
            a.UpdatedDate = today

            ServiceLog.objects.create(
                ID = a.ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                Price = Price,
                Action = a.Action,
                UpdatedDate = today,
                CreatedDate = today
            )
            form.save()
            response_data = {
                "status" : "true",
                "title" : "service updated",
                "message" : "service Successfully Updated",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_service')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ServiceForm(instance=single_brand)
        context ={
            "form" : form,
        }
        return render(request,'users/create_service.html',context)


@login_required
def delete_service(request,pk):
    single_service = Service.objects.get(pk=pk)
    single_service.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "service deleted",
        "message" : "service Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_service')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# currency
@login_required
def list_currency(request):
    user_view = Currency.objects.all()
    query = request.GET.get("q")
    if query:
        user_view = user_view.filter(Q(ID__icontains=query) | Q(Name__icontains=query) | Q(Description__icontains=query) | Q(CreatedUserID__icontains=query) | Q(CreatedDate__icontains=query) | Q(UpdatedUserID__icontains=query) | Q(UpdatedDate__icontains=query) | Q(CAction__icontains=query))
    context ={
        "user_view" : user_view,
    }
    return render(request,'users/list_currency.html',context)


@login_required
def create_currency(request):
    userid = request.user.id
    today = datetime.date.today()
    if request.method == "POST":
        form = CurrencyForm(request.POST)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)     

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.CreatedUserID = userInstance
            a.UpdatedUserID = userInstance
            a.Action = 'A'
            a.ID = get_auto_ID(Product)
            a.CreatedDate = today
            a.UpdatedDate = today
            a.save()

            CurrencyLog.objects.create(
                ID = a.ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                Action = a.Action,
                CreatedDate = a.CreatedDate,
                UpdatedDate = a.UpdatedDate, 
            )

            response_data = {
                "status" : "true",
                "title" : "currency created",
                "message" : "currency Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_currency')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = CurrencyForm()
        context ={
            "form" : form,
        }
        return render(request,'users/create_currency.html',context)


@login_required
def single_currency(request,pk):
    single_soft = Currency.objects.get(pk=pk)
    context ={
        "instance" : single_soft,
    }
    return render(request,'users/currency.html',context)


@login_required
def edit_currency(request,pk):
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    single_brand = Currency.objects.get(pk=pk)
    ID = single_brand.ID
    if request.method == "POST":
        form = CurrencyForm(request.POST,instance=single_brand)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.UpdatedUserID = userInstance
            a.Action = "E"
            a.UpdatedDate = today

            CurrencyLog.objects.create(
                ID = a.ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                Action = a.Action,
                UpdatedDate = today,
                CreatedDate = today
            )
            form.save()
            response_data = {
                "status" : "true",
                "title" : "currency updated",
                "message" : "currency Successfully Updated",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_currency')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = CurrencyForm(instance=single_brand)
        context ={
            "form" : form,
        }
        return render(request,'users/create_currency.html',context)


@login_required
def delete_currency(request,pk):
    single_currency = Currency.objects.get(pk=pk)
    single_currency.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Currency deleted",
        "message" : "Currency Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_currency')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# period
@login_required
def list_period(request):
    user_view = Period.objects.all()
    query = request.GET.get("q")
    if query:
        user_view = user_view.filter(Q(ID__icontains=query) | Q(Name__icontains=query) | Q(Description__icontains=query) | Q(CreatedUserID__icontains=query) | Q(CreatedDate__icontains=query) | Q(UpdatedUserID__icontains=query) | Q(UpdatedDate__icontains=query) | Q(Action__icontains=query) | Q(NoOfDays__icontains=query))
    context ={
        "user_view" : user_view,
    }
    return render(request,'users/list_period.html',context)


@login_required
def create_period(request):
    userid = request.user.id
    today = datetime.date.today()
    if request.method == "POST":
        form = PeriodForm(request.POST)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.CreatedUserID = userInstance
            a.UpdatedUserID = userInstance
            NoOfDays = form.cleaned_data['NoOfDays']
            a.Action = 'A'
            a.ID = get_auto_ID(Period)
            a.CreatedDate = today
            a.UpdatedDate = today
            a.save()

            PeriodLog.objects.create(
                ID = a.ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                NoOfDays = NoOfDays,
                Action = a.Action,
                CreatedDate = a.CreatedDate,
                UpdatedDate = a.UpdatedDate,
            )

            response_data = {
                "status" : "true",
                "title" : "period created",
                "message" : "period Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_period')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = PeriodForm()
        context ={
            "form" : form,
        }
        return render(request,'users/create_period.html',context)


@login_required
def single_period(request,pk):
    single_soft = Period.objects.get(pk=pk)
    context ={
        "instance" : single_soft,
    }
    return render(request,'users/period.html',context)


@login_required
def edit_period(request,pk):
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    single_brand = Period.objects.get(pk=pk)
    ID = single_brand.ID
    if request.method == "POST":
        form = PeriodForm(request.POST,instance=single_brand)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            Name = form.cleaned_data['Name']
            Description = form.cleaned_data['Description']
            a.UpdatedUserID = userInstance
            NoOfDays = form.cleaned_data['NoOfDays']
            a.Action = "E"
            a.UpdatedDate = today

            PeriodLog.objects.create(
                ID = a.ID,
                Name = Name,
                Description = Description,
                CreatedUserID = userInstance,
                UpdatedUserID = userInstance,
                NoOfDays = NoOfDays,
                Action = a.Action,
                UpdatedDate = today,
                CreatedDate = today
            )
            form.save()
            response_data = {
                "status" : "true",
                "title" : "period updated",
                "message" : "period Successfully Updated",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_period')
            } 
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = PeriodForm(instance=single_brand)
        context ={
            "form" : form,
        }
        return render(request,'users/create_period.html',context)


@login_required
def delete_period(request,pk):
    single_period = Period.objects.get(pk=pk)
    single_period.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "period deleted",
        "message" : "period Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_period')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# master
@login_required
def list_master(request):
    
    user_view = None
    comp_name = None
    # user_view = SaleMaster.objects.filter()
    company_instance = web_model.Companies.objects.filter()
    user_instance = User.objects.filter(is_superuser=False)
    user = request.GET.get("user")
    company = request.GET.get("company")
    VanId = request.GET.get("VanId")
    filter_type = request.GET.get("type")

    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and VanId and filter_type:
        user_view = SaleMaster.objects.filter(CompanyProductId__CompanyId=company,VanId=VanId).order_by('Date')
    elif user and company and VanId:
        user_view = SaleMaster.objects.filter(CompanyProductId__CompanyId=company,VanId=VanId).order_by('TransactionId')
    context ={
        "title" : "Sale Master",
        "user_view" : user_view,
        "company_instance" : company_instance,
        "user_instance" : user_instance,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_master.html',context)


# @login_required
# def get_sale_list(request):
#     user_id = request.GET.get('id')
#     company_id = request.GET.get('company_id')
#     print(user_id,'user_id')

#     if user_id:
#         instances = web_models.SaleMaster.objects.filter(is_deleted=False,CompanyProductId__CompanyId=company_id)
#         cust_arr = []
#         data_arr = []
#         for i in instances:
#             print(i.CompanyName,'CompanyName')
#             company_dic = {
#                 "id" : str(i.pk),
#                 "name" : str(i.CompanyName),
#                 "type" : str(i.business_type),
#                 "email" : str(i.Email),
#             }
            
#             data_arr.append(company_dic)
#             print(data_arr,'data_arr')
#         template_name = 'reports/includes/company_list.html'
#         # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
#         if instances:
#             context = {
#                 'instances': instances,
#             }
#             html_content = render_to_string(template_name, context)
#             response_data = {
#                 "status": "true",
#                 'comapny_list': html_content,
#             }
#         else:
#             response_data = {
#                 "status": "false",
#                 "message": "Company not found"
#             }

#         return HttpResponse(json.dumps(response_data), content_type='application/javascript')

#     else:
#         response_data = {
#             "status": "false",
#             "message": "Customer not found"
#         }

#     return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def get_user_companies(request):
    user_id = request.GET.get('id')
    print(user_id,'user_id___________________________$%')

    if user_id:
        instances = web_model.Companies.objects.filter(user__id=user_id)
        cust_arr = []
        data_arr = []
        for i in instances:
            print(i.user.id,'CompanyName')
            order_dic = {
                "id" : str(i.pk),
                "name" : str(i.CompanyName),
            }
            if i.CompanyName not in cust_arr:
                cust_arr.append(i.CompanyName)
                data_arr.append(order_dic)
        template_name = 'select.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if instances:
            print(cust_arr,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            context = {
                'instances': data_arr,
            }
            html_content = render_to_string(template_name, context)
            response_data = {
                "status": "true",
                'customer_select': data_arr,
            }
        else:
            response_data = {
                "status": "false",
                "message": "Companies not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Companies not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def get_company_vanId(request):
    company_id = request.GET.get('id')
    try:
        voucher_type = request.GET.get('voucher_type')
    except:
        voucher_type = ""

    if company_id:
        if voucher_type == "SaleMaster":
            instances = web_model.SaleMaster.objects.filter(CompanyProductId__CompanyId=company_id)
            print(voucher_type)
        elif voucher_type == "SaleReturnMaster":
            instances = web_model.SaleReturnMaster.objects.filter(CompanyProductId__CompanyId=company_id)
            print(voucher_type)
        elif voucher_type == "StockOrder":
            print(voucher_type)
            instances = web_model.StockOrder.objects.filter(CompanyProductId__CompanyId=company_id)
        elif voucher_type == "Reciept":
            print(voucher_type)
            instances = web_model.Reciept.objects.filter(CompanyProductId__CompanyId=company_id)
        elif voucher_type == "Payment":
            print(voucher_type)
            instances = web_model.Payment.objects.filter(CompanyProductId__CompanyId=company_id)
        elif voucher_type == "SaleAccountLedger":
            print(voucher_type)
            instances = web_model.SaleAccountLedger.objects.filter(CompanyProductId__CompanyId=company_id)
        elif voucher_type == "VanSettings":
            instances = web_model.VanSettings.objects.filter(CompanyProductId__CompanyId=company_id)

        cust_arr = []
        data_arr = []
        for i in instances:
            VanId = ""
            if voucher_type == "SaleMaster":
                VanId = str(i.VanId)
            elif voucher_type == "SaleReturnMaster":
                VanId = str(i.VanId)
            elif voucher_type == "StockOrder":
                VanId = str(i.VanID)
            elif voucher_type == "Reciept":
                VanId = str(i.Van_ID)
            elif voucher_type == "Payment":
                VanId = str(i.Van_ID)
            elif voucher_type == "SaleAccountLedger":
                VanId = str(i.RouteId)
            elif voucher_type == "VanSettings":
                VanId = str(i.VanId)
                print("Vansettings")
            order_dic = {
                "id" : str(VanId),
                "name" : str(VanId),
            }
            if VanId not in cust_arr:
                cust_arr.append(VanId)
                data_arr.append(order_dic)
        template_name = 'select.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if instances:
            print(cust_arr,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            context = {
                'instances': data_arr,
            }
            html_content = render_to_string(template_name, context)
            response_data = {
                "status": "true",
                "voucher_type":voucher_type,
                'customer_select': data_arr,
            }
        else:
            response_data = {
                "status": "false",
                "voucher_type":voucher_type,
                "message": "Companies not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Companies not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def list_details(request, pk):
    sale_item = SaleDetails.objects.filter(SaleId=pk)
    sale = SaleMaster.objects.filter(pk=pk)
    context ={
        "userone_view" : sale_item,
        "user_view" : sale,
    }
    return render(request,'users/list_details.html',context)


@login_required
def master(request):
    SaleDetailFormset = formset_factory(SaleDetailForm,extra=1)
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    text = get_auto_id(SaleMaster)
    if request.method == "POST":
        form = SaleMasterForm(request.POST)
        details_formset = SaleDetailFormset(request.POST,prefix='details_formset')
        
        userInstance = User.objects.get(pk=userid)
        if form.is_valid() and details_formset.is_valid():

            a = form.save(commit=False)

            customer = form.cleaned_data['customer']
            total_amount = form.cleaned_data['total_amount']
            a.User = userInstance
            a.Voucher_No = text
            a.Date = today
            a.save()

            SaleMasterLog.objects.create(
                Voucher_No = a.Voucher_No,
                customer = customer,
                total_amount = total_amount,
                User = userInstance,
                Date = a.Date,
            )

            for item in details_formset:
                Product = item.cleaned_data['Product']
                Plan = item.cleaned_data['Plan']
                Year = item.cleaned_data['Year']
                Price = item.cleaned_data['Price']
                NoOfDevices = item.cleaned_data['NoOfDevices']
                
                
                Details.objects.create(
                    Voucher = a,
                    Product = Product,
                    Plan = Plan,
                    Year = Year,
                    Price = Price,
                    NoOfDevices = NoOfDevices,
                )

                Details_log.objects.create(
                    Voucher = a,
                    Product = Product,
                    Plan = Plan,
                    Year = Year,
                    Price = Price,
                    NoOfDevices = NoOfDevices,
                )

            response_data = {
                "status" : "true",
                "title" : "Successfully created",
                "message" : "Sale Successfully Created",
                "redirect" : "true",
                "redirect_url" : reverse('users:list_master')
                # ,kwargs={'pk':a.pk}
            } 
        else:
            message = generate_form_errors(form,formset=False) 
            message += generate_form_errors(details_formset,formset=True)      
            
            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = MasterForm()
        detail_form = DetailsForm()
        details_formset = SaleDetailFormset(prefix='details_formset')
        context ={
            "form" : form,
            "details_formset" : details_formset,
            "text" : text,
            "today" : today
        }
        return render(request,'users/master.html',context)


@login_required
def edit_details(request,pk):
    if request.method == "POST":
        pass

    else:
        form = MasterForm()
        detail_form = DetailsForm()
        # details_formset = SaleDetailFormset(prefix='details_formset')
        context ={
            "form" : form,
            # "details_formset" : details_formset,
            # "text" : text,
            # "today" : today,
            "detail_form" : detail_form,
        }
        return render(request,'users/master.html',context)


@login_required
def delete_master(request,pk):
    single_master = web_model.SaleMaster.objects.get(pk=pk)
    single_detail = web_model.SaleDetails.objects.filter(SaleId=single_master)
    for i in single_detail:
        i.delete()
    single_master.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Master deleted",
        "message" : "Master Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_master')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_sale_status(request,pk):
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    single_master = web_model.SaleMaster.objects.get(pk=pk)
    if single_master.status:
        single_master.status = False
    else:
        single_master.status = True
    print(single_master.status)
    single_master.save()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Master updated",
        "message" : "Master Successfully Updated",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_master')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_reciept_status(request,pk):
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    single_master = web_model.Reciept.objects.get(pk=pk)
    if single_master.status:
        single_master.status = False
    else:
        single_master.status = True
    print(single_master.status)
    single_master.save()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Reciept updated",
        "message" : "Reciept Successfully Updated",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_reciept')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_payment_status(request,pk):
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    single_master = web_model.Payment.objects.get(pk=pk)
    if single_master.status:
        single_master.status = False
    else:
        single_master.status = True
    print(single_master.status)
    single_master.save()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Payment updated",
        "message" : "Payment Successfully Updated",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_payment')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_stock_order_status(request,pk):
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    single_master = web_model.StockOrder.objects.get(pk=pk)
    if single_master.status:
        single_master.status = False
    else:
        single_master.status = True
    print(single_master.status)
    single_master.save()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "StockOrder updated",
        "message" : "StockOrder Successfully Updated",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_stock_order')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def edit_sale_return_status(request,pk):
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    single_master = web_model.SaleReturnMaster.objects.get(pk=pk)
    if single_master.status:
        single_master.status = False
    else:
        single_master.status = True
    print(single_master.status)
    single_master.save()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "SaleReturnMaster updated",
        "message" : "SaleReturnMaster Successfully Updated",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_sale_returns')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



@login_required
def single_view_master(request,pk):
    instance = web_model.SaleMaster.objects.get(pk=pk)
    instances = web_model.SaleDetails.objects.filter(SaleId=instance)

    context ={
        "instances" : instances,
        "instance" : instance,
    }
    return render(request,'users/single_view_master.html',context)



@login_required
def delete_details(request,pk):
    single_details = Details.objects.get(pk=pk)
    master_pk = single_details.Voucher.pk
    print(master_pk)
    single_details.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "period deleted",
        "message" : "period Successfully deleted",
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# Reciept
@login_required
def list_reciept(request):
    print("UVVVVVVAAAIIIIIIIISSSSSS>>>>>>")
    user = request.GET.get("user")
    company = request.GET.get("company")
    VanId = request.GET.get("VanId")
    filter_type = request.GET.get("type")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and VanId and filter_type:
        user_view = web_model.Reciept.objects.filter(CompanyProductId__CompanyId=company,Van_ID=VanId).order_by('Date')
    elif user and company and VanId:
        user_view = web_model.Reciept.objects.filter(CompanyProductId__CompanyId=company,Van_ID=VanId).order_by('TransactionId')
    print(user_view)

    context ={
        "title" : "Reciept",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_reciept.html',context)

@login_required
def single_view_reciept(request,pk):
    instance = web_model.Reciept.objects.get(pk=pk)
    instances = web_model.RecieptDetail.objects.filter(RecieptId=instance)

    context ={
        "instances" : instances,
        "instance" : instance,
    }
    return render(request,'users/single_view_reciept.html',context)


@login_required
def delete_reciept(request,pk):
    instance = web_model.Reciept.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Reciept",
        "message" : "Reciept Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_reciept')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# Reciept
@login_required
def list_payment(request):
    print("UVVVVVVAAAIIIIIIIISSSSSS>>>>>>")
    user = request.GET.get("user")
    company = request.GET.get("company")
    VanId = request.GET.get("VanId")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and VanId:
        user_view = web_model.Payment.objects.filter(CompanyProductId__CompanyId=company,Van_ID=VanId).order_by('TransactionId')
    print(user_view)

    context ={
        "title" : "Payment",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_payment.html',context)


@login_required
def single_view_payment(request,pk):
    instance = web_model.Payment.objects.get(pk=pk)
    instances = web_model.PaymentDetail.objects.filter(PaymentId=instance)

    context ={
        "instances" : instances,
        "instance" : instance,
    }
    return render(request,'users/single_view_payment.html',context)


@login_required
def delete_payment(request,pk):
    instance = web_model.Payment.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Payment",
        "message" : "Payment Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_reciept')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# SaleReturnMaster
@login_required
def list_sale_returns(request):
    print("UVVVVVVAAAIIIIIIIISSSSSS>>>>>>")
    user = request.GET.get("user")
    company = request.GET.get("company")
    VanId = request.GET.get("VanId")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and VanId:
        user_view = web_model.SaleReturnMaster.objects.filter(CompanyProductId__CompanyId=company,VanId=VanId).order_by('TransactionId')
    print(user_view)

    context ={
        "title" : "SaleReturn",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_sale_returns.html',context)


@login_required
def single_view_sale_return(request,pk):
    instance = web_model.SaleReturnMaster.objects.get(pk=pk)
    instances = web_model.SaleReturnDetails.objects.filter(SaleReturnMasterId=instance)

    context ={
        "instances" : instances,
        "instance" : instance,
    }
    return render(request,'users/single_view_sale_return.html',context)


@login_required
def delete_sale_return(request,pk):
    instance = web_model.SaleReturnMaster.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Sale Return",
        "message" : "Sale Return Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_sale_returns')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# StockOrder
@login_required
def list_stock_order(request):
    print("UVVVVVVAAAIIIIIIIISSSSSS>>>>>>")
    user = request.GET.get("user")
    company = request.GET.get("company")
    VanId = request.GET.get("VanId")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and VanId:
        user_view = web_model.StockOrder.objects.filter(CompanyProductId__CompanyId=company,VanID=VanId).order_by('TransactionID')
    print(user_view)

    context ={
        "title" : "StockOrder",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_stock_order.html',context)


@login_required
def single_view_stock_order(request,pk):
    instance = web_model.StockOrder.objects.get(pk=pk)
    instances = web_model.StockOrderDetail.objects.filter(StockOrderId=instance)

    context ={
        "instances" : instances,
        "instance" : instance,
    }
    return render(request,'users/single_view_stock_order.html',context)


@login_required
def delete_stock_order(request,pk):
    instance = web_model.StockOrder.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "StockOrder",
        "message" : "StockOrder Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_stock_order')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale products
@login_required
def list_sale_products(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.SaleProduct.objects.filter(CompanyProductId__CompanyId=company)

    context ={
        "title" : "Sale Product",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_sale_products.html',context)


@login_required
def delete_sale_product(request,pk):
    instance = web_model.SaleProduct.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Sale Product",
        "message" : "Sale Product Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_sale_products')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale price
@login_required
def list_sale_price(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    product = request.GET.get("product")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    # product_instance = web_model.SaleProduct.objects.filter()
    product_instance = []
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and product:
        user_view = web_model.SalePrice.objects.filter(CompanyProductId__CompanyId=company)
    context ={
        "title" : "Sale Price",
        "user_view" : user_view,
         "userid" : user,
        "company" : company,
        "comp_name" : comp_name,
        "product_instance" : product_instance,
    }
    return render(request,'users/list_sale_price.html',context)


@login_required
def delete_sale_price(request,pk):
    instance = web_model.SalePrice.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Sale Product",
        "message" : "Sale Price Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_sale_price')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def get_sale_price_list(request):
    user = request.GET.get("id_user")
    company = request.GET.get("id_company")
    product_id = request.GET.get("id_product")

    print(product_id,"TESTINGGGGGGG...........")
    if user and company:
        # user_view = None
        # comp_name = None
        saleprice_instance = web_model.SalePrice.objects.filter()
        product_instance = web_model.SaleProduct.objects.filter()
        if web_model.Companies.objects.filter(pk=company).exists():
            comp_name = web_model.Companies.objects.get(pk=company).CompanyName
        if user and company and product_id:
            user_view = web_model.SalePrice.objects.filter(CompanyProductId__CompanyId=company,ProductId=product_id)
            for i in user_view:
                print(i.ProductId,"UNDAAAAAAAAAAAAAAAAAA")
        else:
            print("ELLLLLLLLLLLLAAAAAAAAAAAA")
            user_view = web_model.SalePrice.objects.filter(CompanyProductId__CompanyId=company)
            print(user_view,'=======================')
        template_name = 'users/includes/sale_price_list.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if user and company:
            context = {
                "user_view" : user_view,                
                "userid" : user,
                "company" : company,
                "comp_name" : comp_name,
                "saleprice_instance" : saleprice_instance,
                "product_instance" : product_instance
            }
            html_content = render_to_string(template_name, context)
            response_data = {
                "status": "true",
                "count" : user_view.count(),
                'comapny_list': html_content,
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            response_data = {
                "status": "false",
                "message": "Company not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Customer not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



# sale account ledger
@login_required
def list_sale_account_ledger(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    RouteId = request.GET.get("VanId")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and RouteId:
        user_view = web_model.SaleAccountLedger.objects.filter(CompanyProductId__CompanyId=company,RouteId=RouteId)
    context ={
        "title" : "Sale Account Ledger",
        "user_view" : user_view,
         "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_sale_account_ledger.html',context)


@login_required
def delete_sale_account_ledger(request,pk):
    instance = web_model.SaleAccountLedger.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Sale Account Ledger",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_sale_account_ledger')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale account ledger
@login_required
def list_warehouse_stock(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    warehouse = request.GET.get("warehouse")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    warehouse_instance = web_model.WarehouseStock.objects.filter()
    # product_instance = web_model.SaleProduct.objects.filter()
    product_instance = []

    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.WarehouseStock.objects.filter(CompanyProductId__CompanyId=company,WarehouseId=warehouse)
    context ={
        "title" : "Warehouse Stock",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name,
        "warehouse_instance" : warehouse_instance,
        "product_instance" : product_instance,

    }
    return render(request,'users/list_warehouse_stock.html',context)


@login_required
def get_warehouse_stock_list(request):
    user = request.GET.get("id_user")
    company = request.GET.get("id_company")
    warehouse = request.GET.get("id_warehouse")
    product_id = request.GET.get("id_product")

    print(product_id,"TESTINGGGGGGG...........")
    if user and company and warehouse:
        # user_view = None
        # comp_name = None
        warehouse_instance = web_model.WarehouseStock.objects.filter()
        product_instance = web_model.SaleProduct.objects.filter()
        if web_model.Companies.objects.filter(pk=company).exists():
            comp_name = web_model.Companies.objects.get(pk=company).CompanyName
        if user and company and product_id:
            user_view = web_model.WarehouseStock.objects.filter(CompanyProductId__CompanyId=company,WarehouseId=warehouse,ProductId=product_id)
            for i in user_view:
                print(i.ProductId,"UNDAAAAAAAAAAAAAAAAAA")
        else:
            print("ELLLLLLLLLLLLAAAAAAAAAAAA")
            user_view = web_model.WarehouseStock.objects.filter(CompanyProductId__CompanyId=company,WarehouseId=warehouse)
            print(user_view,'=======================')
        template_name = 'users/includes/warehouse_stock_list.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if user and company:
            context = {
                "user_view" : user_view,
                "userid" : user,
                "company" : company,
                "comp_name" : comp_name,
                "warehouse_instance" : warehouse_instance,
                "product_instance" : product_instance
            }
            html_content = render_to_string(template_name, context)
            response_data = {
                "status": "true",
                'comapny_list': html_content,
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            response_data = {
                "status": "false",
                "message": "Company not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Customer not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def get_company_products(request):
    company_id = request.GET.get('id')
    print(company_id,'company_id___________________________$%')

    if company_id:
        instances = web_model.SaleProduct.objects.filter(CompanyProductId__CompanyId=company_id)
        count = instances.count()
        warehouse_instances = web_model.WarehouseStock.objects.filter(CompanyProductId__CompanyId=company_id)
        cust_arr = []
        data_arr = []
        for i in instances:
            for j in warehouse_instances:
                if j.ProductId == i.ProductId:
                    print(i.ProductId,'Productname')
                    order_dic = {
                        "id" : str(i.ProductId),
                        "name" : str(i.Productname),
                    }
                    if i.Productname not in cust_arr:
                        cust_arr.append(i.Productname)
                        data_arr.append(order_dic)
        template_name = 'select.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if instances:
            # print(cust_arr,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            context = {
                'instances': data_arr,
            }
            html_content = render_to_string(template_name, context)
            response_data = {
                "status": "true",
                'customer_select': data_arr,
                'count':count,
            }
        else:
            response_data = {
                "status": "false",
                "message": "Product not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Product not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def delete_warehouse_stock(request,pk):
    instance = web_model.WarehouseStock.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Warehouse Stock",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_warehouse_stock')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale expence ledger
@login_required
def list_expence_ledger(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.ExpenseLedger.objects.filter(CompanyProductId__CompanyId=company)
    context ={
        "title" : "Expence Ledger",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_expence_ledger.html',context)


@login_required
def delete_expence_ledger(request,pk):
    instance = web_model.ExpenseLedger.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Expence Ledger",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_expence_ledger')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale expence ledger
@login_required
def list_last_sale_price(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.LastSalesPrice.objects.filter(CompanyProductId__CompanyId=company)

    context ={
        "title" : "List Last Sale Price",
        "user_view" : user_view,
         "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_last_sale_price.html',context)


@login_required
def delete_last_sale_price(request,pk):
    instance = web_model.LastSalesPrice.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "List Last Sale Price",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_last_sale_price')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale sale route
@login_required
def list_sale_route(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.SaleRoute.objects.filter(CompanyProductId__CompanyId=company)
    context ={
        "title" : "Sale Route",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_sale_route.html',context)


@login_required
def delete_sale_route(request,pk):
    instance = web_model.SaleRoute.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Sale Route",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_sale_route')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# # sale sale route
# def list_sale_route(request):
#     user_view = web_model.SaleRoute.objects.all()
#     query = request.GET.get("q")
#     if query:
#         user_view = user_view.filter(Q(id__icontains=query) | Q(CompanyProductId__CompanyId__CompanyName__icontains=query) | Q(CompanyProductId__CompanyId__user__username__icontains=query))
#     context ={
#         "title" : "Sale Route",
#         "user_view" : user_view,
#     }
#     return render(request,'users/list_sale_route.html',context)


# def delete_sale_route(request,pk):
#     instance = web_model.SaleRoute.objects.get(pk=pk)
#     instance.delete()
#     response_data = {
#         "status" : "true",
#         "icon" : 'warning',
#         "title" : "Sale Route",
#         "message" : "Successfully deleted",
#         "redirect" : "true",
#         "redirect_url" : reverse('users:list_sale_route')
#     } 
#     return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale transaction type
@login_required
def list_transaction_type(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.TransactionType.objects.filter(CompanyProductId__CompanyId=company)
    context ={
        "title" : "Transaction Type",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_transaction_type.html',context)


@login_required
def delete_transaction_type(request,pk):
    instance = web_model.TransactionType.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Transaction Type",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_transaction_type')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# sale sale route
@login_required
def list_van_route(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.VanRoute.objects.filter(CompanyProductId__CompanyId=company)
    context ={
        "title" : "Van Route",
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_van_route.html',context)



@login_required
def delete_van_route(request,pk):
    instance = web_model.VanRoute.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Van Route",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_van_route')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# master
# def list_sale_return(request):
#     user = request.GET.get("user")
#     company = request.GET.get("company")
#     user_view = None
#     comp_name = None
#     print(company,"DDDDDDD")
#     if web_model.Companies.objects.filter(pk=company).exists():
#         comp_name = web_model.Companies.objects.get(pk=company).CompanyName
#     if user and company:
#         user_view = web_model.SaleReturnMaster.objects.filter(CompanyProductId__CompanyId=company)
#     context ={
#         "title" : "Sale Return",
#         "user_view" : user_view,
#         "userid" : user,
#         "company" : company,
#         "comp_name" : comp_name 
#     }
#     return render(request,'users/list_sale_return.html',context)


# def delete_sale_return(request,pk):
#     instance = web_model.SaleReturnMaster.objects.get(pk=pk)
#     instances = web_model.SaleReturnDetails.objects.filter(SaleReturnMasterId=instance)
#     for i in instances:
#         i.delete()
#     instance.delete()
#     response_data = {
#         "status" : "true",
#         "icon" : 'warning',
#         "title" : "Sale Return",
#         "message" : "Successfully deleted",
#         "redirect" : "true",
#         "redirect_url" : reverse('users:list_sale_return')
#     } 
#     return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# master
@login_required
def list_sale_order(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    try:
        VanId = request.GET.get("VanId")
    except:
        VanId = None
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.SaleOrder.objects.filter(CompanyProductId__CompanyId=company)
    if user and company and VanId:
        user_view = web_model.SaleOrder.objects.filter(CompanyProductId__CompanyId=company,VanId=VanId)
    print(company,"##########DDDDDDD")
    context ={
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_sale_order.html',context)


@login_required
def single_view_sale_order(request,pk):
    instance = web_model.SaleOrder.objects.get(pk=pk)
    instances = web_model.SaleOrderDetails.objects.filter(SaleOrderId=instance)

    context ={
        "instances" : instances,
        "instance" : instance,
    }
    return render(request,'users/single_view_sale_order.html',context)


@login_required
def delete_sale_order(request,pk):
    instance = web_model.SaleOrder.objects.get(pk=pk)
    instances = web_model.SaleOrderDetails.objects.filter(SaleOrderId=instance)
    for i in instances:
        i.delete()
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Sale Order",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_sale_order')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



# master
@login_required
def list_bill_wise(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    print(company,"DDDDDDD")
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = web_model.BillWise.objects.filter(CompanyProductId__CompanyId=company)
    context ={
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_bill_wise.html',context)


@login_required
def delete_bill_wise(request,pk):
    instance = web_model.BillWise.objects.get(pk=pk)
    
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Bill Wise",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_bill_wise')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



@login_required
def list_users(request):
    instances = User.objects.filter(is_superuser=False)
    context ={
        "instances" : instances,
    }
    return render(request,'users/list_users.html',context)


@login_required
def delete_user(request,pk):
    user = User.objects.get(pk=pk)
    user.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "User deleted",
        "message" : "User Successfully deleted",
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def user_companies(request):
    print(request.user,"@@@@@")
    instances = Companies.objects.filter(user=request.user)
    for i in instances:
        print(i.user,'username')
    context ={
        "instances" : instances,
    }
    return render(request,'users/user_companies.html',context)


def user_edit_company(request,pk):
    today = datetime.now(timezone.utc)
    instance = web_models.Companies.objects.get(pk=pk)
    if request.method == "POST":
        form = user_forms.UserCompaniesForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            # a.ID = get_auto_ID(web_models.Companies)
            data.creator = request.user
            data.updater = request.user

            Country = form.cleaned_data['Country']
            State = form.cleaned_data['State']
            register_name = form.cleaned_data['register_name']
            tagline = form.cleaned_data['tagline']
            city = form.cleaned_data['city']
            trn_vat_gst = form.cleaned_data['trn_vat_gst']
            cr_cin_number = form.cleaned_data['cr_cin_number']
            
           
            data.Action="M"
            # data.Country = Country
            # data.State = State

            # data.register_name = register_name
            # data.tagline = tagline
            # data.city = city
            # data.trn_vat_gst = trn_vat_gst
            # data.cr_cin_number = cr_cin_number
            # data.logo = request.FILES
            data.save()

            web_models.CompaniesLog.objects.create(
                user = request.user,
                Companyid = data.auto_id,
                auto_id = get_auto_id(web_models.CompaniesLog),
                creator = request.user,
                updater = request.user,
                business_type = data.business_type,
                OfficePhoneNumber = data.OfficePhoneNumber,
                Email = data.Email,
                Action = "M",
                Country = Country,
                State = State,
                
                logo = data.logo,
                register_name = register_name,
                tagline = tagline,
                city = city,
                trn_vat_gst = trn_vat_gst,
                cr_cin_number = cr_cin_number,
            )
            form.save()
            response_data = {
                "status" : "true",
                "title" : "companies edited",
                "message" : "companies Successfully edited",
                "redirect" : "true",
                "redirect_url" : reverse('users:user_companies')
            } 
        else:
            message = generate_form_errors(form,formset=False)
            print(form)
            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = user_forms.UserCompaniesForm(instance=instance)
        context ={
            "form" : form,
        }
        return render(request,'users/user_edit_company.html',context)

@login_required
def list_van_settings(request):
    
    user_view = None
    comp_name = None
    # user_view = SaleMaster.objects.filter()
    company_instance = web_model.Companies.objects.filter()
    user_instance = User.objects.filter(is_superuser=False)
    user = request.GET.get("user")
    company = request.GET.get("company")
    VanId = request.GET.get("VanId")
    
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company and VanId:
        user_view = web_model.VanSettings.objects.filter(CompanyProductId__CompanyId=company,VanId=VanId)
    context ={
        "title" : "VanSettings",
        "user_view" : user_view,
        "company_instance" : company_instance,
        "user_instance" : user_instance,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name
    }
    return render(request,'users/list_van_settings.html',context)


@login_required
def delete_van_settings(request,pk):
    instance = web_model.VanSettings.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "Master deleted",
        "message" : "Master Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:list_van_settings')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def single_view_vansettings(request,pk):
    instance = web_model.VanSettings.objects.get(pk=pk)

    context ={
        "instance" : instance,
    }
    return render(request,'users/single_view_vansettings.html',context)


@login_required
def company_product_report(request):
    print(request.user.id)
    companyproduct_view = web_model.CompanyProduct.objects.all()
    query = request.GET.get("q")
    if query:
        companyproduct_view = companyproduct_view.filter(Q(CompanyId__CompanyName__icontains=query))
    context ={
        "companyproduct_view" : companyproduct_view,
    }
    return render(request,'users/company_product_report.html',context)


@login_required
def print_company_product(request,pk):
    print(request.user.id)
    instance = web_model.CompanyProduct.objects.get(pk=pk)
    # query = request.GET.get("q")
    # if query:
    #     companyproduct_view = companyproduct_view.filter(Q(CompanyId__CompanyName__icontains=query))
    context ={
        "instance" : instance,
    }
    return render(request,'users/print_compay_product.html',context)


@login_required
def e_invoice_list(request):
    print(request.user,"@@@@@")
    if request.user.is_superuser:
        is_superuser = True
        instances = user_models.EInvoice.objects.filter(is_deleted=False)
    else:
        is_superuser = False
        instances = user_models.EInvoice.objects.filter(is_deleted=False,creator=request.user)
    
    context ={
        "is_superuser":is_superuser,
        "instances" : instances,
    }
    return render(request,'users/e_invoice_list.html',context)


# @login_required
def e_invoice_view(request):
    CompanyID = request.GET.get("CompanyID")
    InvoiceID = request.GET.get("InvoiceID")
    VoucherType = request.GET.get("VoucherType")
    print(CompanyID,InvoiceID,VoucherType)
    instance = None
    if user_models.EInvoice.objects.filter(CompanyID__pk=CompanyID,InvoiceID=InvoiceID,VoucherType=VoucherType,is_deleted=False).exists():
        instance = user_models.EInvoice.objects.get(CompanyID__pk=CompanyID,InvoiceID=InvoiceID,VoucherType=VoucherType,is_deleted=False)
        print(instance,'instance')
    context ={
        "instance" : instance,
    }
    return render(request,'users/e_invoice_view.html',context)


@login_required
def delete_e_invoice(request,pk):
    instance = user_models.EInvoice.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status" : "true",
        "icon" : 'warning',
        "title" : "E Invoice deleted",
        "message" : "Successfully deleted",
        "redirect" : "true",
        "redirect_url" : reverse('users:e_invoice_list')
    } 
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def list_user_device_details(request):
    user = request.GET.get("user")
    company = request.GET.get("company")
    user_view = None
    comp_name = None
    try:
        VanId = request.GET.get("VanId")
    except:
        VanId = None
    if web_model.Companies.objects.filter(pk=company).exists():
        comp_name = web_model.Companies.objects.get(pk=company).CompanyName
    if user and company:
        user_view = user_models.UserDeviceDetails.objects.filter(CompanyProductId__CompanyId=company)
    if user and company and VanId:
        user_view = user_models.UserDeviceDetails.objects.filter(CompanyProductId__CompanyId=company,VanId=VanId)
    print(user_view,"##########DDDDDDD")
    context ={
        "user_view" : user_view,
        "userid" : user,
        "company" : company,
        "comp_name" : comp_name 
    }
    return render(request,'users/list_user_device_details.html',context)