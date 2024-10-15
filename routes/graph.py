from __future__ import annotations
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


##class Graph_My:
##    
##    def __init__(self, data):
##        
##        self.edges={}
##        for st in data:
##            key,value=st, st.neighbours.all()
##            l=self.edges.get(key,[])
##            l.append(value)
##            self.edges[key]=value
##    
##    def printGraph(self):
##        for key in self.edges.keys():
##            for value in self.edges[key]:
##                print(f'{key}->{value}',end='')
####    def __str__(self):
####        return self.printGraph()
####
##def get_edges(adict):
##    return [item for sublist in [[(int(key),scr) for scr in value] for key, value in adict.items()] for item in sublist]
                
