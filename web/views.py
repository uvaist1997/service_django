from datetime import datetime, timezone
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
import datetime
import json
from django.contrib.auth import authenticate, login
import datetime
from web import models as web_models
from users import models as user_models
from web import forms as web_forms
from web.functions import generate_form_errors, get_auto_ID, get_auto_id
from main.functions import generate_form_errors_new
from django.contrib.auth.models import User
# from datetime import datetime, timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
# from datetime import timezone
# import datetime
import pandas as pd


@login_required
def create_version(request):
    if request.method == "POST":
        form = web_forms.VersionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)

            version = form.cleaned_data['version']
            status = form.cleaned_data['status']
            if not web_models.Version.objects.filter().exists():
                message = "Version Successfully Created"
                title = "Version Created"
                data.save()
            else:
                web_models.Version.objects.filter().update(version=version, status=status)
                title = "Version Updated"
                message = "Version Successfully Created"
            response_data = {
                "status": "true",
                "title": title,
                "message": message,
                "redirect": "true",
                "redirect_url": reverse('web:create_version')
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        if not web_models.Version.objects.filter().exists():
            instance = None
        else:
            instance = web_models.Version.objects.filter().first()
        form = web_forms.VersionForm(instance=instance)
        context = {
            "form": form,
            "title": "Version",
        }
        return render(request, 'web/create_version.html', context)


# AccountGroup
@login_required
def account_group(request):
    account_view = web_models.AccountGroup.objects.all()
    context = {
        "account_view": account_view,
    }
    return render(request, 'web/accountlist.html', context)


@login_required
def create_account_group(request):
    userid = request.user.id
    today = datetime.date.today()
    if request.method == "POST":
        form = AccountGroupForm(request.POST)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            AccountGroupName = form.cleaned_data['AccountGroupName']
            ParentGroup = form.cleaned_data['ParentGroup']
            Description = form.cleaned_data['Description']
            # ID = form.cleaned_data['ID']
            a.ID = get_auto_ID(AccountGroup)
            a.CreatedUserID = userInstance
            # CreatedDate = form.cleaned_data['CreatedDate']
            a.CreatedDate = today
            a.UpdatedUserID = userInstance
            # UpdatedDate = form.cleaned_data['UpdatedDate']
            a.UpdatedDate = today
            a.Action = "Added"
            a.save()

            AccountGroupLog.objects.create(
                AccountGroupName=AccountGroupName,
                ParentGroup=ParentGroup,
                Description=Description,
                ID=a.ID,
                CreatedUserID=userInstance,
                CreatedDate=a.CreatedDate,
                UpdatedUserID=userInstance,
                UpdatedDate=a.UpdatedDate,
                Action=a.Action,
            )

            response_data = {
                "status": "true",
                "title": "Succesfully submitted",
                "message": "Registration succesfully created",
                "redirect": "true",
                "redirect_url": reverse('web:account_group')

            }
        else:

            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:

        form = AccountGroupForm()
        context = {
            "form": form,
        }
        return render(request, 'web/create_account.html', context)


@login_required
def single_account_group(request, pk):

    instance = get_object_or_404(web_models.AccountGroup.objects.filter(pk=pk))
    context = {
        "instance": instance,
    }
    return render(request, 'web/account.html', context)


@login_required
def edit_account_group(request, pk):
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    single_account_group = web_models.AccountGroup.objects.get(pk=pk)
    ID = single_account_group.ID
    if request.method == "POST":
        form = web_forms.AccountGroupForm(
            request.POST, instance=single_account_group)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)
            AccountGroupName = form.cleaned_data['AccountGroupName']
            ParentGroup = form.cleaned_data['ParentGroup']
            Description = form.cleaned_data['Description']
            # ID = form.cleaned_data['ID']
            # a.CreatedUserID = form.cleaned_data['userInstance']
            # CreatedDate = form.cleaned_data['CreatedDate']
            a.UpdatedUserID = userInstance
            # UpdatedDate = form.cleaned_data['UpdatedDate']
            a.UpdatedDate = today
            a.Action = "Edited"
            form.save()

            AccountGroupLog.objects.create(
                AccountGroupName=AccountGroupName,
                ParentGroup=ParentGroup,
                Description=Description,
                ID=a.ID,
                CreatedUserID=userInstance,
                CreatedDate=today,
                UpdatedUserID=userInstance,
                UpdatedDate=today,
                Action=a.Action,

            )
            form.save()
            response_data = {
                "status": "true",
                "title": "Account group edited",
                "message": "Account Successfully edited",
                "redirect": "true",
                "redirect_url": reverse('web:account_group')
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = AccountGroupForm(instance=single_account_group)
        context = {
            "form": form,
        }
        return render(request, 'web/create_account.html', context)


@login_required
def delete_account_group(request, pk):
    single_account_group = AccountGroup.objects.get(pk=pk)
    if AccountLedger.objects.filter(ParentGroup=single_account_group).exists():
        response_data = {
            "status": "false",
            "icon": "warning",
            "title": "Failed",
            "message": "Account group cant be deleted",
            "redirect": "true",
            "redirect_url": reverse('web:account_group')
        }
    else:
        single_account_group.delete()
        response_data = {
            "status": "true",
            "icon": "warning",
            "title": "Account group deleted",
            "message": "Account group deleted",
            "redirect": "true",
            "redirect_url": reverse('web:account_group')
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# AccountLedger
@login_required
def accountLedger(request):
    userid = request.user.id
    print(request.user.id)
    accountledger_view = web_models.AccountLedger.objects.all()
    context = {
        "accountledger_view": accountledger_view,
    }
    return render(request, 'web/accountlistone.html', context)


@login_required
def CreateAccountLedger(request):
    userid = request.user.id
    today = datetime.date.today()
    if request.method == "POST":
        form = web_forms.AccountLedgerForm(request.POST)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)

            LedgerName = form.cleaned_data['LedgerName']
            ParentGroup = form.cleaned_data['ParentGroup']
            OpeningBalanceType = form.cleaned_data['OpeningBalanceType']
            OpeningBalanceAmount = form.cleaned_data['OpeningBalanceAmount']
            Description = form.cleaned_data['Description']
            # ID = form.cleaned_data['ID']
            a.ID = get_auto_ID(AccountLedger)
            a.CreatedUserID = userInstance
            # CreatedDate = form.cleaned_data['CreatedDate']
            a.CreatedDate = today
            a.UpdatedUserID = userInstance
            # UpdatedDate = form.cleaned_data['UpdatedDate']
            a.UpdatedDate = today
            a.Action = "Added"
            a.save()

            AccountLedgerLog.objects.create(
                LedgerName=LedgerName,
                ParentGroup=ParentGroup,
                OpeningBalanceType=OpeningBalanceType,
                OpeningBalanceAmount=OpeningBalanceAmount,
                Description=Description,
                ID=a.ID,
                CreatedUserID=userInstance,
                # CreatedDate =CreatedDate,
                CreatedDate=a.CreatedDate,
                UpdatedUserID=userInstance,
                # UpdatedDate = UpdatedDate,
                UpdatedDate=a.UpdatedDate,
                Action=a.Action,
            )

            response_data = {
                "status": "true",
                "title": "Succesfully submitted",
                "message": "Registration succesfully created",
                "redirect": "true",
                "redirect_url": reverse('web:accountLedger')

            }
        else:

            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:

        form = web_forms.AccountLedgerForm()
        context = {
            "form": form,
        }
        return render(request, 'web/create_accountone.html', context)


@login_required
def single_account_ledger(request, pk):
    single_account_ledger = web_models.AccountLedger.objects.get(pk=pk)
    context = {
        "instance": single_account_ledger,
    }
    return render(request, 'web/accountone.html', context)


@login_required
def edit_account_ledger(request, pk):
    userid = request.user.id
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc)
    single_account_ledger = web_models.AccountLedger.objects.get(pk=pk)
    if request.method == "POST":
        form = AccountLedgerForm(request.POST, instance=single_account_ledger)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            a = form.save(commit=False)
            LedgerName = form.cleaned_data['LedgerName']
            ParentGroup = form.cleaned_data['ParentGroup']
            OpeningBalanceType = form.cleaned_data['OpeningBalanceType']
            OpeningBalanceAmount = form.cleaned_data['OpeningBalanceAmount']
            Description = form.cleaned_data['Description']
            # UpdatedUserID = userInstance
            # ID = form.cleaned_data['ID']
            # CreatedUserID = form.cleaned_data['CreatedUserID']
            # CreatedDate = form.cleaned_data['CreatedDate']
            a.UpdatedUserID = userInstance
            # UpdatedDate = form.cleaned_data['UpdatedDate']
            a.Action = "Edited"

            AccountLedgerLog.objects.create(
                LedgerName=LedgerName,
                ParentGroup=ParentGroup,
                OpeningBalanceType=OpeningBalanceType,
                OpeningBalanceAmount=OpeningBalanceAmount,
                Description=Description,
                ID=a.ID,
                CreatedUserID=userInstance,
                CreatedDate=today,
                UpdatedUserID=userInstance,
                UpdatedDate=today,
                Action=a.Action,
            )
            form.save()
            response_data = {
                "status": "true",
                "title": "Account ledger edited",
                "message": "Account ledger Successfully edited",
                "redirect": "true",
                "redirect_url": reverse('web:accountLedger')
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = web_forms.AccountLedgerForm(instance=single_account_ledger)
        context = {
            "form": form,
        }
        return render(request, 'web/create_accountone.html', context)


@login_required
def delete_account_ledger(request, pk):
    single_account_ledger = web_models.AccountLedger.objects.get(pk=pk)
    single_account_ledger.delete()
    response_data = {
        "status": "true",
        "icon": "warning",
        "title": "Account ledger deleted",
        "message": "Account ledger deleted",
        "redirect": "true",
        "redirect_url": reverse('web:accountLedger')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# Customer Table
@login_required
def customertable(request):
    print(request.user.id)
    instances = web_models.Register.objects.all()
    customertable_view = web_models.Customer.objects.all()
    context = {
        "customertable_view": customertable_view,
        "instances": instances,
    }
    return render(request, 'web/customers.html', context)


# Companies
@login_required
def companies(request):
    print(request.user.id)
    companies_view = web_models.Companies.objects.all()
    context = {
        "companies_view": companies_view,
    }
    return render(request, 'web/companies.html', context)


@login_required
def create_company(request):

    if request.method == "POST":
        form = web_forms.CompaniesForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(web_models.Companies)
            data.creator = request.user
            data.updater = request.user
            business_type = form.cleaned_data['business_type']
            CompanyName = form.cleaned_data['CompanyName']
            Country = form.cleaned_data['Country']
            State = form.cleaned_data['State']
            OfficePhoneNumber = form.cleaned_data['OfficePhoneNumber']
            Email = form.cleaned_data['Email']
            data.Action = "A"
            data.user = request.user
            data.business_type = business_type
            data.save()

            web_models.CompaniesLog.objects.create(
                user=request.user,
                Companyid=data.auto_id,
                auto_id=data.auto_id,
                creator=request.user,
                updater=request.user,
                business_type=business_type,
                Country=Country,
                State=State,
                OfficePhoneNumber=OfficePhoneNumber,
                Email=Email,
                Action="A",
            )

            response_data = {
                "status": "true",
                "title": "Succesfully submitted",
                "message": "Registration succesfully created",
                "redirect": "true",
                "redirect_url": reverse('web:companies')

            }
        else:

            message = generate_form_errors_new(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:

        form = web_forms.CompaniesForm()
        context = {
            "form": form,
        }
        return render(request, 'web/create_company.html', context)


@login_required
def single_company(request, pk):
    SingleCompanies = web_models.Companies.objects.get(pk=pk)
    context = {
        "instance": SingleCompanies,
    }
    return render(request, 'web/company.html', context)


@login_required
def edit_company(request, pk):
    # today = datetime.datetime.now(timezone.utc)
    SingleCompanies = web_models.Companies.objects.get(pk=pk)
    if request.method == "POST":
        form = web_forms.CompaniesForm(request.POST, instance=SingleCompanies)
        if form.is_valid():
            data = form.save(commit=False)
            # a.ID = get_auto_ID(web_models.Companies)
            data.creator = request.user
            data.updater = request.user
            CompanyName = form.cleaned_data['CompanyName']
            Country = form.cleaned_data['Country']
            State = form.cleaned_data['State']
            OfficePhoneNumber = form.cleaned_data['OfficePhoneNumber']
            business_type = form.cleaned_data['business_type']

            data.Action = "M"
            data.save()

            web_models.CompaniesLog.objects.create(
                user=request.user,
                Companyid=data.auto_id,
                auto_id=get_auto_id(web_models.CompaniesLog),
                creator=request.user,
                updater=request.user,
                business_type=business_type,
                Country=Country,
                State=State,
                OfficePhoneNumber=OfficePhoneNumber,
                Email=data.Email,
                Action="M",
            )
            form.save()
            response_data = {
                "status": "true",
                "title": "companies edited",
                "message": "companies Successfully edited",
                "redirect": "true",
                "redirect_url": reverse('web:companies')
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = web_forms.CompaniesForm(instance=SingleCompanies)
        context = {
            "form": form,
        }
        return render(request, 'web/create_company.html', context)


@login_required
def delete_company(request, pk):
    SingleCompanies = web_models.Companies.objects.get(pk=pk)
    SingleCompanies.delete()
    response_data = {
        "status": "true",
        "icon": "warning",
        "title": "Companies deleted",
        "message": "Companies deleted",
        "redirect": "true",
        "redirect_url": reverse('web:companies')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def company_products(request):
    print("@@@@@@@@@@@@@@@@@@!!!!!!!!!",request.user.id)
    companyproduct_view = web_models.CompanyProduct.objects.all()
    query = request.GET.get("q")
    if query:
        companyproduct_view = companyproduct_view.filter(
            Q(CompanyId__CompanyName__icontains=query) | Q(CompanyId__user__username__icontains=query))
    context = {
        "companyproduct_view": companyproduct_view,
    }
    return render(request, 'web/company_products.html', context)


@login_required
def export_company_products(request):
    # companyproduct_view = web_models.CompanyProduct.objects.all()
    # query = request.GET.get("q")
    # if query:
    #     companyproduct_view = companyproduct_view.filter(
    #         Q(CompanyId__CompanyName__icontains=query) | Q(CompanyId__user__username__icontains=query))
    dic = {}
    cursor = connection.cursor()
    cursor.execute('''
              SELECT               
                "id",
                "date_added",
                (SELECT NULLIF("username", '') FROM public."auth_user" AS C WHERE C."id" = "creator_id"   ) AS Username,
                (SELECT NULLIF("CompanyName", '') FROM public."web_companies" AS C WHERE C."id" = "CompanyId_id"   ) AS CompanyName,
                (SELECT NULLIF("Name", '') FROM public."products" AS P WHERE P."id" = "ProductId_id"   ) AS ProductName,

                (SELECT NULLIF("Country", '') FROM public."web_companies" AS C WHERE C."id" = "CompanyId_id"   ) AS Country,
                (SELECT NULLIF("State", '') FROM public."web_companies" AS C WHERE C."id" = "CompanyId_id"   ) AS State,
                (SELECT NULLIF("OfficePhoneNumber",0) FROM public."web_companies" AS C WHERE C."id" = "CompanyId_id"   ) AS OfficePhoneNumber,
                (SELECT NULLIF("Email", '') FROM public."web_companies" AS C WHERE C."id" = "CompanyId_id"   ) AS Email,

                "No_ofDevice",
                "IsTrialVersion",
                "Action",
                (SELECT NULLIF("Name", '') FROM public."software_plans" AS S WHERE S."id" = "software_plan_id"   ) AS PlanName,
                "ProductExpiryDate",
                "AMCActive",
                "AMCExpiry",
                "service_date",
                "service"
                FROM public."web_company_product"     
                   
        ''', dic)
    response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    response["Content-Disposition"] = 'attachment; filename="{}.xlsx"'.format(
            "Companies"
        )
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    df.columns = [
            'id','date_added','Creator','CompanyName'
            , 'ProductName'
            , 'Country'
            , 'State'
            , 'OfficePhoneNumber'
            , 'Email'
            ,'No_ofDevice','IsTrialVersion','Action','PlanName','ProductExpiryDate','AMCActive','AMCExpiry','service_date','service']
    # df['ProductExpiryDate'] = df['ProductExpiryDate'].dt.tz_localize(None)
    df['ProductExpiryDate'] = df['ProductExpiryDate'].dt.date
    df['AMCActive'] = df['AMCActive'].dt.date
    df['AMCExpiry'] = df['AMCExpiry'].dt.date
    df['service_date'] = df['service_date'].dt.date
    df['date_added'] = df['date_added'].dt.date
   
    # df['ProductExpiryDate'] = df['ProductExpiryDate'].dt.tz_localize(None)
    # df['AMCActive'] = df['AMCActive'].dt.tz_localize(None)
    # df['AMCExpiry'] = df['AMCExpiry'].dt.tz_localize(None)
    # df['service_date'] = df['service_date'].dt.tz_localize(None)
    # df['date_added'] = df['date_added'].dt.tz_localize(None)
    # df['date_updated'] = df['date_updated'].dt.tz_localize(None)
    
    df.to_excel(response,index=False)
    return response


@login_required
def create_company_product(request):
    userid = request.user.id
    today = datetime.date.today()
    if request.method == "POST":
        form = web_forms.CompanyProductForm(request.POST)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            data = form.save(commit=False)
            # a.ID = get_auto_ID(CompanyProducts)
            CompanyId = form.cleaned_data['CompanyId']
            ProductId = form.cleaned_data['ProductId']
            No_ofDevice = form.cleaned_data['No_ofDevice']
            ProductExpiryDate = form.cleaned_data['ProductExpiryDate']
            AMCActive = form.cleaned_data['AMCActive']
            AMCExpiry = form.cleaned_data['AMCExpiry']
            IsTrialVersion = form.cleaned_data['IsTrialVersion']

            data.Action = "A"
            data.save()

            web_models.CompanyProductLog.objects.create(
                CompanyProductId=data.auto_id,
                creator=request.user,
                updater=request.user,
                auto_id=get_auto_id(web_models.CompanyProductLog),
                CompanyId=CompanyId,
                ProductId=ProductId,
                No_ofDevice=No_ofDevice,
                ProductExpiryDate=ProductExpiryDate,
                AMCActive=AMCActive,
                AMCExpiry=AMCExpiry,
                IsTrialVersion=IsTrialVersion,
                Action="A",
            )

            response_data = {
                "status": "true",
                "title": "Succesfully submitted",
                "message": "Registration succesfully created",
                "redirect": "true",
                "redirect_url": reverse('web:company_products')

            }
        else:

            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:

        form = web_forms.CompanyProductForm()
        context = {
            "form": form,
            "is_edit": False

        }
        return render(request, 'web/create_company_product.html', context)


@login_required
def single_company_product(request, pk):
    instance = get_object_or_404(
        web_models.CompanyProduct.objects.filter(pk=pk))
    context = {
        "instance": instance,
    }
    return render(request, 'web/single_company_product.html', context)


@login_required
def edit_company_product(request, pk):
    # today = datetime.now(timezone.utc)
    instance = get_object_or_404(
        web_models.CompanyProduct.objects.filter(pk=pk))
    if request.method == "POST":
        form = web_forms.CompanyProductForm(request.POST, instance=instance)

        if form.is_valid():
            CompanyId = form.cleaned_data['CompanyId']
            ProductId = form.cleaned_data['ProductId']
            No_ofDevice = form.cleaned_data['No_ofDevice']
            ProductExpiryDate = form.cleaned_data['ProductExpiryDate']
            AMCActive = form.cleaned_data['AMCActive']
            AMCExpiry = form.cleaned_data['AMCExpiry']
            IsTrialVersion = form.cleaned_data['IsTrialVersion']
            data = form.save(commit=False)
            data.updater = request.user
            data.date_updated = datetime.datetime.now()

            data.Action = "M"
            data.save()

            web_models.CompanyProductLog.objects.create(
                CompanyProductId=data.auto_id,
                creator=request.user,
                updater=request.user,
                auto_id=get_auto_id(web_models.CompanyProductLog),
                CompanyId=CompanyId,
                ProductId=ProductId,
                No_ofDevice=No_ofDevice,
                ProductExpiryDate=ProductExpiryDate,
                AMCActive=AMCActive,
                AMCExpiry=AMCExpiry,
                IsTrialVersion=IsTrialVersion,
                Action="M",
            )
            response_data = {
                "status": "true",
                "title": "company product edited",
                "message": "company products Successfully edited",
                "redirect": "true",
                "redirect_url": reverse('web:company_products')
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = web_forms.CompanyProductForm(instance=instance)
        device_instances = web_models.CompanyDevices.objects.filter(
            CompanyProductId=instance)
        context = {
            "form": form,
            "is_edit": True,
            "instance": instance,
            "device_instances": device_instances,
        }
        return render(request, 'web/create_company_product.html', context)


@login_required
def exp_date_is_trail_company_device(request, pk):
    instance = get_object_or_404(
        web_models.CompanyProduct.objects.filter(pk=pk))
    device_instances = web_models.CompanyDevices.objects.filter(
        CompanyProductId=instance)
    for i in device_instances:
        i.IsTrialVersion = instance.IsTrialVersion
        i.ProductExpiryDate = instance.ProductExpiryDate
        i.save()

    response_data = {
        "status": "true",
        "icon": 'warning',
        "title": "Company Device",
        "message": "Device Successfully Updated",
        "redirect": "true",
        "redirect_url": reverse('web:company_products')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def delete_company_product(request, pk):
    instance = web_models.CompanyProduct.objects.get(pk=pk)
    username = request.GET.get('username')
    password = request.GET.get('password')
    print(instance.ProductId, "INSTANCE", username)
    print(instance.ProductId, "INSTANCE", password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if instance.ProductId.Name == 'Van Sale Product':
            if web_models.SaleMaster.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.SaleMaster.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    details = web_models.SaleDetails.objects.filter(SaleId=i)
                    for j in details:
                        j.delete()
                    i.delete()
                print(instance, "SALEMASTER")

            if web_models.SaleOrder.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.SaleOrder.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    details = web_models.SaleOrderDetails.objects.filter(
                        SaleOrderId=i)
                    for j in details:
                        j.delete()
                    i.delete()
                print(instance, "SaleOrder")

            if web_models.SaleProduct.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.SaleProduct.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "SaleProduct")

            if web_models.SalePrice.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.SalePrice.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "SalePrice")

            if web_models.SaleAccountLedger.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.SaleAccountLedger.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "SaleAccountLedger")

            if web_models.WarehouseStock.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.WarehouseStock.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "WarehouseStock")

            if web_models.ExpenseLedger.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.ExpenseLedger.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "ExpenseLedger")

            if web_models.LastSalesPrice.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.LastSalesPrice.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "LastSalesPrice")

            if web_models.SaleRoute.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.SaleRoute.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "SaleRoute")

            if web_models.TransactionType.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.TransactionType.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "TransactionType")

            if web_models.VanRoute.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.VanRoute.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "VanRoute")

            if web_models.SaleReturnMaster.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.SaleReturnMaster.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    details = web_models.SaleReturnDetails.objects.filter(
                        SaleReturnMasterId=i)
                    for j in details:
                        j.delete()
                    i.delete()
                print(instance, "SaleReturnMaster")

            if web_models.BillWise.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.BillWise.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "BillWise")

            if web_models.Reciept.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.Reciept.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    details = web_models.RecieptDetail.objects.filter(
                        RecieptId=i)
                    for j in details:
                        j.delete()
                    i.delete()
                print(instance, "Reciept")

            if web_models.Payment.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.Payment.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    details = web_models.PaymentDetail.objects.filter(
                        PaymentId=i)
                    for j in details:
                        j.delete()
                    i.delete()
                print(instance, "Payment")

            if web_models.VanSettings.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.VanSettings.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "VanSettings")

            if web_models.TaxCategory.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.TaxCategory.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "TaxCategory")

            if web_models.CompanyDevices.objects.filter(CompanyProductId=instance).exists():
                instances = web_models.CompanyDevices.objects.filter(
                    CompanyProductId=instance)
                for i in instances:
                    i.delete()
                print(instance, "CompanyDevices")

        instance.delete()
        response_data = {
            "status": "true",
            "icon": "warning",
            "title": "Company Product",
            "message": "Successfully deleted",
            "redirect": "true",
            "redirect_url": reverse('web:company_products')
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "type": "warning",
            "title": "error",
            "message": "username or password incorrect",
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

# Company Devices


@login_required
def company_devices(request):
    instances = web_models.CompanyDevices.objects.filter()
    query = request.GET.get("q")
    print("ssssssssssss", query, instances)
    if query:
        instances = instances.filter(
            Q(CompanyProductId__CompanyId__CompanyName__icontains=query))
        print(instances, "Ullil")
    context = {
        "instances": instances,
    }
    return render(request, 'web/company_devices.html', context)


@login_required
def create_company_devices(request):
    userid = request.user.id
    today = datetime.date.today()
    if request.method == "POST":
        form = web_forms.CompanyDeviceForm(request.POST)
        userInstance = User.objects.get(id=userid)
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_ID(web_models.CompanyDevices)
            CompanyProudctID = form.cleaned_data['CompanyProudctID']
            DeviceCode = form.cleaned_data['DeviceCode']
            Type = form.cleaned_data['Type']
            data.Action = "A"
            data.save()

            web_model.CompanyDevicesLog.objects.create(
                auto_id=get_auto_id(web_model.CompanyDevices),
                creator=request.user,
                updater=request.user,
                CompanyProductId=CompanyProductId,
                DeviceName=DeviceName,
                DeviceCode=DeviceCode,
                Type=Type,

                Action="A",

            )

            response_data = {
                "status": "true",
                "title": "Succesfully submitted",
                "message": "Registration succesfully created",
                "redirect": "true",
                "redirect_url": reverse('web:companydevices')

            }
        else:

            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:

        form = CompanyDeviceForm()
        context = {
            "form": form,
        }
        return render(request, 'web/create_company_devices.html', context)


@login_required
def company_device(request, pk):
    instance = get_object_or_404(
        web_models.CompanyDevices.objects.filter(pk=pk))
    context = {
        "instance": instance,
    }
    return render(request, 'web/company_device.html', context)


@login_required
def edit_company_devices(request, pk):

    # today = datetime.datetime.now(timezone.utc)
    instance = web_models.CompanyDevices.objects.get(pk=pk)
    if request.method == "POST":
        form = web_forms.CompanyDeviceForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            # data.auto_id = get_auto_id(web_models.CompanyDevices)
            CompanyProductId = form.cleaned_data['CompanyProductId']
            DeviceCode = form.cleaned_data['DeviceCode']
            DeviceName = form.cleaned_data['DeviceName']
            Type = form.cleaned_data['Type']
            data.updater = request.user
            data.date_updated = datetime.datetime.now()
            data.Action = "M"
            data.save()

            print("HALOOOOOOIIIIIII")
            web_models.CompanyDevicesLog.objects.create(
                auto_id=get_auto_id(web_models.CompanyDevicesLog),
                creator=request.user,
                updater=request.user,
                CompanyProductId=CompanyProductId,
                DeviceName=DeviceName,
                DeviceCode=DeviceCode,
                Type=Type,

                Action="A",

            )
            response_data = {
                "status": "true",
                "title": "company product edited",
                "message": "company products Successfully edited",
                "redirect": "true",
                "redirect_url": reverse('web:company_devices')
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = web_forms.CompanyDeviceForm(instance=instance)
        context = {
            "form": form,
        }
        return render(request, 'web/create_company_devices.html', context)


@login_required
def delete_company_devices(request, pk):
    SingleCompanyDevices = web_models.CompanyDevices.objects.get(pk=pk)
    SingleCompanyDevices.delete()
    response_data = {
        "status": "true",
        "icon": "warning",
        "title": "Company device deleted",
        "message": "Company device deleted",
        # "redirect" : "true",
        # "redirect_url" : reverse('web:companydevices')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


#########REGISTER#############
@login_required
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        form = RegisterForm(request.POST)
        userid = request.user.id
        today = datetime.date.today()
        userInstance = User.objects.get(id=userid)
        if form.is_valid() and form.is_valid():
            data = form.save(commit=False)
            data.ID = get_auto_id(Register)
            username_test = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            data.CreatedUserID = userInstance
            data.UpdatedUserID = userInstance
            data.CreatedDate = today
            data.UpdatedDate = today

            # user_aaa = User.objects.create_user(
            #     username = username_test,
            #     first_name = first_name,
            #     last_name = last_name,
            #     email = email,
            #     password = password1,
            #     )
            # data =form.save(commit=False)
            data.first_name = first_name
            data.last_name = last_name
            data.save()
            print(data.pk, 'haloooooi')

            data1 = form.save(commit=False)
            data1.user = data
            data1.save()

            response_data = {
                'status': 'true',
                'title': "form submitted",
                'redirect': 'true',
                'message': "form submitted Successfully",

            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": str(message)
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = UserForm()
        reg_form = RegisterForm()
        context = {
            "form": form,
            "reg_form": reg_form,
        }
        return render(request, 'registration/registration_form.html', context)


# company_list
@login_required
def company_list(request):
    user_instance = User.objects.filter(is_superuser=False)
    context = {
        "user_instance": user_instance,
    }
    return render(request, 'reports/company_list.html', context)


# company_device_list
@login_required
def company_device_list(request):
    company_instance = web_models.Companies.objects.filter()
    context = {
        "company_instance": company_instance,
    }
    return render(request, 'reports/company_device_list.html', context)


@login_required
def get_company_list(request):
    user_id = request.GET.get('id')
    TrialVersion_True = request.GET.get('TrialVersion_True')
    TrialVersion_False = request.GET.get('TrialVersion_False')
    is_type = request.GET.get('type')
    print(user_id, 'user_id')
    # ==================================
    if user_id:
        # ====
        if user_id and is_type and is_type == "----" and TrialVersion_True == "true":
            print("FIRST111111..........")
            company_ids = web_models.CompanyDevices.objects.filter(
                CompanyProductId__CompanyId__user=user_id, IsTrialVersion=True).values_list('CompanyProductId__CompanyId', flat=True)
            instances = web_models.Companies.objects.filter(
                is_deleted=False, pk__in=company_ids)
        elif user_id and is_type and is_type == "----" and TrialVersion_False == "true":
            print("SECOND2222222..........")
            company_ids = web_models.CompanyDevices.objects.filter(
                CompanyProductId__CompanyId__user=user_id, IsTrialVersion=False).values_list('CompanyProductId__CompanyId', flat=True)
            instances = web_models.Companies.objects.filter(
                is_deleted=False, pk__in=company_ids)
        # =====
        elif user_id and is_type and is_type != "----" and TrialVersion_True == "true":
            print("FIRST..........")
            company_ids = web_models.CompanyDevices.objects.filter(
                CompanyProductId__CompanyId__user=user_id, Type=is_type, IsTrialVersion=True).values_list('CompanyProductId__CompanyId', flat=True)
            instances = web_models.Companies.objects.filter(
                is_deleted=False, pk__in=company_ids)
        elif user_id and is_type and is_type != "----" and TrialVersion_False == "true":
            print("SECOND..........")
            company_ids = web_models.CompanyDevices.objects.filter(
                CompanyProductId__CompanyId__user=user_id, Type=is_type, IsTrialVersion=False).values_list('CompanyProductId__CompanyId', flat=True)
            instances = web_models.Companies.objects.filter(
                is_deleted=False, pk__in=company_ids)
        elif user_id and is_type and is_type != "----":
            print("THIRD..........")
            company_ids = web_models.CompanyDevices.objects.filter(
                CompanyProductId__CompanyId__user=user_id, Type=is_type).values_list('CompanyProductId__CompanyId', flat=True)
            instances = web_models.Companies.objects.filter(
                is_deleted=False, pk__in=company_ids)
        elif user_id:
            print("FOURTH..........")
            instances = web_models.Companies.objects.filter(
                is_deleted=False, user=user_id)
    # ===================================
        cust_arr = []
        data_arr = []
        for i in instances:
            company_dic = {
                "id": str(i.pk),
                "name": str(i.CompanyName),
                "type": str(i.business_type),
                "email": str(i.Email),
            }

            data_arr.append(company_dic)
        template_name = 'reports/includes/company_list.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if instances:
            context = {
                'instances': instances,
            }
            html_content = render_to_string(template_name, context)
            response_data = {
                "status": "true",
                'comapny_list': html_content,
            }
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
def delete_company_list(request, pk):
    instance = web_models.Companies.objects.get(pk=pk)
    instance.delete()
    response_data = {
        "status": "true",
        "icon": "warning",
        "title": "Company deleted",
        "message": "Successfully deleted",
        "redirect": "true",
        "redirect_url": reverse('web:company_list')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def get_company_device_list(request):
    company_id = request.GET.get('id')
    print(company_id, 'company_id')

    if company_id:
        instances = web_models.CompanyDevices.objects.filter(
            is_deleted=False, CompanyProductId__CompanyId=company_id)
        product_instances = web_models.CompanyProduct.objects.filter(
            is_deleted=False, CompanyId=company_id)
        template_name = 'reports/includes/company_device_list.html'
        template_name1 = 'reports/includes/company_product_list.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if instances:
            context = {
                'instances': instances,
                'product_instances': product_instances,
            }
            html_content = render_to_string(template_name, context)
            html_content1 = render_to_string(template_name1, context)
            response_data = {
                "status": "true",
                'device_list': html_content,
                'product_list': html_content1,
            }
        else:
            response_data = {
                "status": "false",
                "message": "Company not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Devices not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def get_company_device(request):
    divice_id = request.GET.get('id')
    print(divice_id, 'company_id')

    if divice_id:
        if web_models.CompanyDevices.objects.filter(is_deleted=False, pk=divice_id).exists():
            instance = web_models.CompanyDevices.objects.get(
                is_deleted=False, pk=divice_id)

            response_data = {
                "status": "true",
                "ProductExpiryDate": str(instance.ProductExpiryDate),
                "IsTrialVersion": instance.IsTrialVersion,

            }
        else:
            response_data = {
                "status": "false",
                "message": "Company Devices not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Devices not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def get_update_company_device(request):
    print("OOOOOOOOIIIIIIII")
    divice_id = request.GET.get('id')
    date = request.GET.get('date')
    is_trail = request.GET.get('is_trail')
    print(date, is_trail)

    if divice_id:
        if web_models.CompanyDevices.objects.filter(is_deleted=False, pk=divice_id).exists():
            instance = web_models.CompanyDevices.objects.get(
                is_deleted=False, pk=divice_id)
            if date:
                date_dt3 = datetime.datetime.strptime(date, '%Y-%m-%d')
                instance.ProductExpiryDate = date_dt3
            if is_trail:
                if is_trail == "true":
                    print("TRUEEE")
                    instance.IsTrialVersion = True
                else:
                    print("False.....")
                    instance.IsTrialVersion = False

            instance.save()
            print(instance.ProductExpiryDate)
            response_data = {
                "status": "true",


            }
        else:
            response_data = {
                "status": "false",
                "message": "Company Devices not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "Devices not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# company_list
@login_required
def activity_logs(request):
    company_instances = web_models.Companies.objects.filter(is_deleted=False)
    context = {
        "company_instances": company_instances,
    }
    return render(request, 'reports/activity_logs.html', context)


@login_required
def get_activity_logs(request):
    pk = request.GET.get('id')

    print(pk)
    CompanyId = []
    if pk:
        if web_models.Companies.objects.filter(is_deleted=False, pk=pk).exists():
            CompanyId.append(web_models.Companies.objects.get(
            is_deleted=False, pk=pk).pk)
        # comp_product = web_models.CompanyProduct.objects.filter(
        #     is_deleted=False, CompanyId__id=pk).values_list('id',flat=True)
        comp_product = web_models.CompanyProduct.objects.filter(
            is_deleted=False, CompanyId__id=pk)
        if comp_product:
            CompanyId = []
            for i in comp_product:
                print(i.id)
                CompanyId .append(str(i.pk)+str("CompanyProductId"))
        
        print(CompanyId)
        instances = user_models.ActivityLog.objects.filter(CompanyId__in=CompanyId)
        print(instances)

        data_arr = []
        for i in instances:
            company_dic = {
                "id": str(i.pk),
                "log_type": str(i.log_type),
                "date": str(i.date),
                "time": str(i.time),
                "message": str(i.message),
                "description": str(i.description),
            }

            data_arr.append(company_dic)
            print(data_arr, 'data_arr')
        template_name = 'reports/includes/activity_log_list.html'
        # instances = transaction_models.Token.objects.filter(is_deleted=False,AgentID=agent_id,Date=date)
        if instances:
            context = {
                'instances': instances,
            }
            html_content = render_to_string(template_name, context)
            response_data = {
                "status": "true",
                'comapny_list': html_content,
            }
        else:
            response_data = {
                "status": "false",
                "message": "not found"
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        response_data = {
            "status": "false",
            "message": "not found"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
