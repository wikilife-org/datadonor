# coding=utf-8

import os

import requests
from django.core.management.base import BaseCommand, CommandError
from twitter import Twitter, OAuth
from physical.services.stats.services import PhysicalActivityDistributionService
from social.services.utilities import global_education, global_work
from health.utilities import get_conditions_rank, get_complaints_rank, get_emotions_rank


class Command(BaseCommand):

    def url_screengrab(self, url, name):
        #cmd = "export DISPLAY=:0;/usr/local/bin/CutyCapt  --auto-load-images=on --delay=15000 --max-wait=60000  --url={u} --out=/home/datadonor/static/tmp/{name}.png".format(u = url, name=name)

        cmd = 'xvfb-run --server-args="-screen 0, 1280x1200x24" CutyCapt --auto-load-images=on --plugins=on  --javascript=on --js-can-access-clipboard=on --java=on --delay=60000 --max-wait=120000 --url={u} --out=/home/datadonor/static/tmp/general/{name}.png'.format(u = url, name=name)
        os.system(cmd)

    def handle(self, *args, **options):

        cmd = 'rm -rf /home/datadonor/static/tmp/general/*'
        os.system(cmd)

        tw = TwitterService()

        if "steps" in args:
            print ("Tweet: Steps report")    
            dto = PhysicalActivityDistributionService().get_steps_distribution_global()
            text = "%s #datadonors took an average of %s daily #steps this week  #activity #physical" %(dto["total_users"], dto["avg"])
            url = "http://datadonors.org/statistics/physical-activity-steps/"
            self.url_screengrab(url+"?pic=true", "physical-activity-steps")
            tw.share_stat(text, url, "physical-activity-steps.png")

        if "miles" in args:
            print ("Tweet: Miles report")
            dto = PhysicalActivityDistributionService().get_miles_distribution_global()
            text = "%s #datadonors moved an average of %s #miles daily this week  #activity #physical" %(dto["total_users"], dto["avg"])
            url = "http://datadonors.org/statistics/physical-activity-miles/"
            self.url_screengrab(url+"?pic=true", "physical-activity-miles")
            tw.share_stat(text, url, "physical-activity-miles.png")

        if "education" in args:
            print ("Tweet: Education report")
            text = "#datadonors #education level reached"
            url = "http://datadonors.org/statistics/social-education-level/"
            self.url_screengrab(url+"?pic=true", "social-education-level")
            tw.share_stat(text, url, "social-education-level.png")

        if "work" in args:
            print ("Tweet: Work report")
            global_data, avg, total_users  = global_work()
            text = "#datadonors #working experience #avg %s years based on %s users"%(avg, total_users)
            url = "http://datadonors.org/statistics/social-work-years/"
            self.url_screengrab(url+"?pic=true", "social-work-years")
            tw.share_stat(text, url, "social-work-years.png")

        if "complaints" in args:
            print ("Tweet: Complaints report")
            data, total = get_complaints_rank()
            text = "#datadonors #top #complaints based on %s users"%(total)
            url = "http://datadonors.org/statistics/social-health-complaints/"
            self.url_screengrab(url+"?pic=true", "social-health-complaints")
            tw.share_stat(text, url, None)

        if "conditions" in args:
            print ("Tweet: Conditions report")
            data, total = get_conditions_rank()
            text = "#datadonors #top #conditions based on %s users"%(total)
            url = "http://datadonors.org/statistics/social-health-conditions/"
            self.url_screengrab(url+"?pic=true", "social-health-conditions")
            tw.share_stat(text, url, None)

        if "emotions" in args:
            print ("Tweet: Emotions report")
            data, total = get_emotions_rank()
            text = "#datadonors #top #emotions based on %s users"%(total)
            url = "http://datadonors.org/statistics/social-health-emotions/"
            self.url_screengrab(url+"?pic=true", "social-health-emotions")
            tw.share_stat(text, url, None)


class TwitterService():

    def __init__(self):
        self.consumer_key = "tI96ubeTKwDH5juZZFkt8ZKUT"
        self.consumer_secret = "3TslPpV0LnYRXy9CWXlGHbBwaSllTTob7VajyJ47lTqkmWdGUV"
        self.url_separator = " "
        self.url_separator_trimmed = "... "

    def share_stat(self, text, url, img_name):
        oauth_token = "117759178-JJqLuTIR0GYYZXcbWfpV564BjfJJbWO57vatqSgF"
        oauth_secret = "vwG1K54ejtE9ahpr7b9VxbxPu1T7iMzkFzIshAQVZcgg8"

        oauth = OAuth(oauth_token, oauth_secret,
                      self.consumer_key, self.consumer_secret)
        twitter = Twitter(auth=oauth)


        # TODO: poll these values from twitter every 24hs

        # from help/configuration#short_url_length_https
        url_length = len(url)
        # from help/configuration#characters_reserved_per_media

        if len(text) + url_length  > 140:
            trim_to = 140 - url_length  \
                - len(self.url_separator_trimmed)
            text = text[:trim_to] + self.url_separator_trimmed + url
        else:
            text = text + self.url_separator + url

        if img_name:
            image_file = "/home/datadonor/static/tmp/general/{name}".format(name=img_name)
            imagefile= open(image_file, "rb")
            data = imagefile.read()

            params = {
                "media[]": data,
                "status": text,
            }

            twitter.statuses.update_with_media(**params)
        else:
            params = {
                "status": text,
            }

            twitter.statuses.update(**params)
