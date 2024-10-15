from django import forms
from django.forms import widgets, fields

from .models import Cities, RailwayStations,Trains, TrainStatus, RailwayStationsTrains, Ticket, TicketRanks,ScheduleTrains
from datetime import datetime, date, time






class CityUpdateForm(forms.ModelForm):

    class Meta:
        model=Cities
        fields=['name']
    
    widgets={
              'name':forms.TextInput(attrs={'class':'form-control','empty_value':True}),                                      
     }

    
class CityStationsUpdateForm(forms.Form):
    
    stations=forms.CharField(label='Вокзалы',
                             widget=forms.CheckboxSelectMultiple(choices=[]))
                                         
  
class RailwayStationsNeighboursUpdateForm(forms.Form):
    
    neighbours=forms.CharField(label='Соседние станции',
                             widget=forms.CheckboxSelectMultiple(choices=[],attrs={'class':'form-control','empty_value':True}))
    neighbours_add=forms.CharField(label='Соседние станции',
                             widget=forms.CheckboxSelectMultiple(choices=[],attrs={'class':'form-control','empty_value':True}))
    
class TrainStationsUpdateForm(forms.Form):
    
    stations=forms.CharField(label='Станции',
                             widget=forms.CheckboxSelectMultiple(choices=[]))
    stations_add=forms.CharField(label='Станции',
                             widget=forms.CheckboxSelectMultiple(choices=[]))
                                         
class RailwayStationsUpdateForm(forms.ModelForm):

    class Meta:
        model=RailwayStations
        fields=['name','status']

    widgets={
        'name':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
 #       'city':forms.Select(choices=[(c.id,c.name) for c in Cities.objects.all()],attrs={'class':'form-control','empty_value':True}),
        'status':forms.CheckboxInput(attrs={'class':'form-control'})
                                         
   }

class RailwayStationsTrainsUpdateForm(forms.ModelForm):

    class Meta:
        model=RailwayStationsTrains
        fields=['station']

    widgets={
        'station':forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],attrs={'class':'form-control','empty_value':True}),
   }

class TrainsUpdateForm(forms.ModelForm):

    class Meta:
        model=Trains
        fields=['number','name','status','train_begin','train_end','stations']

    widgets={
        'number':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
        'name':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
        'status':forms.Select(choices=[(s.id,s.name) for s in TrainStatus.objects.all()],attrs={'class':'form-control','empty_value':True}),
        'train_begin':forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],attrs={'class':'form-control','empty_value':True}),
        'train_end':forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],attrs={'class':'form-control','empty_value':True}),
    
    
        'status':forms.CheckboxInput(attrs={'class':'form-control'})
                                         
   }

class TicketUpdateForm(forms.ModelForm):

    class Meta:
        model=Ticket
        fields=['train','start','finish','date_start','rank','price']

    widgets={
        'train':forms.Select(choices=[(tr.id,f'{tr.train_begin}-{tr.train_end}') for tr in Trains.objects.all()],
                                      attrs={'class':'form-control','empty_value':True}),
        'price':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
        'rank':forms.Select(choices=[(r.id,r.rank) for r in TicketRanks.objects.all()],attrs={'class':'form-control','empty_value':True}),
        'start':forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],
                             attrs={'class':'form-control','empty_value':True}),
        'finish':forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],
                              attrs={'class':'form-control','empty_value':True}),
        'date_start':forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}),
        #'date_bought':forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}),

                                         
   }
class TicketChoiceForm(forms.ModelForm):

    class Meta:
        model=Ticket
        fields=['start','finish','rank','carriage','place']

    widgets={
##        'train':forms.Select(choices=[(tr.id,f'{tr.train_begin}-{tr.train_end}') for tr in Trains.objects.all()],
##                                      attrs={'class':'form-control','empty_value':True}),
        #'price':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
        'rank':forms.Select(choices=[(r.rank,r.rank) for r in TicketRanks.objects.all()],attrs={'class':'form-control','empty_value':True}),
        'start':forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],
                             attrs={'class':'form-control','empty_value':True}),
        'finish':forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],
                              attrs={'class':'form-control','empty_value':True}),
        'carriage':forms.Select(choices=[(c,c) for c in range(20)],attrs={'class':'form-control','empty_value':True}),
        'place':forms.Select(choices=[(pl,pl) for pl in range(54)],attrs={'class':'form-control','empty_value':True}),                            
   }

class TrainChoiceForm(forms.Form):

     date_train=forms.DateField(label='Дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
     time_train=forms.CharField(label='Поезд-время',
                             widget=forms.Select(choices=[]))

class TrainTicketsForm(forms.Form):

    #paid=forms.CharField(label='Оплата',widget=forms.Select(choices=[(True,True),(False,False)],attrs={'class':'form-control'}))
    date=forms.DateField(label='Дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    time=forms.CharField(label='Время',widget=forms.Select(choices=[],attrs={'class':'form-control'}))
 


    
