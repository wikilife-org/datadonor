"""Admin settings"""

from django.contrib import admin
from social.models import *


admin.site.register(Profile)
admin.site.register(SocialUserAggregatedData)
admin.site.register(GlobalEducationDistribution)
admin.site.register(GlobalWorkExperinceDistribution)
admin.site.register(SocialGlobalAggregatedData)
admin.site.register(DegreeLevel)