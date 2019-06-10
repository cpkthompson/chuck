from django.contrib import admin

from workspace.models import IdeUser
# Register your models here.

class IdeUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(IdeUser, IdeUserAdmin)