from django import forms
from .models import Order
from railway.models import Trains


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','email',
                  'address','postal_code','city']

        
class OrderSearchForm(forms.ModelForm):

    paid=forms.CharField(label='Оплата',widget=forms.Select(choices=[(True,True),(False,False)],attrs={'class':'form-control'}))
    date_b=forms.DateField(label='Начальная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    date_e=forms.DateField(label='Конечная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))


    class Meta:
        model=Order
        fields=['first_name','last_name',
                  'address','city','paid']
    widgets={
        'first_name':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
        'last_name':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
##        'address':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
##        'city':forms.TextInput(attrs={'class':'form-control','empty_value':True}),
       # 'created':forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}),
                             
   }

class TicketSearchForm(forms.Form):

    #paid=forms.CharField(label='Оплата',widget=forms.Select(choices=[(True,True),(False,False)],attrs={'class':'form-control'}))
    date_b=forms.DateField(label='Начальная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    date_e=forms.DateField(label='Конечная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    train=forms.CharField(label='Поезд',widget=forms.Select(choices=[(tr.id,f'{tr.train_begin}-{tr.train_end}')
                                                                  for tr in Trains.objects.all()],attrs={'class':'form-control'}))
