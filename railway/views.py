from django.shortcuts import render,get_object_or_404, redirect
from django import forms
from django.conf import settings
from django.forms import fields, widgets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import (CitiesSerializer,
                          RailwayStationsSerializer,
                          RailwayStationsCreateSerializer,
                          RailwayStationsUpdateSerializer,
                          CityUpdateSerializer,
                          TrainsSerializer,
                          TicketSerializer,
                          TicketRanksSerializer)
from .models import Cities, RailwayStations, Trains,RailwayStationsTrains, Ticket, TicketRanks,ScheduleTrains

from .forms import (CityUpdateForm,
                    CityStationsUpdateForm,
                    RailwayStationsUpdateForm,
                    RailwayStationsNeighboursUpdateForm,
                    TrainsUpdateForm,
                    TrainStationsUpdateForm,
                    RailwayStationsTrainsUpdateForm,
                    TicketUpdateForm,
                    TicketChoiceForm,
                    TrainChoiceForm,
                    TrainTicketsForm)
from cart.forms import CartAddTicketForm
from order.models import OrderItem
from rest_framework import generics
from django.core.cache import cache
from routes.serializers import NeighboursDistanceSerializer
from routes.models import NeighboursDistance
from routes.graph import WeightedGraph
from routes.dijkstra import *

from django.db.models import Q
from datetime import timedelta, datetime

def main_menu(request):
    return render(request,'railway/main_page.html')
""" CRUD, List- Города """

class CitiesListView(generics.ListCreateAPIView):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer


class CityDetailView(APIView):

    def get(self, request,pk):
      
        city=get_object_or_404(Cities,id=pk)
        
        return Response({city.name:[s['name'] for s in serializer.data]})
  
class CityUpdateView(generics.UpdateAPIView):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer

    def get(self, request,pk):
      
        city=get_object_or_404(Cities,id=pk)
        serializer=CitiesSerializer(city)
        return Response(serializer.data)

    
    

class CityDeleteView(generics.DestroyAPIView):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
    def get(self, request,pk):
      
        city=get_object_or_404(Cities,id=pk)
        serializer=CitiesSerializer(city)
        return Response(serializer.data)

##class CitiesListView(APIView):
##
##    def get(self,request):
##        cities=Cities.objects.all()
##        serializer=CitiesSerializer(cities, many=True)
##        return Response(serializer.data)

##class RailwayStationsListView(APIView):
##    
##    def get(self, request):
##        stations=RailwayStations.objects.all()
##        serializer=RailwayStationsSerializer(stations, many=True)
##        return Response(serializer.data)

""" CRUD, List- Вокзалы """


class RailwayStationsListView(generics.ListAPIView):
    queryset = RailwayStations.objects.all()
    serializer_class = RailwayStationsSerializer

class RailwayStationsCreateView(APIView):

    def post(self, request):
        serializer=RailwayStationsSerializer(data=request.data)
        
        if serializer.is_valid():
            station=serializer.create(request.data)
            #station[0].city=Cities.objects.filter(name__in=request.data['city'])
            #station[0].city.set(city)
            return Response(f'{station}')
            #   redirect('railway_stations_list_url')
        else:
            station=serializer.create(request.data)
            return Response(f'{station}')

    


class RailwayStationsUpdateView(generics.UpdateAPIView):
    queryset = RailwayStations.objects.all()
    serializer_class = RailwayStationsSerializer

    def get(self, request,pk):
      
        station=get_object_or_404(RailwayStations,id=pk)
        serializer=RailwayStationsSerializer(station)
        return Response(serializer.data)

class RailwayStationsDeleteView(generics.DestroyAPIView):
    queryset = RailwayStations.objects.all()
    serializer_class = RailwayStationsSerializer

    def get(self, request,pk):
      
        station=get_object_or_404(RailwayStations,id=pk)
        serializer=RailwayStationsSerializer(station)
        return Response(serializer.data)

class RailwayStationsDetailView(generics.RetrieveAPIView):
    queryset = RailwayStations.objects.all()
    serializer_class = RailwayStationsSerializer

    def get(self, request,pk):
      
        station=get_object_or_404(RailwayStations,id=pk)
        serializer=RailwayStationsSerializer(station)
        return Response(serializer.data)


""" CRUD, List- Маршруты """

class TrainsListView(generics.ListAPIView):
    queryset = Trains.objects.all()
    serializer_class = TrainsSerializer


    

class TrainDetailView(generics.RetrieveAPIView):
    queryset = Trains.objects.all()
    serializer_class = TrainsSerializer

class TrainDeleteView(generics.DestroyAPIView):
    queryset = Trains.objects.all()
    serializer_class = TrainsSerializer

    def get(self, request,pk):
      
        train=get_object_or_404(Trains,id=pk)
        serializer=TrainsSerializer(route)
        return Response(serializer.data)

class TrainCreateView(APIView):

    def post(self, request):
        serializer=RoutesSerializer(data=request.data)
        if serializer.is_valid():
            train=serializer.create(request.data)
            stations=RailwayStations.objects.filter(id__in=request.data['stations'])
            toute[0].stations.set(stations)
            return Response(f'{train}')
            #   redirect('railway_stations_list_url')
        else:
            train=serializer.create(request.data)
            stations=RailwayStations.objects.filter(id__in=request.data['stations'])
            route[0].stations.set(stations)
            return Response(f'{train}')

class TrainUpdateView(APIView):

  

    def get(self, request,pk):
      
        route=get_object_or_404(Routes,id=pk)
        serializer=TrainsSerializer(route)
        return Response(serializer.data)
    
    def post(self, request,pk):
        serializer=TrainsSerializer(data=request.data)
        if serializer.is_valid():
            train=serializer.create(request.data)
            stations=RailwayStations.objects.filter(id__in=request.data['stations'])
            toute[0].stations.set(stations)
            return Response(f'{train}')
            #   redirect('railway_stations_list_url')
        else:
            train=serializer.create(request.data)
            stations=RailwayStations.objects.filter(id__in=request.data['stations'])
            route[0].stations.set(stations)
            return Response(f'{train}')


""" Frontend """

""" CRUD, List- Города """

class CitiesListViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/cities_list.html'
    

    def get(self,request):
        cities=cache.get('cities')
        if not cities:
            cities=Cities.objects.all()
            cache.set('cities',cities,10)
        paginator=Paginator(cities,15)
        page=request.GET.get('page')
        try:
            cities=paginator.page(page)
        except PageNotAnInteger:
            cities=paginator.page(1)
        except EmptyPage:
            cities=paginator.page(paginator.num_pages)
        
        serializer=CitiesSerializer(cities,many=True)
        return Response({'cities':cities, 'page':page})


class CityCreateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/city_create.html'


    def get(self,request):
        serializer=CitiesSerializer()
        return Response({'serializer':serializer})

    def post(self, request):
        serializer=CitiesSerializer(data=request.data)
        if serializer.is_valid():            
            serializer.save()
        return redirect('cities_url')
        
class CityUpdateViewFront(LoginRequiredMixin,APIView):
    
    template_name = 'railway/city_update.html'


    def get(self,request,pk):
        city=get_object_or_404(Cities,id=pk)
        query=[(s.id,s.name) for s in city.get_stations()]
        form=CityUpdateForm(instance=city)
        form_stations=CityStationsUpdateForm()
        return render(request,'railway/city_update.html',{'form':form,
                                                          'stations':form_stations['stations'].as_widget(forms.CheckboxSelectMultiple(choices=query))})
                      
    def post(self, request,pk):
        city=get_object_or_404(Cities,id=pk)
        query=[(s.id,s.name) for s in city.get_stations()]
        bound_form=CityUpdateForm(request.POST,instance=city)
        bound_form_stations=CityStationsUpdateForm(request.POST)
        new_set_stations=[st for st in RailwayStations.objects.filter(id__in=bound_form_stations['stations'].value())]
        if bound_form.is_valid():
            new_city=bound_form.save()
            for st in city.get_stations():
                if str(st.id) not in bound_form_stations['stations'].value():
                    st.status=False
                    st.save()
            
            return redirect(new_city)
            #return render(request,'railway/city_update.html',{'form':bound_form,'s':(new_set_stations,bound_form_stations['stations'].value()),
                                                          #'stations':bound_form_stations['stations'].as_widget(forms.CheckboxSelectMultiple(choices=query))})
          
        else:
            return render(request,'railway/city_update.html',{'form':bound_form,
                                                          'stations':bound_form_stations['stations'].as_widget(forms.CheckboxSelectMultiple(choices=query))})
    
class CityDetailViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/city_detail.html'

    def get(self, request,pk):
      
        city=get_object_or_404(Cities,id=pk)
        serializer=RailwayStationsSerializer(city.get_stations(),many=True)
        return Response({'city':city})#.name:[s['name'] for s in serializer.data]})
  

class CityDeleteViewFront(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        city=get_object_or_404(Cities,id=pk)
        serializer=CitiesSerializer(city)
        return render(request,'railway/city_delete.html',{'city':city})
    def post(self, request,pk):
      
        city=get_object_or_404(Cities,id=pk)
        city.delete()
        cache.set('cities','')
        return redirect('cities_url')
    
""" CRUD, List- Станции """

class RailwayStationsListViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/railway_stations_list.html'
    

    def get(self,request):
        stations=cache.get('stations')
        if not stations:
            stations=RailwayStations.objects.all()
            cache.set('stations',stations,10)
        paginator=Paginator(stations,15)
        page=request.GET.get('page')
        try:
            stations=paginator.page(page)
        except PageNotAnInteger:
            stations=paginator.page(1)
        except EmptyPage:
            stations=paginator.page(paginator.num_pages)
        
        serializer=RailwayStationsSerializer(stations,many=True)
        return Response({'stations':stations, 'page':page})


class RailwayStationsCreateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/railway_stations_create.html'


    def get(self,request):
        serializer=RailwayStationsCreateSerializer()
        return Response({'serializer':serializer})

    def post(self, request):
        city=Cities.objects.get(id=request.data['city'])
        if not RailwayStations.objects.filter(city=city).exists():
            serializer=RailwayStationsCreateSerializer(data=request.data)
            if serializer.is_valid():         
                station=serializer.create(request.data)
                neighs=RailwayStations.objects.filter(id__in=serializer.data['neighbours'])
                
                station.neighbours.set(neighs)
                station.city=city
                station.save()
                for st in station.neighbours.all():
                    dist=NeighboursDistance(start=station, finish=st,distance=0)
                    dist.save()
                
        #return Response({'serializer':serializer,'s':(serializer.data['neighbours'],request.data['neighbours'],neighs, request.data)})
        return redirect('railway_stations_url')
        
class RailwayStationsUpdateViewFront(LoginRequiredMixin,APIView):
    
    def get(self,request,pk):
        station=get_object_or_404(RailwayStations,id=pk)
        query_n=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s in station.neighbours.all() and s.id!=station.id]
        query_add=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s not in station.neighbours.all() and s.id!=station.id]
        form=RailwayStationsUpdateForm(instance=station)#, initial={'city':station.city})
        form_st=RailwayStationsNeighboursUpdateForm()
        return render(request,'railway/railway_stations_update.html',{'form':form,#'station':station,
                                    'neighs':form_st['neighbours'].as_widget(forms.CheckboxSelectMultiple(choices=query_n)),
                                    'neighs_add':form_st['neighbours_add'].as_widget(forms.CheckboxSelectMultiple(choices=query_add))})

    def post(self, request,pk):
        station=get_object_or_404(RailwayStations,id=pk)
        query_n=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s in station.neighbours.all() and s.id!=station.id]
        query_add=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s not in station.neighbours.all() and s.id!=station.id]
        bound_form=RailwayStationsUpdateForm(request.POST,instance=station)
        bound_form_st=RailwayStationsNeighboursUpdateForm(request.POST)
        new_neighbours=[st for st in RailwayStations.objects.filter(id__in=bound_form_st['neighbours_add'].value())]
        new_neighbours.extend([st for st in station.neighbours.all()
                                    if st not in [st for st in RailwayStations.objects.filter(id__in=bound_form_st['neighbours'].value())]])      

        if bound_form.is_valid():
            new_station=bound_form.save()
            new_station.neighbours.set(new_neighbours)
            new_station.save()
            for st in new_station.neighbours.all():
                dist=NeighboursDistance(start=new_station, finish=st,distance=0)
                dist.save()
            return redirect('railway_stations_url')
        else:
            return render(request,'railway/railway_stations_update.html',{'form':bound_form,#'station':station,
                                    'neighs':bound_form_st['neighbours'].as_widget(forms.CheckboxSelectMultiple(choices=query_n)),
                                    'neighs_add':bound_form_st['neighbours_add'].as_widget(forms.CheckboxSelectMultiple(choices=query_add))})


            

    
class RailwayStationsDetailViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/railway_stations_detail.html'

    def get(self, request,pk):
      
        station=get_object_or_404(RailwayStations,id=pk)
        serializer=RailwayStationsSerializer(station)
        if RailwayStationsTrains.objects.filter(station=station).exists():
            st=RailwayStationsTrains.objects.get(station=station)   
            return Response({'station':station,'st':st,'trains':st.trains.all()})
        return Response({'station':station})

class RailwayStationsDeleteViewFront(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        station=get_object_or_404(RailwayStations,id=pk)
        serializer=RailwayStationsSerializer(station)
        return render(request,'railway/railway_stations_delete.html',{'station':station})
    def post(self, request,pk):
      
        station=get_object_or_404(RailwayStations,id=pk)
        station.delete()
        cache.set('stations','')
        return redirect('railway_stations_url')

class RailwayStationsUpdateTrainsViewFront(LoginRequiredMixin,View):
    def get(self, request,pk):
      
        station=get_object_or_404(RailwayStations,id=pk)
        st=RailwayStationsTrains.objects.update_or_create(station=station)
        form=RailwayStationsTrainsUpdateForm(instance=st[0])
        return render(request,'railway/railway_stations_update_trains.html',{'station':station,'st':st[0],'form':form})
    
    def post(self, request,pk):
        station=get_object_or_404(RailwayStations,id=pk)
        st=RailwayStationsTrains.objects.update_or_create(station=station)
        bound_form=form=RailwayStationsTrainsUpdateForm(request.POST,instance=st[0],initial={'station':st[0]})
        new_st=bound_form.save()
        new_st.update_trains()
        r=new_st.update_trains()
        new_st.save()
        return redirect('railway_stations_url')
        #return render(request,'railway/railway_stations_update_trains.html',{'station':station,'s':r})
       
        
        
""" CRUD,LIST --Поезда """

class TrainsListViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/trains_list.html'
    

    def get(self,request):
        trains=cache.get('trains')
        if not trains:
            trains=Trains.objects.all()
            cache.set('trains',trains,10)
        paginator=Paginator(trains,15)
        page=request.GET.get('page')
        try:
            trains=paginator.page(page)
        except PageNotAnInteger:
            trains=paginator.page(1)
        except EmptyPage:
            trains=paginator.page(paginator.num_pages)
        
        serializer=TrainsSerializer(trains,many=True)
        return Response({'trains':trains, 'page':page})


class TrainCreateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/train_create.html'


    def get(self,request):
        serializer=TrainsSerializer()
        return Response({'serializer':serializer})

    def post(self, request):
        serializer=TrainsSerializer(data=request.data)
        if serializer.is_valid():
            train=serializer.create(request.data)          
            stats=RailwayStations.objects.filter(id__in=serializer.data['stations'])
            train[0].stations.set(stats)
            train[0].save()
            for station in RailwayStationsTrains.objects.filter(Q(station__in=stats)|Q(station=train[0].train_begin)|Q(station=train[0].train_end)):
                station.trains.add(train[0])
                station.save()
        return redirect('trains_url')
        
class TrainUpdateViewFront(LoginRequiredMixin,APIView):


    def get(self,request,pk):
        train=get_object_or_404(Trains,id=pk)
        query=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s in train.stations.all()]
        query_add=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s not in train.stations.all() and  s!=train.train_begin and s!=train.train_end]
        form=TrainsUpdateForm(instance=train)#, initial={'city':station.city})
        form_st=TrainStationsUpdateForm()
        
        return render(request,'railway/train_update.html',{'form':form,
                                    'stations':form_st['stations'].as_widget(forms.CheckboxSelectMultiple(choices=query)),
                                    'stations_add':form_st['stations_add'].as_widget(forms.CheckboxSelectMultiple(choices=query_add))})

    def post(self, request,pk):
        train=get_object_or_404(Trains,id=pk)
        query=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s in train.stations.all()]
        query_add=[(s.id,f'{s.name} -{s.city}') for s in RailwayStations.objects.all() if s not in train.stations.all() and  s!=train.train_begin and s!=train.train_end]
        bound_form=TrainsUpdateForm(request.POST,instance=train)
        bound_form_st=TrainStationsUpdateForm(request.POST)
        new_stations=[st for st in RailwayStations.objects.filter(id__in=bound_form_st['stations_add'].value())]
        new_stations1=[st for st in RailwayStations.objects.filter(id__in=bound_form_st['stations'].value())]
        new_stations.extend([st for st in train.stations.all()
                                    if st not in [st for st in RailwayStations.objects.filter(id__in=bound_form_st['stations'].value())]])
        if bound_form.is_valid():
            new_train=bound_form.save()
            new_train.stations.set(new_stations)
            new_train.save()
            for station in RailwayStationsTrains.objects.filter(Q(station__in=new_stations)|Q(station=new_train.train_begin)|Q(station=new_train.train_end)):
                station.trains.add(new_train)
                station.save()
            for station in RailwayStationsTrains.objects.filter(Q(station__in=new_stations1)|Q(station=new_train.train_begin)|Q(station=new_train.train_end)):
                station.trains.remove(new_train)
                station.save() 
            return redirect('trains_url')
        else:
            return render(request,'railway/train_update.html',{'form':bound_form,
                                    'stations':bound_form_st['stations'].as_widget(forms.CheckboxSelectMultiple(choices=query)),
                                    'stations_add':bound_form_st['stations-add'].as_widget(forms.CheckboxSelectMultiple(choices=query_add))})

    
class TrainDetailViewFront(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        train=get_object_or_404(Trains,id=pk)
        form=TrainTicketsForm()
        return render(request,'railway/train_detail.html',{'train':train,'form':form})

class TrainTicketsBought(LoginRequiredMixin,View):

    def get(self,request,pk):
        if request.GET:
            form=TrainTicketsForm(request.GET)
            train=get_object_or_404(Trains,id=pk)

            date_lst=request.GET['date'].split('-')
            trains=ScheduleTrains.objects.filter(train=train,date_train=request.GET['date'], time_train=request.GET['time'])
            date_lst=form['date'].value().split('-')
            time_lst=form['time'].value().split(':')
            tickets=Ticket.objects.filter(date_start=datetime(int(date_lst[0]),int(date_lst[1]),int(date_lst[2]),int(time_lst[0]),int(time_lst[1]),int(time_lst[2])),
                                          train=train)
            paginator=Paginator(tickets,15)
            page=request.GET.get('page')
            try:
                tickets=paginator.page(page)
            except PageNotAnInteger:
                tickets=paginator.page(1)
            except EmptyPage:
                tickets=paginator.page(paginator.num_pages)
            return render(request,'railway/tickets_list.html',{'tickets':tickets,'page':page})
        else:
            train=get_object_or_404(Trains,id=pk)
            form=TrainTicketsForm()
            query=list(set([(tr.time_train,tr.time_train) for tr in ScheduleTrains.objects.filter(train=train)]))
            return render(request,'railway/tickets_bought.html',{'train':train,'form':form,
                                                        'time':form['time'].as_widget(forms.Select(choices=query))})
            
        


class TrainDeleteViewFront(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        train=get_object_or_404(Trains,id=pk)
        serializer=TrainsSerializer(train)
        return render(request,'railway/train_delete.html',{'train':train})
    def post(self, request,pk):
      
        train=get_object_or_404(Trains,id=pk)
        train.delete()
        cache.set('trains','')
 
        return redirect('trains_url')

""" CRUD,LIST --Билеты """

class TicketsListViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/tickets_list.html'
    

    def get(self,request):
        trains=cache.get('tickets')
        if not trains:
            tickets=Ticket.objects.all()
            cache.set('tickets',trains,10)
        paginator=Paginator(tickets,15)
        page=request.GET.get('page')
        try:
            tickets=paginator.page(page)
        except PageNotAnInteger:
            tickets=paginator.page(1)
        except EmptyPage:
            tickets=paginator.page(paginator.num_pages)
        
        serializer=TicketSerializer(tickets,many=True)
        return Response({'tickets':tickets, 'page':page})

class TicketsChoiceViewFront(LoginRequiredMixin,View):
  

    def get(self,request,pk):
        train=Trains.objects.get(id=pk)
        form=TicketChoiceForm()
        form_tr=TrainChoiceForm()
        query_st=[(train.train_begin.id,f'{train.train_begin.name}-{train.train_begin.city}'),(train.train_end.id,f'{train.train_end.name}-{train.train_end.city}')]
        query_st.extend([(st.id,f'{st.name}-{st.city}') for st in train.stations.all()])
        
        query=[(tr.time_train,f'{tr.time_train}') for tr in ScheduleTrains.objects.filter(train=train)]
        #отбор по дате
        return render(request,'railway/tickets_choice.html',{'form':form,'train':train,
                                                             'start':form['start'].as_widget(forms.Select(choices=query_st)),
                                                             'finish':form['finish'].as_widget(forms.Select(choices=query_st)),
                                                             'date_train':form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                                                             'choice_train':form_tr['time_train'].as_widget(forms.Select(choices=query))})
    def post(self,request,pk):
        train=Trains.objects.get(id=pk)
        
        bound_form=TicketChoiceForm(request.POST)
        bound_form_tr=TrainChoiceForm(request.POST)
        sch_train=ScheduleTrains.objects.get(train=train, date_train=request.POST['date_train'], time_train=request.POST['time_train'])
        query_st=[(train.train_begin.id,f'{train.train_begin.name}-{train.train_begin.city}'),(train.train_end.id,f'{train.train_end.name}-{train.train_end.city}')]
        query_st.extend([(st.id,f'{st.name}-{st.city}') for st in train.stations.all()])
        query=[(tr.time_train,f'{tr.time_train}') for tr in ScheduleTrains.objects.filter(train=train)]
        gr=WeightedGraph(train.get_distance_beatween_stations())
        for station in train.get_distance_beatween_stations():
            for neigh in station.neighbours.all():
                if neigh in train.get_distance_beatween_stations():
                    if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
                        dist=NeighboursDistance.objects.get(start=station, finish=neigh)
                        gr.add_edge_by_vertices(station,neigh,dist.distance)
                    elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
                        dist=NeighboursDistance.objects.get(finish=station, start=neigh)
                        gr.add_edge_by_vertices(station,neigh,dist.distance)
                    else:
                        gr.add_edge_by_vertices(station,neigh,0)
        
        if bound_form.is_valid():
            new_ticket=bound_form.save()
            new_ticket.train=sch_train
            date_lst=bound_form_tr['date_train'].value().split('-')
            time_lst=bound_form_tr['time_train'].value().split(':')
            new_ticket.date_start=datetime(int(date_lst[0]),int(date_lst[1]),int(date_lst[2]),int(time_lst[0]),int(time_lst[1]),int(time_lst[2]))
            #bound_form_tr['date_train'].value()#+timedelta(hours=7, minutes=0)
            start=new_ticket.start
            finish=new_ticket.finish
            distances, path_dict=dijkstra(gr,start)
            if gr.index_of(start)==gr.index_of(finish):
                return render(request,'railway/tickets_choice.html',{'form':bound_form,'train':train,
                            'start':bound_form['start'].as_widget(forms.Select(choices=query_st)),
                            'finish':bound_form['finish'].as_widget(forms.Select(choices=query_st)),
                            'date_train':bound_form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                            'choice_train':bound_form_tr['time_train'].as_widget(forms.Select(choices=query)),
                           'message':f'Станция отправки и прибытия совпадают'})
                
            path=path_dict_to_path(gr.index_of(start),gr.index_of(finish), path_dict)
            
            tic_rank=TicketRanks.objects.get(rank=new_ticket.rank)
            new_ticket.price=settings.PRICE_FOR_KM*total_weight(path)*tic_rank.koef
            
            new_ticket.save()
            ## Если нет такого поезда
            sch_train=ScheduleTrains.objects.get(date_train=bound_form_tr['date_train'].value(),train=train)
            temp=sch_train.tickets.split(':')
            if str((new_ticket.carriage,new_ticket.place)) not in temp:
                return render(request,'railway/tickets_choice.html',{'form':bound_form,'train':train,
                            'start':bound_form['start'].as_widget(forms.Select(choices=query_st)),
                            'finish':bound_form['finish'].as_widget(forms.Select(choices=query_st)),
                            'date_train':bound_form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                            'choice_train':bound_form_tr['time_train'].as_widget(forms.Select(choices=query)),
                            'message':f'Билет: Вагон№ {new_ticket.carriage}-Место№ {new_ticket.place} уже куплен'})
                
            temp.remove(str((new_ticket.carriage,new_ticket.place)))
            sch_train.tickets=':'.join([str(t) for t in temp])
            sch_train.save()
            cart_ticket_form=CartAddTicketForm()
            return  render(request,'railway/ticket_add_cart.html',{'ticket':new_ticket,'cart_ticket_form':cart_ticket_form})
            #redirect(new_ticket)
        else:
            return render(request,'railway/tickets_choice.html',{'form':bound_form,'train':train,
                            'start':bound_form['start'].as_widget(forms.Select(choices=query_st)),
                            'finish':bound_form['finish'].as_widget(forms.Select(choices=query_st)),
                           'date_train':bound_form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                            'choice_train':bound_form_tr['time_train'].as_widget(forms.Select(choices=query)),
                            'message':f'Проверьте данные'})
    

class BookedTicketsViewFront(LoginRequiredMixin,View):
  

    def get(self,request,pk):
        train=Trains.objects.get(id=pk)
        form=TicketChoiceForm()
        form_tr=TrainChoiceForm()
        query_st=[(train.train_begin.id,f'{train.train_begin.name}-{train.train_begin.city}'),(train.train_end.id,f'{train.train_end.name}-{train.train_end.city}')]
        query_st.extend([(st.id,f'{st.name}-{st.city}') for st in train.stations.all()])
        
        query=[(tr.time_train,f'{tr.time_train}') for tr in ScheduleTrains.objects.filter(train=train)]
        #отбор по дате
        return render(request,'railway/tickets_booked.html',{'form':form,'train':train,
                                                             'start':form['start'].as_widget(forms.Select(choices=query_st)),
                                                             'finish':form['finish'].as_widget(forms.Select(choices=query_st)),
                                                             'date_train':form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                                                             'choice_train':form_tr['time_train'].as_widget(forms.Select(choices=query))})
    def post(self,request,pk):
        train=Trains.objects.get(id=pk)
        
        bound_form=TicketChoiceForm(request.POST)
        bound_form_tr=TrainChoiceForm(request.POST)
        sch_train=ScheduleTrains.objects.get(train=train, date_train=request.POST['date_train'], time_train=request.POST['time_train'])
        query_st=[(train.train_begin.id,f'{train.train_begin.name}-{train.train_begin.city}'),(train.train_end.id,f'{train.train_end.name}-{train.train_end.city}')]
        query_st.extend([(st.id,f'{st.name}-{st.city}') for st in train.stations.all()])
        query=[(tr.time_train,f'{tr.time_train}') for tr in ScheduleTrains.objects.filter(train=train)]
        gr=WeightedGraph(train.get_distance_beatween_stations())
        for station in train.get_distance_beatween_stations():
            for neigh in station.neighbours.all():
                if neigh in train.get_distance_beatween_stations():
                    if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
                        dist=NeighboursDistance.objects.get(start=station, finish=neigh)
                        gr.add_edge_by_vertices(station,neigh,dist.distance)
                    elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
                        dist=NeighboursDistance.objects.get(finish=station, start=neigh)
                        gr.add_edge_by_vertices(station,neigh,dist.distance)
                    else:
                        gr.add_edge_by_vertices(station,neigh,0)
        
        if bound_form.is_valid():
            new_ticket=bound_form.save()
            new_ticket.train=sch_train
            date_lst=bound_form_tr['date_train'].value().split('-')
            time_lst=bound_form_tr['time_train'].value().split(':')
            new_ticket.date_start=datetime(int(date_lst[0]),int(date_lst[1]),int(date_lst[2]),int(time_lst[0]),int(time_lst[1]),int(time_lst[2]))
            #bound_form_tr['date_train'].value()#+timedelta(hours=7, minutes=0)
            start=new_ticket.start
            finish=new_ticket.finish
            distances, path_dict=dijkstra(gr,start)
            if gr.index_of(start)==gr.index_of(finish):
                return render(request,'railway/tickets_booked.html',{'form':bound_form,'train':train,
                            'start':bound_form['start'].as_widget(forms.Select(choices=query_st)),
                            'finish':bound_form['finish'].as_widget(forms.Select(choices=query_st)),
                            'date_train':bound_form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                            'choice_train':bound_form_tr['time_train'].as_widget(forms.Select(choices=query)),
                           'message':f'Станция отправки и прибытия совпадают'})
                
            path=path_dict_to_path(gr.index_of(start),gr.index_of(finish), path_dict)
            
            tic_rank=TicketRanks.objects.get(rank=new_ticket.rank)
            new_ticket.price=settings.PRICE_FOR_KM*total_weight(path)*tic_rank.koef
            new_ticket.booked=True
            new_ticket.save()
            sch_train=ScheduleTrains.objects.get(date_train=bound_form_tr['date_train'].value(),train=train)
            temp=sch_train.tickets.split(':')
            if str((new_ticket.carriage,new_ticket.place)) not in temp:
                return render(request,'railway/tickets_booked.html',{'form':bound_form,'train':train,
                            'start':bound_form['start'].as_widget(forms.Select(choices=query_st)),
                            'finish':bound_form['finish'].as_widget(forms.Select(choices=query_st)),
                            'date_train':bound_form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                            'choice_train':bound_form_tr['time_train'].as_widget(forms.Select(choices=query)),
                            'message':f'Билет: Вагон№ {new_ticket.carriage}-Место№ {new_ticket.place} уже куплен или забронирован'})
                
            temp.remove(str((new_ticket.carriage,new_ticket.place)))
            sch_train.tickets=':'.join([str(t) for t in temp])
            sch_train.save()
            cart_ticket_form=CartAddTicketForm()
            return  render(request,'railway/ticket_add_cart.html',{'ticket':new_ticket,'cart_ticket_form':cart_ticket_form})
            #redirect(new_ticket)
        else:
            return render(request,'railway/tickets_booked.html',{'form':bound_form,'train':train,
                            'start':bound_form['start'].as_widget(forms.Select(choices=query_st)),
                            'finish':bound_form['finish'].as_widget(forms.Select(choices=query_st)),
                           'date_train':bound_form_tr['date_train'].as_widget(forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'})),
                            'choice_train':bound_form_tr['time_train'].as_widget(forms.Select(choices=query)),
                            'message':f'Проверьте данные'})
    

class TicketCreateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/ticket_create.html'


    def get(self,request):
        serializer=TicketSerializer()
        return Response({'serializer':serializer})

    def post(self, request):
        serializer=TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket=serializer.create(request.data)          
            ticket[0].save()
          
        return redirect('tickets_url')

        
class TicketUpdateViewFront(LoginRequiredMixin,APIView):


    def get(self,request,pk):
        ticket=get_object_or_404(Ticket,id=pk)
        form=TicketUpdateForm(instance=ticket)                
        return render(request,'railway/ticket_update.html',{'form':form})
    def post(self, request,pk):
        ticket=get_object_or_404(Ticket,id=pk)
        bound_form=TicketUpdateForm(request.POST,instance=ticket)
        if bound_form.is_valid():
            new_ticket=bound_form.save()
            return redirect(new_ticket)
        else:
            return render(request,'railway/ticket_update.html',{'form':bound_form})


class TicketDetailViewFront(LoginRequiredMixin,APIView):

    def get(self, request,pk):      
        ticket=get_object_or_404(Ticket,id=pk)
        order=OrderItem.objects.get(ticket=ticket)
        
        #cart_ticket_form=CartAddTicketForm()
        return render(request, 'railway/ticket_detail.html',{'ticket':ticket,'order':order})

class TicketDeleteViewFront(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        ticket=get_object_or_404(Ticket,id=pk)
        serializer=TicketSerializer(ticket)
        return render(request,'railway/ticket_delete.html',{'ticket':ticket})
    def post(self, request,pk):
      
        ticket=get_object_or_404(Ticket,id=pk)
        ticket.delete()
        cache.set('tickets','')
 
        return redirect('tickets_url')


##class BookedTicketsListViewFront(LoginRequiredMixin,APIView):
##    renderer_classes = [TemplateHTMLRenderer]
##    template_name = 'railway/tickets_list.html'
##    
##
##    def get(self,request):
##        trains=cache.get('tickets')
##        if not trains:
##            tickets=Ticket.objects.all()
##            cache.set('tickets',trains,10)
##        paginator=Paginator(tickets,15)
##        page=request.GET.get('page')
##        try:
##            tickets=paginator.page(page)
##        except PageNotAnInteger:
##            tickets=paginator.page(1)
##        except EmptyPage:
##            tickets=paginator.page(paginator.num_pages)
##        
##        serializer=TicketSerializer(tickets,many=True)
##        return Response({'tickets':tickets, 'page':page})
##    

""" CRUD,LIST --Ранги билетов """

class TicketRanksListViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/ticketranks_list.html'
    

    def get(self,request):
        ticketranks=cache.get('ticketranks')
        if not ticketranks:
            ticketranks=TicketRanks.objects.all()
            cache.set('ticketranks',ticketranks,10)
        paginator=Paginator(ticketranks,15)
        page=request.GET.get('page')
        try:
            ticketranks=paginator.page(page)
        except PageNotAnInteger:
            ticketranks=paginator.page(1)
        except EmptyPage:
            ticketranks=paginator.page(paginator.num_pages)
        
        serializer=TicketRanksSerializer(ticketranks,many=True)
        return Response({'ticketranks':ticketranks, 'page':page})


class TicketRankCreateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/ticketrank_create.html'


    def get(self,request):
        serializer=TicketRanksSerializer()
        return Response({'serializer':serializer})

    def post(self, request):
        serializer=TicketRanksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
          
        return redirect('ticketranks_url')
    
class TicketRankUpdateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/ticketrank_update.html'


    def get(self,request,pk):
        ticketrank=TicketRanks.objects.get(id=pk)
        serializer=TicketRanksSerializer(ticketrank)
        return Response({'serializer':serializer,'ticketrank':ticketrank})

    def post(self, request,pk):
        ticketrank=get_object_or_404(TicketRanks,id=pk)
        serializer=TicketRanksSerializer(ticketrank,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('ticketranks_url')
        
class TicketRankUpdateViewFront(LoginRequiredMixin,APIView):


    def get(self,request,pk):
        ticketrank=get_object_or_404(TicketRanks,id=pk)      
        form=TicketRankstUpdateForm(instance=ticketrank)
        return render(request,'railway/ticketrank_update.html',{'form':form})

    def post(self, request,pk):
        ticket=get_object_or_404(TicketRanks,id=pk)
        bound_form=TicketRanksUpdateForm(request.POST,instance=ticket)
        if bound_form.is_valid():
            new_ticket=bound_form.save()
            return redirect(new_ticket)#'tickets_url')
        else:
            return render(request,'railway/ticketrank_update.html',{'form':bound_form})

    
class TicketRankDetailViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/ticketrank_detail.html'

    def get(self, request,pk):
      
        ticketrank=get_object_or_404(TicketRanks,id=pk)
        serializer=TicketRanksSerializer(ticketrank)
        return Response({'ticketrank':ticketrank})#.name:[s['name'] for s in serializer.data]})

class TicketRankDeleteViewFront(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        ticketrank=get_object_or_404(TicketRanks,id=pk)
        serializer=TicketRanksSerializer(ticketrank)
        return render(request,'railway/ticketrank_delete.html',{'ticketrank':ticketrank})
    def post(self, request,pk):
      
        ticketrank=get_object_or_404(TicketRanks,id=pk)
        ticketrank.delete()
        cache.set('ticketranks','')
 
        return redirect('ticketranks_url')


            

            

        
        
