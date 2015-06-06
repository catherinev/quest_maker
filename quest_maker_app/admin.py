from django.contrib import admin
from .models import Quest, Waypoint, QuestTemplate, UserQuest, DailyMile


# Register your models here.
admin.site.register(Quest)
admin.site.register(Waypoint)
admin.site.register(QuestTemplate)
admin.site.register(UserQuest)
admin.site.register(DailyMile)