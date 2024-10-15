from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *
from routes.views import *

urlpatterns = [

    path('', main_menu, name='main_menu_url'),
    path('cities/', CitiesListViewFront.as_view(), name='cities_url'),
    path('cities/create/', CityCreateViewFront.as_view(), name='city_create_url'),
    path('cities/<int:pk>/', CityDetailViewFront.as_view(), name='city_detail_front_url'),
    path('cities/<int:pk>/delete/', CityDeleteViewFront.as_view(), name='city_delete_front_url'),
    path('cities/<int:pk>/update/', CityUpdateViewFront.as_view(), name='city_update_front_url'),
    
    path('stations/', RailwayStationsListViewFront.as_view(), name='railway_stations_url'),
    path('stations/create/', RailwayStationsCreateViewFront.as_view(), name='railway_stations_create_front_url'),
    path('stations/<int:pk>/', RailwayStationsDetailViewFront.as_view(), name='railway_stations_detail_front_url'),
    path('stations/<int:pk>/update_trains/', RailwayStationsUpdateTrainsViewFront.as_view(), name='railway_stations_update_trains_front_url'),
    path('stations/<int:pk>/update/', RailwayStationsUpdateViewFront.as_view(), name='railway_stations_update_front_url'),
    path('stations/<int:pk>/delete/', RailwayStationsDeleteViewFront.as_view(), name='railway_stations_delete_front_url'),
    path('stations/<int:pk>/distance/', RailwayStationsDistancesView.as_view(), name='railway_stations_distances_front_url'),
    
    path('trains/', TrainsListViewFront.as_view(), name='trains_url'),
    path('trains/<int:pk>/', TrainDetailViewFront.as_view(), name='train_detail_front_url'),
    path('trains/<int:pk>/bought_tickets', TrainTicketsBought.as_view(), name='train_tickets_bought_url'),
    path('trains/<int:pk>/delete/', TrainDeleteViewFront.as_view(), name='train_delete_front_url'),
    path('trains/<int:pk>/update/', TrainUpdateViewFront.as_view(), name='train_update_front_url'),
    path('trains/create/', TrainCreateViewFront.as_view(), name='train_create_front_url'),
    
    path('tickets/', TicketsListViewFront.as_view(), name='tickets_url'),
    path('tickets/choice/<int:pk>/', TicketsChoiceViewFront.as_view(), name='tickets_choice_url'),
    path('tickets/booked/<int:pk>/', BookedTicketsViewFront.as_view(), name='tickets_booked_url'),
    path('tickets/create/', TicketCreateViewFront.as_view(), name='ticket_create_front_url'),
    path('tickets/<int:pk>/', TicketDetailViewFront.as_view(), name='ticket_detail_front_url'),
    path('tickets/<int:pk>/delete/', TicketDeleteViewFront.as_view(), name='ticket_delete_front_url'),
    path('tickets/<int:pk>/update/', TicketUpdateViewFront.as_view(), name='ticket_update_front_url'),
    
    path('ticketranks/', TicketRanksListViewFront.as_view(), name='ticketranks_url'),
    path('ticketranks/create/', TicketRankCreateViewFront.as_view(), name='ticketrank_create_front_url'),
    path('ticketranks/<int:pk>/', TicketRankDetailViewFront.as_view(), name='ticketrank_detail_front_url'),
    path('ticketranks/<int:pk>/delete/', TicketRankDeleteViewFront.as_view(), name='ticketrank_delete_front_url'),
    path('ticketranks/<int:pk>/update/', TicketRankUpdateViewFront.as_view(), name='ticketrank_update_front_url'),
     
    


    
    path('api/v1/cities/', CitiesListView.as_view(), name='cities_list_url'),
    path('api/v1/cities/<int:pk>/', CityDetailView.as_view(), name='city_detail_url'),
    path('api/v1/cities/<int:pk>/update/', CityUpdateView.as_view(), name='cities_update_url'),
    path('api/v1/cities/<int:pk>/delete/', CityDeleteView.as_view(), name='city_delete_url'),
    path('api/v1/stations/', RailwayStationsListView.as_view(), name='railway_stations_list_url'),
    path('api/v1/stations/create/', RailwayStationsCreateView.as_view(), name='railway_stations_create_url'),
    path('api/v1/stations/<int:pk>/', RailwayStationsDetailView.as_view(), name='railway_stations_detail_url'),
    path('api/v1/stations/<int:pk>/update/', RailwayStationsUpdateView.as_view(), name='railway_stations_update_url'),
    path('api/v1/stations/<int:pk>/delete/', RailwayStationsDeleteView.as_view(), name='railway_stations_delete_url'),
    path('api/v1/trains/', TrainsListView.as_view(), name='trains_list_url'),
    path('api/v1/trains/<int:pk>/', TrainDetailView.as_view(), name='train_detail_url'),
    path('api/v1/trains/<int:pk>/delete/', TrainDeleteView.as_view(), name='train_delete_url'),
    path('api/v1/trains/<int:pk>/update/', TrainUpdateView.as_view(), name='train_update_url'),
    path('api/v1/trains/create/', TrainCreateView.as_view(), name='train_create_url'),
       

]

