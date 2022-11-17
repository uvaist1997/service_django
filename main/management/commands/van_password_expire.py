from django.shortcuts import render, get_object_or_404
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import datetime
from main.functions import is_password_expired
from web.models import VanPassword
import time


# StartTime=time.time()


class Command(BaseCommand):

    def handle(self, *args, **options):

        today = datetime.datetime.today()
        instances = VanPassword.objects.filter(
            is_expired=False)
        for instance in instances:
            is_expired = is_password_expired(instance.time_str)
            print(instance.is_expired, is_expired)
            if is_expired:
                instance.is_expired = True
                instance.save()
