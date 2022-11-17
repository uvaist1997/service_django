from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.http import require_GET
from django.core import serializers
from django.contrib.auth.models import Group
from django.db.models import Sum, Q
import datetime
import re
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def app(request):
    return HttpResponseRedirect(reverse('dashboard'))


@login_required
def dashboard(request):

    context = {
        "title": "Dashboard",
    }
    return render(request, "dashboard.html", context)
