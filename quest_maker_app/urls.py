from django.conf.urls import url
from quest_maker_app import views


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),  
            
]