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


all_outage_sql = """SELECT * FROM outage_outage as oo
                    LEFT OUTER JOIN outage_environment as oe
                    ON oo.environ_id = oe.id
                    LEFT OUTER JOIN outage_service as os
                    ON oo.service_id = os.id
                    LEFT OUTER JOIN outage_severity as osev
                    ON oo.sev_id = osev.id
                    """

class UptimeObj():
    def __init__(self, wk, env, rows):
        self.wk = wk
        self.envi = env
        self.out_rows = rows
        self.now = datetime.datetime.now()
        #self.now = timezone.now()
        utc = pytz.UTC

        self.cur_wk = datetime.date(self.now.year, self.now.month, self.now.day).strftime("%U")
        self.wk_start = datetime.datetime.strptime('2017-W'+ str(self.cur_wk) + '-0', "%Y-W%U-%w")
        self.wk_end = datetime.datetime.strptime('2017-W'+ str(self.cur_wk)  + '-6', "%Y-W%U-%w")

        self.wk_start = utc.localize(self.wk_start)
        self.wk_end = utc.localize(self.wk_end)

        self.out_list = []
        self.duration = 0

        #search for outages in the week
        for r in self.out_rows:
            if r[2] > self.wk_start and r[4] < self.wk_end and r[14]+r[17]+r[20]:
                self.out_list.append(r)

    def calc_uptime(self):
        self.uptime = ((10080 - self.duration)/10080)

    def calc_duration(self):
        for r in self.out_list:
            self.duration = self.duration + (r[4] - r[2])

    def calc_mttr(self):
        if self.count != 0:
            self.mttr = self.duration / self.count
        else:
            self.mttr = 0

    def calc_count(self):
        self.count = len(self.out_list)

    def calc(self):
        self.calc_duration()
        self.calc_count()
        self.calc_uptime()
        self.calc_mttr()

def placeholder(request):
    pass

def connect_db(name):
    if name == 'spat':
        conn = psycopg2.connect(ac.spat_name())
        x = conn.cursor()
        return x

def pull_data_spat(sql):
    spat_cur = connect_db('spat')
    spat_cur.execute(sql)
    rows = spat_cur.fetchall()
    return rows

def outage_crawler(request):
    now = datetime.datetime.now()
    o_data = pull_data_spat(all_outage_sql)
    #first item of first sql statement
    #print(o_data[0][14]+o_data[0][17]+str(o_data[0][20]))

    weeks = Week.objects.all()
    envr = Environment.objects.all()
    cur_wk = int(datetime.date(now.year, now.month, now.day).strftime("%U"))

    #for each week
    for w in weeks:
        up = Uptime_Week.objects.filter(week_num=w)
        if up or w.week_num > cur_wk or w.year > now.year:
            continue
        #and each Environment
        for e in envr:
            #initiate uptime object
            up_obj = UptimeObj(w, e, o_data)
            up_obj.calc()
            up = Uptime_Week(week_num=w, env=e, uptime=up_obj.uptime, duration=up_obj.duration, mttr=up_obj.mttr, count=up_obj.count)
            up.save()

    return HttpResponseRedirect(reverse('status:status'))