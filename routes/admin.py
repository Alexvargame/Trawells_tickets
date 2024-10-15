from django.contrib import admin
from .models import NeighboursDistance, Routes

@admin.register(NeighboursDistance)
class NeighboursDistanceAdmin(admin.ModelAdmin):
    list_display=('id','start','finish','distance')


@admin.register(Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display=('id','start','finish','get_stations_distance','get_route_distance')

