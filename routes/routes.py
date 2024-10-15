#https://github.com/appKODE/2018-internship-backend

from __future__ import annotations
from functools import reduce
from collections import deque
#from railway.models import RailwayStations

from dijkstra import *

from dataclasses import dataclass


@dataclass
class Edge:
    u: int # вершина "откуда"
    v: int # вершина "куда"
    def reversed(self) -> Edge:
        return Edge(self.v, self.u)
    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"

@dataclass
class WeightedEdge(Edge):
    weight:float

    def reversed(self):
        return WeightedEdge(self.v, self.u, self.weight)

    def __lt__(self, other):
        return self.weight<other.weight
    def __str__(self):
        return f'{self.u} {self.weight}->{self.v}'

    
class Graph:

    def __init__(self, vertices):

        self.vertices=vertices
        self.edges=[[] for _ in vertices]


    
    @property
    def vertex_count(self):
         return len(self.vertices)

    @property
    def egde_count(self):
        return sum(map(len,self.edges))

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
        self.edges.append([])
        return self.vertex_count-1

    def add_edge(self, edge):
        if edge not in self.edges[edge.u]:
            self.edges[edge.u].append(edge)
##        print(self.edges[edge.v], edge.reversed())
##        input()
        if edge.reversed() not in self.edges[edge.v]:
            self.edges[edge.v].append(edge.reversed())

    def add_edge_by_indices(self,u,v):
        edge=Edge(u,v)
        self.add_edges(edge)

    def add_edge_by_vertices(self, first, second):
        u=self.vertices.index(first)
        v=self.vertices.index(second)
        self.add_edge_by_indices(u,v)

    
    

    def vertex_at(self,index):
        return self.vertices[index]

    def index_of(self,vertex):
        return self.vertices.index(vertex)
    
    def neighbors_for_index(self,index):
        return list(map(self.vertex_at,[e.v for e in self.edges[index]]))

    def neighbors_for_vertex(self,vertex):
        return self.neighbors_for_index(self.index_of(vertex))

    def edges_for_index(self, index):
        return self.edges[index]

    def edges_for_vertex(self,vertex):
        return self.edges_for_index(self.index_of(vertex))

    def __str__(self):
        desc=''
        for i in range(self.vertex_count):
            desc+=f'{self.vertex_at(i)}->{self.neighbors_for_index(i)}\n'
        return desc

        

class WeightedGraph(Graph):

    def __init__(self, vertices):

        self.vertices=vertices
        self.edges=[[] for _ in vertices]

    def add_edge_by_indices(self,u,v,weight):
        edge=WeightedEdge(u,v,weight)
        self.add_edge(edge)

    def add_edge_by_vertices(self, first, second,weight):
        u=self.vertices.index(first)
        v=self.vertices.index(second)
        self.add_edge_by_indices(u,v,weight)

    def neighbors_for_index_with_weights(self,index):
        distance_tuples=[]
        for edge in self.edges_for_index(index):
            distance_tuples.append((self.vertex_at(edge.v),edge.weight))
        return distance_tuples
    
    def __str__(self):
        desc=''
        for i in range(self.vertex_count):
            desc+=f"{self.vertex_at(i)}->{self.neighbors_for_index_with_weights(i)}\n"
        return desc

class GraphMy:

##    def __init__(self, edges,n):
##        print(edges)
##        self.adjList=[[] for _ in range(n)]
##        for (scr,dest) in edges:
##            self.adjList[scr].append(dest)
##
##        print(self.adjList)
    def __init__(self, edges,n):
        print(edges)
        self.adjList=[[] for _ in range(n)]
        for (scr,dest) in edges:
            self.adjList[scr].append(dest)

        print(self.adjList)

    def printGraph(self):
        print(self.adjList)
        for scr in range(len(self.adjList)):
            print('scr',scr)
            input()
            print('lisr',self.adjList[scr])
            for dest in self.adjList[scr]:
                print('dest',dest)
                print(f'{scr}->{dest}',end='')

def get_edges(adict):
    return [item for sublist in [[(int(key),scr) for scr in value] for key, value in adict.items()] for item in sublist]
                
    
def check_relation(adict,first,second):
    #adict={}

##    for st in RailStations.objrcts.all():
##        key,value=st, st.get_neighbours.all()
####        l=adict.get(key,[])
####        l.append(value)
##        adict[key]=value
    print(adict)
    edges=[item for sublist in [[(key,scr) for scr in value] for key, value in adict.items()] for item in sublist]
    print(edges)
    search_queue=deque()
    print(search_queue)
    search_queue+=adict[first]
    searched=[]
    while search_queue:
        person=search_queue.popleft()
        if not person in searched:
            if person==second:
                searched.append(person)
                print(searched)
                return True
            else:
                search_queue+=adict[person]
                searched.append(person)
        
    return False


def main():
    adict= {
    "Харьков:Южный": [
        "Харьков:Левада",
        "Полтава:Центральный",
        "Днепропетровск:Центральный",
        "Запорожье:Центральный"
    ],
    "Харьков:Левада": [
        "Харьков:Южный",
        "Купянск:Купянск"
    ],
    "Киев:Центральный": [
        "Полтава:Центральный",
        "Одесса:Центральный",
        "Днепропетровск:Центральный",
        "Запорожье:Центральный",
        "Лубны:Лубны"
    ],
    "Полтава:Центральный": [
        "Харьков:Южный",
        "Киев:Центральный",
        "Лубны:Лубны"
    ],
    "Одесса:Центральный": [
        "Киев:Центральный",
        "Днепропетровск:Центральный"
    ],
    "Днепропетровск:Центральный": [
        "Харьков:Южный",
        "Киев:Центральный",
        "Одесса:Центральный",
        "Запорожье:Центральный"
    ],
    "Запорожье:Центральный": [
        "Харьков:Южный",
        "Киев:Центральный",
        "Днепропетровск:Центральный"
    ],
    "Лубны:Лубны": [
        "Киев:Центральный",
        "Полтава:Центральный"
    ],
    "Купянск:Купянск": [
        "Харьков:Левада"
    ]
    }
##    adict= {
##    "1": [
##        2,
##        4,
##        6,
##        7
##    ],
##    "2": [
##        1,
##        9
##    ],
##    "3": [
##        4,
##        5,
##        6,
##        7,
##        8
##    ],
##    "4": [
##        1,
##        3,
##        8
##    ],
##    "5": [
##        3,
##        6
##    ],
##    "6": [
##        1,
##        3,
##        5,
##        7
##    ],
##    "7": [
##        1,
##        3,
##        6
##    ],
##    "8": [
##        3,
##        4
##    ],
##    "9": [
##        2
##    ]
##}
##    print(check_relation(adict,"Харьков:Южный", "Киев:Центральный"))
##
##    print()
##    print()

    gr=WeightedGraph(["Харьков:Южный","Харьков:Левада","Киев:Центральный","Полтава:Центральный","Одесса:Центральный",
             "Днепропетровск:Центральный","Запорожье:Центральный","Лубны:Лубны","Купянск:Купянск"])
##    gr.add_edge_by_vertices("Харьков:Южный","Харьков:Левада",0)
##    gr.add_edge_by_vertices("Харьков:Южный","Полтава:Центральный",0)
##    gr.add_edge_by_vertices("Харьков:Левада","Харьков:Южный",0)
    for st in ["Харьков:Южный","Харьков:Левада","Киев:Центральный","Полтава:Центральный","Одесса:Центральный",
             "Днепропетровск:Центральный","Запорожье:Центральный","Лубны:Лубны","Купянск:Купянск"]:
        for v in adict[st]:
            gr.add_edge_by_vertices(st,v,4)
    print(gr)
    print()
    input()
    distances, path_dict=dijkstra(gr,"Харьков:Южный")
    name_distance=distance_array_to_vertex_dict(gr,distances)
    print("Distances form 'Харьков:Южный'")
    for key, value in name_distance.items():
        print(f'{key}:{value}')
    print()

    print('Кратчайшее расстояние от Харькова до Одессы:')
    path=path_dict_to_path(gr.index_of('Харьков:Южный'),
                           gr.index_of("Одесса:Центральный"), path_dict)
    print_weighted_path(gr,path)
    

if __name__ == "__main__":
    main()


