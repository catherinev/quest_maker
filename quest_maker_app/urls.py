from django.conf.urls import url
from django.views.generic import TemplateView, FormView
from quest_maker_app import views


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about/$', TemplateView.as_view(template_name='quest_maker_app/about.html'), name='about'),
    url(r'^quest/(?P<quest_id>\d+)/$', views.quest, name='quest'),
    url(r'^quest/(?P<quest_id>\d+)/user/(?P<user_id>\d+)/$', views.user_quest,
        name='user_quest'),
]
