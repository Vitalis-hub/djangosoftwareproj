from django.urls import path, include
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
import university.back

import university.back as back
from . import views

app_name = 'university'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('get_directions/', views.GetDirectionsView.as_view(), name='get_direction'),
    path('get_address/', views.GetAddressView.as_view(), name='get_address'),
    path('get_entrances/<int:pk>/', views.GetEntranceElementsView.as_view(), name='get_address'),
    path('get_location_elements/', views.GetLocationElementsView.as_view(), name='get_location_elements'),
    path('search_locations/', views.SearchLocationsView.as_view(), name='search_locations'),
    url(r'^panel/$', back.panel, name='panel'),
    url(r'^mylogin/$', back.mylogin, name='mylogin'),
    url(r'^signup/$', back.register ,name='register'),
]