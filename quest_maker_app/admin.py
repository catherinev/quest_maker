from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django.db import models
from .models import (Quest, Waypoint, QuestTemplate, UserQuest, DailyDistance, 
                     Profile)

# Enable inline editing of waypoints inside QuestTemplate editor.
class WaypointInline(admin.TabularInline):
    model = Waypoint
    # Configure number and text box size for waypoint descriptions:
    extra = 10
    formfield_overrides = {
        models.TextField:
        {'widget': forms.Textarea(attrs={'rows': 1, 'cols': 40})},
    }


class QuestTemplateAdmin(admin.ModelAdmin):
    inlines = [
        WaypointInline
    ]
    exclude = ()


class QuestAdmin(admin.ModelAdmin):
    inlines = [
        WaypointInline
    ]
    exclude = ()

# add user profile to user
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


# Reregister the User admin.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register the rest of the models.
admin.site.register(Quest)
admin.site.register(Waypoint)
admin.site.register(QuestTemplate, QuestTemplateAdmin)
admin.site.register(UserQuest)
admin.site.register(DailyDistance)
