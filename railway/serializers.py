from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Cities,RailwayStations, Trains, Ticket, TicketRanks

class CitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Cities
        fields=('name',)
        
class RailwayStationsSerializer(serializers.ModelSerializer):
    city=serializers.SlugRelatedField(slug_field="name", read_only=True)
    #city=serializers.ChoiceField(choices=[(c.id,c.name) for c in Cities.objects.all()],style={'base_template': 'select.html'})
    class Meta:
        model=RailwayStations
        fields=('name','city','neighbours','status')

    def create(self, validated_data):
        station=RailwayStations.objects.update_or_create(
            #defaults={'city':Cities.objects.get(id=1)},
            name=validated_data.get('name',None),
            city=Cities.objects.get(name=validated_data.get('city'))
            )
        return station
    
##class RailwayStationsTrainsSerializer(serializers.ModelSerializer):
##    trains=serializers.SlugRelatedField(slug_field="name", read_only=True)
##    #city=serializers.ChoiceField(choices=[(c.id,c.name) for c in Cities.objects.all()],style={'base_template': 'select.html'})
##    class Meta:
##        model=RailwayStationsTrains
##        fields=('trains',)
##        return station

    
class RailwayStationsCreateSerializer(serializers.ModelSerializer):
    
    city=serializers.ChoiceField(choices=[(c.id,c.name) for c in Cities.objects.all()],style={'base_template': 'select.html'})
    neighbours=serializers.MultipleChoiceField(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all() if st.status],
                                       style={'base_template': 'checkbox_multiple.html'})
    class Meta:
        model=RailwayStations
        fields=('name','city','neighbours')

    def create(self, validated_data):
        station=RailwayStations.objects.create(
            name=validated_data.get('name',None),
            #city=Cities.objects.get(name=validated_data.get('city'))
            )
        return station


class RailwayStationsUpdateSerializer(serializers.ModelSerializer):
    
    city=serializers.ChoiceField(label='Город',choices=[(c.id,c.name) for c in Cities.objects.all()],style={'base_template': 'select.html'})
    neighbours=RailwayStationsSerializer(label='Соседние станции',read_only=True, many=True)
    #serializers.MultipleChoiceField(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],
                                       #style={'base_template': 'checkbox_multiple.html'})
    class Meta:
        model=RailwayStations
        fields=('name','city','neighbours')

    def create(self, validated_data):
        station=RailwayStations.objects.update_or_create(
            name=validated_data.get('name',None),
            #city=Cities.objects.get(name=validated_data.get('city'))
            )
        return station
    
class RailwayStationsTrainSerializer(serializers.ModelSerializer):
    name=serializers.ChoiceField(label='Город',choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all() if st.status],style={'base_template': 'select.html'})
    class Meta:
        model=RailwayStations
        fields=('name',)

    
class CityUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Cities
        fields=('name','get_stations')
    name = serializers.CharField(label='Город',max_length=100)
    #stations=RailwayStationsSerializer(read_only=True, many=True)
    get_stations=serializers.ChoiceField(label="Вокзалы",choices=[(st.id,(st.name,st.city)) for st in RailwayStations.objects.all() if st.status],
                                         style={'base_template': 'checkbox_multiple.html'})

    
class TrainsSerializer(serializers.ModelSerializer):
    train_begin=serializers.ChoiceField(label='Пункт отбытия',choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all() if st.status],
                                       style={'base_template': 'select.html'})
    train_end=serializers.ChoiceField(label='Пункт назначения',choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all() if st.status],
                                       style={'base_template': 'select.html'})
    stations=serializers.MultipleChoiceField(label='Станции',choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all() if st.status],
                                       style={'base_template': 'checkbox_multiple.html'})

    class Meta:
        model=Trains
        fields=('number','status','name','train_begin','train_end','stations')

    def create(self, validated_data):
 
        train=Trains.objects.update_or_create(
            name=validated_data.get('name',None),
            status=validated_data.get('status',None),
            number=validated_data.get('number',None),           
            train_begin=RailwayStations.objects.get(id=validated_data.get('train_begin')),
            train_end=RailwayStations.objects.get(id=validated_data.get('train_end')),
            )
        return train

    
class TicketSerializer(serializers.ModelSerializer):
    
    train=serializers.ChoiceField(label='Поезд',choices=[(tr.id,f'{tr.train_begin}-{tr.train_end}') for tr in Trains.objects.all()],
                                       style={'base_template': 'select.html'})
    start=serializers.ChoiceField(label='Пункт назначения',choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all() if st.status],
                                       style={'base_template': 'select.html'})
    finish=serializers.ChoiceField(label='Пункт прибытия',choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all() if st.status],
                                       style={'base_template': 'select.html'})
    rank=serializers.ChoiceField(label='Ранг',choices=[(r.rank,r.rank) for r in TicketRanks.objects.all()],
                                       style={'base_template': 'select.html'})

    class Meta:
        model=Ticket
        fields=('train','start','finish','date_start','date_bought','rank','price')

    def create(self, validated_data):
 
        ticket=Ticket.objects.update_or_create(
            train=Trains.objects.get(id=validated_data.get('train')),          
            start=RailwayStations.objects.get(id=validated_data.get('start')),
            finish=RailwayStations.objects.get(id=validated_data.get('finish')),
            date_start=validated_data.get('date_start',None),
            date_bought=validated_data.get('date_bought',None),    
            rank=validated_data.get('rank',None),
            price=validated_data.get('price',None), 
            
            )
        return ticket


class TicketRanksSerializer(serializers.ModelSerializer):
    rank = serializers.CharField(label='Ранг',max_length=100)
    description = serializers.CharField(label='Описание')

    class Meta:
        model=TicketRanks
        fields=('rank','description')


        
##class RoutesSerializer(serializers.ModelSerializer):
##    route_begin=RailwayStationsSerializer()
##    route_end=RailwayStationsSerializer()
##    class Meta:
##        model=Routes
##        fields=('number','status','name','route_begin','route_end','stations')
