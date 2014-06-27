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
import base64


def url_screengrab(user_id, **kwargs):
    cmd = "export DISPLAY=:0;/usr/local/bin/CutyCapt  --auto-load-images=on --delay=15000 --max-wait=60000  --url=http://datadonors.org/reports/user/full/{u}/  --out=/home/datadonor/static/tmp/report_{u}.png".format(u = user_id)
    os.system(cmd)
    

def user_weekly_report():
    emails = []
    #users = User.objects.all()
    users = [User.objects.get(id= 1)]
    for user in users:
        if user.profile.email and user.profile.email not in emails:
            emails.append(user.profile.email)
            url_screengrab(user.id)
            image = "report_{u}.png".format(u = user.id)
            send_email_report(user.profile.email, "DataDonors Weekly Report", {"user_id":base64.b64encode(str(user.id).encode('ascii')), "image": image})
                    