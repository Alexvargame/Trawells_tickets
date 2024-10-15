from django.urls import path
#from . import views

from .views import *

#app_name = 'order'

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('search/', OrderSearch.as_view(), name='order_search'),
    path('search_ticket/', TicketSearch.as_view(), name='ticket_search'),
    path('booked_tickets/', BookedTickets.as_view(), name='booked_tickets'),
    path('check_booked/<int:pk>/', CheckBooked.as_view(), name='check_booked'),
    path('confirm_booked/<int:pk>/', ConfirmBooked.as_view(), name='confirm_booked'),
    path('order_item/<int:pk>/', OrderItemDetailView.as_view(), name='order_item_detail_url'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail_url'),
]
