from typing import List
from .graph import WeightedEdge, WeightedGraph
from .priority_queue import PriorityQueue
from railway.models import Trains, TrainStatus, RailwayStationsTrains

from django.db.models import Q

WeightedPath=List[WeightedEdge]

def total_weight(wp):
    return sum([e.weight for e in wp])

def mst(wg,start):
    if start>(wg.vertex_count-1) or start<0:
        return None
    result=[]
    pq=PriorityQueue()
    visited=[False]*wg.vertex_count

    def visit(index):
        visited[index]=True
        for edge in wg.edges_for_index(index):
            if not visited[edge.v]:
                pq.push(edge)
    visit(start)

    while not pq.empty:
        edge=pq.pop()
        if visited[edge.v]:
            continue
        result.append(edge)
        visit(edge.v)
        return result

def print_weighted_path(wg,wp):
    for edge in wp:
        print(f'{wg.vertex_at(edge.u)} {edge.weight}>{wg.vertex_at(edge.v)}')

    print(f'Total weigth:{total_weight(wp)}')
    
               
def dict_weighted_path(wg,wp):
    path_dict={}
    for edge in wp:
        key, value= f'{wg.vertex_at(edge.u)}->{wg.vertex_at(edge.v)}',edge.weight
        path_dict[key]=value
#(wg.vertex_at(edge.u),wg.vertex_at(edge.v)), edge.weight#
    return path_dict      

def get_trains(wg,wp):
    trains_dict={}
    for edge in wp:
        for train in Trains.objects.all():
            if train.train_begin==wg.vertex_at(edge.u):
                if train.train_end==wg.vertex_at(edge.v) or wg.vertex_at(edge.v) in train.stations.all():
                    status=TrainStatus.objects.get(name=train.status)
                    key, value=train, round(edge.weight/status.speed,2)
                    trains_dict[key]=value
            elif train.train_end==wg.vertex_at(edge.v):
                if train.train_begin==wg.vertex_at(edge.u) or wg.vertex_at(edge.u) in train.stations.all():
                    status=TrainStatus.objects.get(name=train.status)
                    key, value=train, round(edge.weight/status.speed,2) 
                    trains_dict[key]=value
            elif wg.vertex_at(edge.u) in train.stations.all():# or wg.vertex_at(edge.v) in train.stations.all():
                status=TrainStatus.objects.get(name=train.status)
                key, value=train, round(edge.weight/status.speed,2) 
                trains_dict[key]=value
        #if len(trains_dist)<i+1:
    return trains_dict

def get_optimum_trains(wg,wp):
    tr_d=[]
    trains_graph_list=[]
    trains_graph_list.append(wg.vertex_at(wp[0].u))
    for edge in wp:
        if wg.vertex_at(edge.v) not in trains_graph_list:
            trains_graph_list.append(wg.vertex_at(edge.v))
    train_graph=WeightedGraph(trains_graph_list)
    for i in range(len(trains_graph_list)):
        if RailwayStationsTrains.objects.filter(station=trains_graph_list[i]).exists():
            tr_d.append(trains_graph_list[i])
            tr_d.append(i)
            st=RailwayStationsTrains.objects.get(station=trains_graph_list[i])
            tr_d.append("TRAINS")
            tr_d.append(st.trains.all())
            tr_d.append("!!!")
            for j in range(i+1,len(trains_graph_list)): 
                tr_d.append(trains_graph_list[j])
                tr_d.append(j)
                if RailwayStationsTrains.objects.filter(station=trains_graph_list[j]).exists():
                    st_1=RailwayStationsTrains.objects.get(station=trains_graph_list[j])
                    tr_d.append("TRAINS")
                    tr_d.append(st_1.trains.all())
                    tr_d.append("!!!")
                    for train in st.trains.all():
                        if train in st_1.trains.all():
                            if train not in tr_d:
                                tr_d.append(train)
                    
##                    for train in st.trains.filter(Q(train_begin=trains_graph_list[j])|Q(train_end=trains_graph_list[j])
##                                              |Q(trains_graph_list[j]__in=[st for st in train.stations.all()]):
##                    tr_d.append(trains_graph_list[j])
##                    tr_d.append(j)
##                    if Trains.objects.filter(Q(train_begin=trains_graph_list[j])|Q(train_end=trains_graph_list[j])
##                                             |Q(trains_graph_list[j]__in=stations.all())).exists():
##                        tr_d.append(Trains.objects.get(train_begin=trains_graph_list[i], train_end=trains_graph_list[j]))
                            train_graph.add_edge_by_vertices(trains_graph_list[i],trains_graph_list[j],1)
        
    return train_graph,trains_graph_list
##def get_trains(wg,wp):
##    trains_dict={}
##    for train in Trains.objects.all():
##        if train.train_begin==wg.vertex_at(wp[0].u):
##            if train.train_end==wg.vertex_at(wp[-1].v) or wg.vertex_at(wp[-1].v) in train.stations.all():
##                status=TrainStatus.objects.get(name=train.status)
##                key, value=train, round(total_weight(wp)/status.speed,2)
##                trains_dict[key]=value
##        elif train.train_end==wg.vertex_at(wp[-1].v):
##            if train.train_begin==wg.vertex_at(wp[0].u) or wg.vertex_at(wp[0].u) in train.stations.all():
##                status=TrainStatus.objects.get(name=train.status)
##                key, value=train, round(total_weight(wp)/status.speed,2) 
##                trains_dict[key]=value
##        elif wg.vertex_at(wp[0].u) in train.stations.all() and wg.vertex_at(wp[-1].v) in train.stations.all():
##            status=TrainStatus.objects.get(name=train.status)
##            key, value=train, round(total_weight(wp)/status.speed,2) 
##            trains_dict[key]=value
##    return trains_dict
