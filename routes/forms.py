from django import forms
from django.forms import widgets, fields

from railway.models import RailwayStations
from datetime import datetime, date, time


    
class ChoiceRouteForm(forms.Form):
    
    start=forms.CharField(label='Начальный пункт',
                             widget=forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],
                                                 attrs={'class':'form-control','empty_value':True}))
    finish=forms.CharField(label='Конечный пункт',
                             widget=forms.Select(choices=[(st.id,f'{st.name}-{st.city}') for st in RailwayStations.objects.all()],
                                                 attrs={'class':'form-control','empty_value':True}))
                                         
  
