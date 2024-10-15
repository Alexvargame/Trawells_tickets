from django.db import models
from django.shortcuts import reverse
from routes.graph import WeightedGraph
#from routes.models import NeighboursDistance
from datetime import timedelta, datetime, date, time

from itertools import product


class TrainStatus(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    speed=models.DecimalField('Скорость, км/ч',max_digits=10, decimal_places=2, default=0.00)
    class Meta:
        verbose_name='Статус'
        verbose_name_plural='Статусы'
    def __str__(self):
        return f'{self.name}-{self.speed}'

class Cities(models.Model):

    name=models.CharField(max_length=100)

    class Meta:
        verbose_name='Город'
        verbose_name_plural='Города'

    def get_stations(self):

        stations=RailwayStations.objects.filter(city=self.id)
        return stations
        
    def get_absolute_url(self):
        return reverse('city_detail_front_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('city_update_front_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('city_delete_front_url',kwargs={'pk':self.id})


    def __str__(self):
##        c_dict={}
##        c_dict[self.name]=self.get_stations
        return self.name
                


class RailwayStations(models.Model):

    name=models.CharField(max_length=100)
    city=models.ForeignKey(Cities, on_delete=models.DO_NOTHING,
                           verbose_name='Город',related_name='city',blank=True,null=True)
    neighbours=models.ManyToManyField('self',verbose_name="соседние станции", blank=True)
    status=models.BooleanField(default=True)
    
    
    class Meta:
        default_related_name = 'railwaystations'
        verbose_name='Вокзал'
        verbose_name_plural='Вокзалы'

    def __str__(self):
        return f'{self.city}- {self.name}'
    def get_neighbours(self):
        return [f'{r.city}-{r.name}' for r in self.neighbours.all() if r.status]

    def get_absolute_url(self):
        return reverse('railway_stations_detail_front_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('railway_stations_update_front_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('railway_stations_delete_front_url',kwargs={'pk':self.id})


class Trains(models.Model):
    CHOICE_STATUS=[(obj.name,obj.name) for obj in TrainStatus.objects.all()]
    number=models.PositiveIntegerField()
    name=models.CharField(max_length=100, blank=True, default='')
    status=models.CharField(choices=CHOICE_STATUS,max_length=100, blank=True)
    train_begin=models.ForeignKey(RailwayStations, on_delete=models.DO_NOTHING,
                           verbose_name='Станция отправления',related_name='railwaystations_begin')
    train_end=models.ForeignKey(RailwayStations, on_delete=models.DO_NOTHING,
                           verbose_name='Станция прибытия',related_name='railwaystations_end')
    stations=models.ManyToManyField(RailwayStations,verbose_name="станции", related_name="stations", blank=True)
    
    class Meta:
        verbose_name='Поезд'
        verbose_name_plural='Поезда'
    def get_stations(self):
        return [f'{r.city}-{r.name}' for r in self.stations.all() if r.status]
    def __str__(self):
        return f'{self.train_begin}-{self.train_end}'
    def get_absolute_url(self):
        return reverse('train_detail_front_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('train_update_front_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('train_delete_front_url',kwargs={'pk':self.id})

    def get_distance_train(self):
        lst=[self.train_begin]
        lst.extend([st for st in self.stations.all()])
        
        return lst
        

    def get_distance_beatween_stations(self):
        lst=[self.train_begin]
        lst.extend([st for st in self.stations.all()])
        lst.append(self.train_end)
##        gr=WeightedGraph(lst)
##        for station in lst:
##            for neigh in station.neighbours.all():
##                if neigh in lst:
##                    if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
##                        dist=NeighboursDistance.objects.get(start=station, finish=neigh)
##                        gr.add_edge_by_vertices(station,neigh,dist.distance)
##                    elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
##                        dist=NeighboursDistance.objects.get(finish=station, start=neigh)
##                        gr.add_edge_by_vertices(station,neigh,dist.distance)
##                    else:
##                        gr.add_edge_by_vertices(station,neigh,0)
        return lst

class RailwayStationsTrains(models.Model):

    station=models.ForeignKey(RailwayStations, on_delete=models.DO_NOTHING,
                           verbose_name='Станция',related_name='railwaystations_trains')
    trains=models.ManyToManyField(Trains,verbose_name="проходящие поезда", blank=True)
    
    
    class Meta:
        default_related_name = 'railwaystations_trains'
        verbose_name='Поезда через вокзал'
        verbose_name_plural='Поезда через вокзалы'

    def __str__(self):
        return f'{self.station.city}-{self.station.name}'
    
    def get_trains(self):
        
        return [f'{tr.number}-{tr.train_begin}-{tr.train_end}' for tr in self.trains.all()]

   
    def get_absolute_url(self):
        return reverse('railway_stations_trains_front_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('railway_stations_update_trains_front_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('railway_stations_trains_delete_front_url',kwargs={'pk':self.id})

    def update_trains(self):
        #lst=[]
        #stn=RailwayStations.objects.get(id=self.station.id)
        self.trains.set([])
        for train in Trains.objects.all():
            if train not in self.trains.all():
                #lst.append((train, self,self.station.id,train.train_begin.id,train.train_end.id,train.stations.all(),self.station in train.stations.all()))
                if self.station.id==train.train_begin.id or  self.station.id==train.train_end.id or self.station in train.stations.all():
                    self.trains.add(train)
        return self#, lst
                    

class TicketRanks(models.Model):
    rank=models.CharField(max_length=100)
    koef=models.DecimalField('Коэффиецинт',max_digits=4, decimal_places=2, default=1.00)
    description=models.TextField(blank=True,default='')
    class Meta:
       
        verbose_name='Ранг билета'
        verbose_name_plural='Ранги билета'

    def __str__(self):
        return f'{self.rank}'
    def get_absolute_url(self):
        return reverse('ticketrank_detail_front_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('ticketrank_update_front_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('ticketrank_delete_front_url',kwargs={'pk':self.id})
    

class ScheduleTrains(models.Model):
    places=range(1,36)
    carriages=range(1,10)
    date_train=models.DateField('Дата')
    time_train=models.TimeField('Время')
    train=models.ForeignKey(Trains, on_delete=models.DO_NOTHING,
                           verbose_name='Поезд',related_name='schedule_train')
    tickets=models.CharField(max_length=5000,default=':'.join([str(item) for item in product(carriages, places)]),null=True,blank=True)
    on_sale=models.BooleanField(default=True)
    decription=models.TextField(default='',null=True,blank=True)
    #[str(str(item[0])+'-'+str(item[1]))
    class Meta:
       
        verbose_name='Расписание'
        verbose_name_plural='Расписание поездов'

##    def get_tickets(self):
##        return [tic for tic in self.tickets.all()]

    def __str__(self):
        return f'{self.train}-{self.date_train}'


    
class Ticket(models.Model):
    CHOICE_RANK=[(r.rank,r.rank) for r in TicketRanks.objects.all()]
    train=models.ForeignKey(ScheduleTrains, on_delete=models.DO_NOTHING,
                           verbose_name='Поезд',related_name='ticket_train', blank=True,null=True)
    start=models.ForeignKey(RailwayStations, on_delete=models.DO_NOTHING,
                           verbose_name='Станция отправления',related_name='ticket_start')
    finish=models.ForeignKey(RailwayStations, on_delete=models.DO_NOTHING,
                           verbose_name='Станция отправления',related_name='ticket_finish')
    date_start=models.DateTimeField('Дата поездки', blank=True,null=True)
    date_bought=models.DateTimeField('Дата покупки',auto_now_add=True)
    rank=models.CharField(choices=CHOICE_RANK, max_length=100)
    price=models.DecimalField('Цена',max_digits=10, decimal_places=2,default=0.00)
    booked=models.BooleanField(default=False)
    carriage=models.PositiveSmallIntegerField(default=1)
    place=models.PositiveSmallIntegerField(default=1)

    class Meta:
       
        verbose_name='Билет'
        verbose_name_plural='Билеты'

    def __str__(self):
        return f'{self.train}: {self.start}-{self.finish}, {self.rank}'

   
    def get_absolute_url(self):
        return reverse('ticket_detail_front_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('ticket_update_front_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('ticket_delete_front_url',kwargs={'pk':self.id})
    
    def cancel_booked_url(self):
        self.booked=False
        self.save()
        
        self.train.tickets+=':'+str((self.carriage,self.place))
        self.train.save()
        
        return reverse('ticket_detail_front_url',kwargs={'pk':self.id})

