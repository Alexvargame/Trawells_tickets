from django.urls import path
from .views import *

urlpatterns = [
 path('', cart_detail, name='cart_detail'),
 path('add/<int:ticket_id>/', cart_add, name='cart_add'),
 path('remove/<int:ticket_id>/', cart_remove, name='cart_remove'),
]
