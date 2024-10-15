from django.shortcuts import render,get_object_or_404, redirect
from django.shortcuts import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics

from railway.models import RailwayStations, TrainStatus,RailwayStationsTrains
from .forms import ChoiceRouteForm
from .models import NeighboursDistance
from .serializers import NeighboursDistanceSerializer,NeighboursDistanceCreateSerializer,NeighboursDistanceUpdateSerializer

from .dijkstra import *
from .graph import WeightedGraph


def sec_to_time(minuts):
    
    hr,mn=divmod(minuts,60)
    return f'{hr}:{mn}'


@api_view()
def get_graph(request):
    adict={}
    new_graph=WeightedGraph([st for st in RailwayStations.objects.all()])
    for station in [st for st in RailwayStations.objects.all()]:
            for neigh in station.neighbours.all():
                new_graph.add_edge_by_vertices(station,neigh,0)
    for i in range(new_graph.vertex_count):
        key, value=new_graph.vertex_at(i), new_graph.neighbors_for_index(i)
        adict[key]=value
    return Response(f'{adict}')  
   
    
    
class GraphView(View):
    def get(self,request):
        new_graph=Graph(RailwayStations.objects.all())
        return render(request, 'routes/graph_list.html',{'edges':new_graph})
        
class WeightedGraphView(View):
    def get(self,request):
        new_graph1=WeightedGraph([st for st in RailwayStations.objects.all()])
        for station in [st for st in RailwayStations.objects.all()]:
            st=RailwayStationsTrains.objects.get(station=station)
            for neigh in station.neighbours.all():
                if RailwayStationsTrains.objects.filter(station=neigh).exists():
                    st_1=RailwayStationsTrains.objects.get(station=neigh)
                    for train in st.trains.all():
                        if train in st_1.trains.all():
                
                            if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
                                dist=NeighboursDistance.objects.get(start=station, finish=neigh)
                                new_graph1.add_edge_by_vertices(station,neigh,dist.distance)
                            elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
                                dist=NeighboursDistance.objects.get(finish=station, start=neigh)
                                new_graph1.add_edge_by_vertices(station,neigh,dist.distance)
                            else:
                                new_graph1.add_edge_by_vertices(station,neigh,0)
        new_graph=WeightedGraph([st for st in RailwayStations.objects.all()])
        for station in [st for st in RailwayStations.objects.all()]:

            for neigh in station.neighbours.all():
 
                if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
                    dist=NeighboursDistance.objects.get(start=station, finish=neigh)
                    new_graph.add_edge_by_vertices(station,neigh,dist.distance)
                elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
                    dist=NeighboursDistance.objects.get(finish=station, start=neigh)
                    new_graph.add_edge_by_vertices(station,neigh,dist.distance)
                else:
                    new_graph.add_edge_by_vertices(station,neigh,0)
    
                
    
        return render(request, 'routes/weighted_graph_list.html',{'graph':new_graph,'s':new_graph1})
    
class RoutesByDistanceView(View):
    def get(self,request):
        new_graph=WeightedGraph([st for st in RailwayStations.objects.all()])
        for station in [st for st in RailwayStations.objects.all()]:
            for neigh in station.neighbours.all():
                if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
                    dist=NeighboursDistance.objects.get(start=station, finish=neigh)
                    new_graph.add_edge_by_vertices(station,neigh,dist.distance)
                elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
                    dist=NeighboursDistance.objects.get(finish=station, start=neigh)
                    new_graph.add_edge_by_vertices(station,neigh,dist.distance)
                else:
                    new_graph.add_edge_by_vertices(station,neigh,0)

        new_graph1=WeightedGraph([st for st in RailwayStations.objects.all()])
        for station in [st for st in RailwayStations.objects.all()]:
            st=RailwayStationsTrains.objects.get(station=station)
            for neigh in station.neighbours.all():
                if RailwayStationsTrains.objects.filter(station=neigh).exists():
                    st_1=RailwayStationsTrains.objects.get(station=neigh)
                    for train in st.trains.all():
                        if train in st_1.trains.all():
                
                            if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
                                dist=NeighboursDistance.objects.get(start=station, finish=neigh)
                                new_graph1.add_edge_by_vertices(station,neigh,dist.distance)
                            elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
                                dist=NeighboursDistance.objects.get(finish=station, start=neigh)
                                new_graph1.add_edge_by_vertices(station,neigh,dist.distance)
                            else:
                                new_graph1.add_edge_by_vertices(station,neigh,0)
        if request.GET:
            form=ChoiceRouteForm(request.GET)
            if form['start'].value()==form['finish'].value():
                form=ChoiceRouteForm()
                context={'form':form}
                return render(request, 'routes/routes_list.html',context=context)
            
            
            start=RailwayStations.objects.get(id=form['start'].value())
            finish=RailwayStations.objects.get(id=form['finish'].value())
            distances, path_dict=dijkstra(new_graph,start)
            #name_distance=distance_array_to_vertex_dict(new_graph,distances)
            

            path=path_dict_to_path(new_graph.index_of(start),new_graph.index_of(finish), path_dict)
            distances_1, path_dict_1=dijkstra(get_optimum_trains(new_graph1,path)[0],get_optimum_trains(new_graph1,path)[1][0])
            path_train=path_dict_to_path(get_optimum_trains(new_graph1,path)[0].index_of(get_optimum_trains(new_graph1,path)[1][0]),
                                         get_optimum_trains(new_graph1,path)[0].index_of(get_optimum_trains(new_graph1,path)[1][-1]), path_dict_1)
    #
            name_distance=distance_array_to_vertex_dict(new_graph1,distances_1)
            context={'form':form,
                     'get_trains':get_trains(new_graph,path),
##                     's':(get_optimum_trains(new_graph1,path)[1],distances_1,total_weight(path_train),name_distance),#dict_weighted_path(get_optimum_trains(new_graph,path)[1],path_train),
##                     's1':get_trains(new_graph, path),
                     'start':start,
                     'finish':finish,
                     'graph':new_graph,
                     'path':dict_weighted_path(new_graph,path),
                     'all_distance':total_weight(path)#sum([value for value in dict_weighted_path(new_graph,path).values()]),
                     }
            return render(request, 'routes/routes_list.html',context=context)
        else:
            form=ChoiceRouteForm()
            context={'form':form}
            return render(request, 'routes/routes_list.html',context=context)

            
class RailwayStationsDistancesView(View):
    def get(self,request,pk):
        new_graph=WeightedGraph([st for st in RailwayStations.objects.all()])
        for station in [st for st in RailwayStations.objects.all()]:
            for neigh in station.neighbours.all():
                if NeighboursDistance.objects.filter(start=station, finish=neigh).exists():
                    dist=NeighboursDistance.objects.get(start=station, finish=neigh)
                    new_graph.add_edge_by_vertices(station,neigh,dist.distance)
                elif  NeighboursDistance.objects.filter(finish=station, start=neigh).exists() :
                    dist=NeighboursDistance.objects.get(finish=station, start=neigh)
                    new_graph.add_edge_by_vertices(station,neigh,dist.distance)
                else:
                    new_graph.add_edge_by_vertices(station,neigh,0)
        station=RailwayStations.objects.get(id=pk)
        distances, path_dict=dijkstra(new_graph,station)
        name_distance=distance_array_to_vertex_dict(new_graph,distances)
        context={'name_distance':name_distance,
                 'station':station}
        return render(request, 'railway/railway_stations_distances.html',context=context)

""" Frontend """

""" CRUD, List- NeighboursDistance """

class NeighboursDistanceListViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'routes/neighbours_distance_list.html'
    
    
    def get(self,request):
        neighbours_distance=cache.get('neighbours_distance')
        if not neighbours_distance:
            neighbours_distance=NeighboursDistance.objects.all()
            cache.set('neighbours_distance',neighbours_distance,10)
        paginator=Paginator(neighbours_distance,10)
        page=request.GET.get('page')
        try:
            neighbours_distance=paginator.page(page)
        except PageNotAnInteger:
            neighbours_distance=paginator.page(1)
        except EmptyPage:
            neighbours_distance=paginator.page(paginator.num_pages)
        
        serializer=NeighboursDistanceSerializer(neighbours_distance,many=True)
        return Response({'neighbours_distance':neighbours_distance, 'page':page})


class NeighboursDistanceCreateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'railway/city_create.html'


    def get(self,request):
        serializer=NeighboursDistanceCreateSerializer()
        return Response({'serializer':serializer})

    def post(self, request):
        start=RailwayStations.objects.get(id=request.data['start'])
        finish=RailwayStations.objects.get(id=request.data['finish'])
        if not NeighboursDistance.objects.filter(start=start,finish=finish).exists():
            serializer=NeighboursDistanceCreateSerializer(data=request.data)
            if serializer.is_valid():
                distance=serializer.create(request.data)
                #serializer.save()      
                distance.start=start
                distance.finish=finish
                distance.save()
            return redirect('neighbours_distance_url')
        else:
            serializer=NeighboursDistanceCreateSerializer()
            return Response({'serializer':serializer})
        
class NeighboursDistanceUpdateViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'routes/neighbours_distance_update.html'

    def get(self,request,pk):
        neighbours_distance=get_object_or_404(NeighboursDistance,id=pk)      
        serializer=NeighboursDistanceUpdateSerializer()
        return Response({'serializer':serializer})
                      
    def post(self, request,pk):
        neighbours_distance=get_object_or_404(NeighboursDistance,id=pk)      
        serializer=NeighboursDistanceUpdateSerializer(neighbours_distance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('neighbours_distance_url')
        else:
            #neighbours_distance=get_object_or_404(NeighboursDistance,id=pk)      
            serializer=NeighboursDistanceUpdateSerializer()
            return Response({'serializer':serializer})
    
class NeighboursDistanceDetailViewFront(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'routes/neighbours_distance_detail.html'

    def get(self, request,pk):
      
        neighbours_distance=get_object_or_404(NeighboursDistance,id=pk)
        return Response({'neighbours_distance':neighbours_distance})  

class NeighboursDistanceDeleteViewFront(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        neighbours_distance=get_object_or_404(NeighboursDistance,id=pk)
        serializer=NeighboursDistanceSerializer(neighbours_distance)
        return render(request,'routes/neighbours_distance_delete.html',{'neighbours_distance':neighbours_distance})
    def post(self, request,pk):
      
        neighbours_distance=get_object_or_404(NeighboursDistance,id=pk)
        neighbours_distance.delete()
        cache.set('neighbours_distance','')
        return redirect('neighbours_distance_url')
