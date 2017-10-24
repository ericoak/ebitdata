from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import psycopg2
import datetime
import acc_keys as ac
import pytz
from django.utils import timezone

from models.models import Week, Environment, Month, Uptime_Week
from .models import Script
# Create your views here.
from .models import Script

def status(request):
    sta = Script.objects.all()
    context = {'scripts': sta}
    return render(request, 'status/status.html', context)

def blank(request):
    return render(request, 'status/blank.html')
