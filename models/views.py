from django.shortcuts import render
import datetime

# Create your views here.

from .models import Week, Environment, Month

month_name_dict = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June',
                    '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}
month_code_dict = {'1':'JAN', '2':'FEB', '3':'MAR', '4':'APR', '5':'MAY', '6':'JUN',
                    '7':'JUL', '8':'AUG', '9':'SEP', '10':'OCT', '11':'NOV', '12':'DEC'}

def placeholder(request):
    pass

def setup_week(request):
    #start 1/1/2017
    now = datetime.datetime.now()
    year = now.year
    ser = Week.objects.filter(year__contains=year)
    if not ser:
        for x in range(0,53):
            wk = str(year)+'-W'+str(x)
            fst_day1 = datetime.datetime.strptime(wk + '-0', "%Y-W%U-%w")
            fst_day = fst_day1.day
            week_name = "Week of "+month_code_dict[str(fst_day1.month)]+' '+str(fst_day)
            obj = Week(week_num=x, year=year, week_name=week_name)
            obj.save()

    return render(request, 'status/blank.html')

def setup_environment(request, tog):

    if tog == 1:
        env = Environment.objects.all()
        env.delete()

    envs = ['RMM', 'Continuity', 'HelpDesk', 'NOC', 'SOC','Boston', 'Cranberry (non-HelpDesk)', 'Houston', 'Mumbai (non-NOC)', 'Pune (non-SOC)', 'London', 'Sydney', 'Markley (Internal)' ]
    servs = ['Internet', 'Firewall', 'VPN', 'Wifi', 'Phones', 'Conference Room', 'VMware Engineering Environment', 'Applications']
    sev = [1,2,3,4,5]

    if len(Environment.objects.all()) == 0 or tog == 1:
        for e in envs:
            for s in servs:
                for se in sev:
                    obj = Environment(env=e, service=s, sev=se)
                    obj.save()

    return render(request, 'status/blank.html')

def setup_month(request):
    #start 1/17
    now = datetime.datetime.now()
    year = now.year
    ser = Month.objects.filter(year__contains=year)
    if not ser:
        for x in range(1,13):
            month_name = month_name_dict[str(x)]
            month_code = month_code_dict[str(x)]
            obj = Month(month_num=x, month_name=month_name, month_code=month_code, year=year)
            obj.save()

    return render(request, 'status/blank.html')
