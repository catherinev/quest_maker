from django.conf.urls import url
from django.views.generic import TemplateView, FormView
from django.contrib.auth import views as authviews

from quest_maker_app import views


urlpatterns = [

    url(r'^$',
        views.homepage,
        name='homepage'),
    url(r'^about/$',
        TemplateView.as_view(template_name='quest_maker_app/about.html'),
        name='about'),

    # Authentication.
    # See https://docs.djangoproject.com/en/1.8/topics/auth/default/
    # By default, these views look for templates inside quest_maker/templates/registration/
    url(r'^login/$',
        authviews.login,
        name='login'),
    # Note that the view function can be passed nondefault arguments
    # by setting url kwargs parameter to a dict with argument names as keys.
    url(r'^logout/$',
        authviews.logout,
        kwargs={'next_page': '/'},
        name='logout'),
    url(r'^signup/$',
        views.signup,
        name='signup'),
    url(r'^password-reset/$',
        authviews.password_reset,
        name='password_reset'),

    url(r'^quest/(?P<quest_id>\d+)/$',
        views.quest,
        name='quest'),
    url(r'^quest/(?P<quest_id>\d+)/user/(?P<user_id>\d+)/$',
        views.user_quest,
        name='user_quest'),
]
