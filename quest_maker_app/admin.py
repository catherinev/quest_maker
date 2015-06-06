from django.contrib import admin
from django import forms
from django.db import models
from .models import Quest, Waypoint, QuestTemplate, UserQuest, DailyMile

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




# Register your models here.
admin.site.register(Quest)
admin.site.register(Waypoint)
admin.site.register(QuestTemplate, QuestTemplateAdmin)
admin.site.register(UserQuest)
admin.site.register(DailyMile)
