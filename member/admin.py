from member.models import *
from django.contrib import admin


class CustomFacebookUserAdmin(admin.ModelAdmin):
    model = CustomFacebookUser

admin.site.register(CustomFacebookUser, CustomFacebookUserAdmin)

