# coding=utf-8

from django.contrib.auth.models import User
from physical.models import UserActivityLog
from datetime import date, datetime, time, timedelta
import time
import shlex
import subprocess
import os
from utils.commons import send_email_report
from users.models import Profile
from xvfbwrapper import Xvfb


def url_screengrab(user_id, **kwargs):
    cmd = "export DISPLAY=:0;/usr/local/bin/CutyCapt --url=http://datadonors.org/reports/user/full/{u}/  --out=/home/datadonor/static/tmp/report_{u}.png".format(u = user_id)
    os.system(cmd)
    

def user_weekly_report():
    
    emails = User.objects.all()
    for user in users:
        user = int(user)
        user_obj= User.objects.get(id=user)
        if user_obj.profile.email:
            url_screengrab(user)
            image = "report_{u}.png".format(u = user)
            #send_email_report(user_obj.profile.email, "Datadonors Weekly Report", {"image": image})
                    