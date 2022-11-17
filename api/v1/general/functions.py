from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from web import models as web_model
from json import loads,dumps

def generate_serializer_errors(args):
	message = ""
	for key, values in args.iteritems():
		error_message = ""
		for value in values:
			error_message += value + ","
		error_message = error_message[:-1]

		message += "%s : %s | " %(key,error_message)
	return message[:-3]


def get_current_role(cls):
	current_role = "user" 

	if cls.user.is_authenticated:           
		roles = list(set([x.name for x in cls.user.groups.all()]))
		if cls.user.is_superuser:
			current_role = "superuser"
		elif 'delivery_agent' in roles:
				current_role = 'delivery_agent'
		elif 'customer_user' in roles:
				current_role = 'customer_user'
					
	return current_role


def call_paginator_all(model_object, page_number, items_per_page):
	paginator = Paginator(model_object, items_per_page)
	content = paginator.page(page_number)
	return content


def list_pagination(list_value, items_per_page, page_no):
	paginator_object = Paginator(list_value, items_per_page)
	get_value = paginator_object.page(page_no).object_list
	return get_value


def get_auto_id(Model):
	auto_id = 1
	print(Model,"get_auto_id")
	latest_auto_id =  Model.objects.all().order_by("-date_added")[:1]
	if latest_auto_id:
		for auto in latest_auto_id:
			auto_id = auto.auto_id + 1
	return auto_id


def get_instance(pk,model):
	instance = None
	if model.objects.filter(is_deleted=False,pk=pk).exists():
		instance = get_object_or_404(model.objects.filter(is_deleted=False,pk=pk))
	return instance


def convertOrderdDict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


def bulkCreate(instances_arr,companyproduct_ins,request,model):
	model.objects.bulk_create([
        model(
        **{key:value for key, value in i.items()},
        creator=request.user,
		updater=request.user,
		CompanyProductId=companyproduct_ins,
        )
        for i in instances_arr
    ])

	