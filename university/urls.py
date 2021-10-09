from django.urls import path, include
from . import views

app_name = 'university'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('get_directions/', views.GetDirectionsView.as_view(), name='get_direction'),
    path('get_address/', views.GetAddressView.as_view(), name='get_address'),
    path('get_entrances/<int:pk>/', views.GetEntranceElementsView.as_view(), name='get_address'),
    path('get_location_elements/', views.GetLocationElementsView.as_view(), name='get_location_elements'),
    path('search_locations/', views.SearchLocationsView.as_view(), name='search_locations'),
]