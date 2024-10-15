from django.db import models
from railway.models import RailwayStations
from django.shortcuts import reverse


     
class NeighboursDistance(models.Model):
    
    start=models.ForeignKey(RailwayStations, on_delete=models.CASCADE,
                           verbose_name='Начальный пункт',related_name='startpoint',blank=True,null=True)
    finish=models.ForeignKey(RailwayStations, on_delete=models.CASCADE,
                           verbose_name='Конечный пункт',related_name='finishpoint',blank=True,null=True)
    distance=models.DecimalField('Расстояние, км',max_digits=10, decimal_places=2, default=0.00)
    class Meta:
        verbose_name='Расстояние между соседями'
        verbose_name_plural='Расстояния между соседями'
    def __str__(self):
        return f'{self.start}-{self.finish}'
    def get_absolute_url(self):
        return reverse('neighbours_distance_detail_front_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('neighbours_distance_update_front_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('neighbours_distance_delete_front_url',kwargs={'pk':self.id})



class Routes(models.Model):

    start=models.ForeignKey(RailwayStations, on_delete=models.CASCADE,
                           verbose_name='Начальный пункт',related_name='routestartpoint',blank=True,null=True)
    finish=models.ForeignKey(RailwayStations, on_delete=models.CASCADE,
                           verbose_name='Конечный пункт',related_name='routefinishpoint',blank=True,null=True)

##    start=models.CharField('Начальный пункт',choices=[(obj.name,f'{obj.name}-{obj.city}') for obj in RailwayStations.objects.all()],max_length=100, blank=True)
##    finish=models.CharField('Конечный пункт',choices=[(obj.name,f'{obj.name}-{obj.city}') for obj in RailwayStations.objects.all()],max_length=100, blank=True)
    stations_distance=models.ManyToManyField(NeighboursDistance,verbose_name="расстояния", related_name="distances", blank=True)
    class Meta:
        verbose_name='Маршрут'
        verbose_name_plural='Маршруты'
    def __str__(self):
        return f'{self.start.name}-{self.finish.name}'

    def get_stations_distance(self):
        return [f'{sd.start}-{sd.finish}-{sd.distance}' for sd in self.stations_distance.all()]
    def get_route_distance(self):
        return sum([sd.distance for sd in self.stations_distance.all()])

