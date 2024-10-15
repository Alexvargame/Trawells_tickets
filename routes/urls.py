from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
##    path('api/v1/cities/', CitiesListView.as_view(), name='cities_list_url'),
##    path('api/v1/cities/<int:pk>/', CityDetailView.as_view(), name='city_detail_url'),
##    path('api/v1/cities/<int:pk>/update/', CityUpdateView.as_view(), name='cities_update_url'),
##    path('api/v1/cities/<int:pk>/delete/', CityDeleteView.as_view(), name='city_delete_url'),
##    path('api/v1/stations/', RailwayStationsListView.as_view(), name='railway_stations_list_url'),
    path('api/v1/graph/', get_graph, name='railway_stations_graph_url'),
    #path('api/v1/graphlist/', GraphView.as_view(), name='graph_list_url'),
    path('api/v1/graphlist/', WeightedGraphView.as_view(), name='weighted_graph_list_url'),
    path('api/v1/routes_distance/', RoutesByDistanceView.as_view(), name='routes_by_distance_list_url'),
    
    path('api/v1/neighbours_distance/', NeighboursDistanceListViewFront.as_view(), name='neighbours_distance_url'),
    path('api/v1/neighbours_distance/create/', NeighboursDistanceCreateViewFront.as_view(), name='neighbours_distance_create_url'),
    path('api/v1/neighbours_distance/<int:pk>/', NeighboursDistanceDetailViewFront.as_view(), name='neighbours_distance_detail_front_url'),
    path('api/v1/neighbours_distance/<int:pk>/delete/', NeighboursDistanceDeleteViewFront.as_view(), name='neighbours_distance_delete_front_url'),
    path('api/v1/neighbours_distance/<int:pk>/update/', NeighboursDistanceUpdateViewFront.as_view(), name='neighbours_distance_update_front_url'),
##    path('api/v1/stations/create/', RailwayStationsCreateView.as_view(), name='railway_stations_create_url'),
##    path('api/v1/stations/<int:pk>/', RailwayStationsDetailView.as_view(), name='railway_stations_detail_url'),
##    path('api/v1/stations/<int:pk>/update/', RailwayStationsUpdateView.as_view(), name='railway_stations_update_url'),
##    path('api/v1/stations/<int:pk>/delete/', RailwayStationsDeleteView.as_view(), name='railway_stations_delete_url'),
##    path('api/v1/trains/', TrainsListView.as_view(), name='routes_list_url'),
##    path('api/v1/trains/<int:pk>/', TrainDetailView.as_view(), name='route_detail_url'),
##    path('api/v1/trains/<int:pk>/delete/', TrainDeleteView.as_view(), name='route_delete_url'),
##    path('api/v1/trains/<int:pk>/update/', TrainUpdateView.as_view(), name='route_update_url'),
##    path('api/v1/trains/create/', TrainCreateView.as_view(), name='route_create_url'),
       

]

