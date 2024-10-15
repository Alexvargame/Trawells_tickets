from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *

##class CitiesSerializer(serializers.ModelSerializer):
##
##    class Meta:
##        model=Cities
##        fields=('name',)
##        
class NeighboursDistanceSerializer(serializers.ModelSerializer):
    start=serializers.SlugRelatedField(slug_field="Начальный пункт", read_only=True)
    finish=serializers.SlugRelatedField(slug_field="Конечный пункт", read_only=True)
    #city=serializers.ChoiceField(choices=[(c.id,c.name) for c in Cities.objects.all()],style={'base_template': 'select.html'})
    class Meta:
        model=NeighboursDistance
        fields=('start','finish','distance')

    def create(self, validated_data):
        distance=NeighboursDistance.objects.update_or_create(
            distance=validated_data.get('distance',None),
            start=RailwayStations.objects.get(name=validated_data.get('start')),
            finish=RailwayStations.objects.get(name=validated_data.get('finish'))
            )
        return distance
class NeighboursDistanceCreateSerializer(serializers.ModelSerializer):
    start=serializers.ChoiceField(choices=[(st.id,f'{st.city}-{st.name}') for st in RailwayStations.objects.all()],style={'base_template': 'select.html'})
    finish=serializers.ChoiceField(choices=[(st.id,f'{st.city}-{st.name}') for st in RailwayStations.objects.all()],style={'base_template': 'select.html'})
    #city=serializers.ChoiceField(choices=[(c.id,c.name) for c in Cities.objects.all()],style={'base_template': 'select.html'})
    class Meta:
        model=NeighboursDistance
        fields=('start','finish','distance')

    def create(self, validated_data):
        distance=NeighboursDistance.objects.create(
            distance=validated_data.get('distance',None),
            #start=RailwayStations.objects.get(name=validated_data.get('start')),
            #finish=RailwayStations.objects.get(name=validated_data.get('finish'))
            )
        return distance
class NeighboursDistanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=NeighboursDistance
        fields=('distance',)

##        
##class CityDetailSerializer(serializers.Serializer):
##    name = serializers.CharField(max_length=100)
##    stations= RailwayStationsSerializer(read_only=True, many=True)
##
##    
##class TrainsSerializer(serializers.ModelSerializer):
##    route_begin=RailwayStationsSerializer()
##    route_end=RailwayStationsSerializer()
##    stations=RailwayStationsSerializer(read_only=True, many=True)
##    class Meta:
##        model=Trains
##        fields=('number','status','name','route_begin','route_end','stations')
##
##    def create(self, validated_data):
##        route=Routes.objects.update_or_create(
##            #defaults={'city':Cities.objects.get(id=1)},
##            name=validated_data.get('name',None),
##            status=validated_data.get('status',None),
##            number=validated_data.get('number',None),
##            route_begin=RailwayStations.objects.get(id=validated_data.get('route_begin')),
##            route_end=RailwayStations.objects.get(id=validated_data.get('route_end')),
##            )
##        return route
##
####class RoutesSerializer(serializers.ModelSerializer):
##    route_begin=RailwayStationsSerializer()
##    route_end=RailwayStationsSerializer()
##    class Meta:
##        model=Routes
##        fields=('number','status','name','route_begin','route_end','stations')
