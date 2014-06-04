# coding=utf-8

from django.contrib.auth.models import User
from physical.models import UserActivityLog
from datetime import date, datetime, time, timedelta
import time
import shlex
import subprocess
import os
#Get users with at least 1 log in the last week.
#Generate the image.
#sleep (5 secs) 
#get the image path
#get the template
#email the template to the user

from xvfbwrapper import Xvfb




def url_screengrab(user_id, **kwargs):
    
    user_id = int(user_id)
    #cmd = '''export DISPLAY=:0;/usr/local/bin/CutyCapt --url=http://datadonors.org/reports/user/physical/{u}/  --out=/home/datadonor/static/tmp/physical_report_{u}.png '''.format(u = user_id)
    #vdisplay = Xvfb()
    #vdisplay.start()
    #cmd = '''export DISPLAY=:0
    #        /usr/local/bin/CutyCapt --url=http://datadonors.org/reports/user/physical/{u}/ --out=/home/datadonor/static/tmp/physical_report_{u}.png'''.format(u=user_id)
    #proc = subprocess.Popen(shlex.split(cmd))
    #proc.communicate()
    #vdisplay.stop()
    #os.system("export DISPLAY=:0")
    cmd = "export DISPLAY=:0;/usr/local/bin/CutyCapt --url=http://datadonors.org/reports/user/physical/{u}/  --out=/home/datadonor/static/tmp/physical_report_{u}.png".format(u = user_id)
    os.system(cmd)
    

def physical_weekly_report():
    today = date.today()
    last_sunday = today - timedelta(days=6)
    users = UserActivityLog.objects.filter(execute_time__range=(last_sunday, today), \
                                           type__in=["walking", "running", "cycling"]).\
                                           values_list('user', flat=True).distinct()
                                           
    
    for user in users:
        url_screengrab(user)
        
        