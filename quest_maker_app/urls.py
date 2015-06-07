from django.conf.urls import url
from quest_maker_app import views


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),  
    url(r'^quest/(?P<quest_id>\d+)/$', views.quest, name='quest'),
    url(r'^quest/(?P<quest_id>\d+)/user/(?P<user_id>\d+)/$', views.user_quest, 
        name='user_quest'),
]