from django.conf.urls import url
from . import views

urlpatterns = [
    #set the root of t
    url(r'^panel/manager/group/$', views.manager_group, name='manager_group'),
]