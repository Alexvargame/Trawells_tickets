from django.contrib import admin

from .models import *


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display=('id','name','get_stations')

    

@admin.register(RailwayStations)
class RailwayStationsAdmin(admin.ModelAdmin):
    list_display=('id','name','city','get_neighbours','status')

@admin.register(RailwayStationsTrains)
class RailwayStationsTrainsAdmin(admin.ModelAdmin):
    list_display=('id','station','get_trains')

@admin.register(Trains)
class TrainsAdmin(admin.ModelAdmin):
    list_display=('id','number','name','status','train_begin','train_end','get_stations')

@admin.register(TrainStatus)
class TrainStatusAdmin(admin.ModelAdmin):
    list_display=('name','speed','description')
    
@admin.register(TicketRanks)
class TicketRanksAdmin(admin.ModelAdmin):
    list_display=('id','rank','koef')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display=('id','train','start','finish','date_start',
                  'date_bought','rank','carriage','place','price','booked')

@admin.register(ScheduleTrains)
class ScheduleTrainsAdmin(admin.ModelAdmin):
    list_display=('id','date_train','time_train','train','tickets','on_sale')


