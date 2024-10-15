from __future__ import annotations
from dataclasses import dataclass
from .mst import WeightedPath, print_weighted_path,dict_weighted_path, total_weight, get_trains, get_optimum_trains
from .graph import WeightedEdge, WeightedGraph
from .priority_queue import PriorityQueue

@dataclass
class DijkstraNode:
    vertex:int
    distance:float

    def __lt__(self,other):
        return self.distance<other.distance

    def __eq__(self,other):
        return self.distance==other.distance

def dijkstra(wg,root):
    first=wg.index_of(root)
    distances=[None]*wg.vertex_count
    distances[first]=0
    path_dict={}
    pq=PriorityQueue()
    pq.push(DijkstraNode(first,0))

    while not pq.empty:
        u=pq.pop().vertex
        dist_u=distances[u]
        for we in wg.edges_for_index(u):
            dist_v=distances[we.v]
            if dist_v is None or dist_v>we.weight+dist_u:
                distances[we.v]=we.weight+dist_u
                path_dict[we.v]=we
                pq.push(DijkstraNode(we.v,we.weight+dist_u))
    return distances, path_dict


def distance_array_to_vertex_dict(wg,distances):
    distance_dict={}
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)]=distances[i]
    return distance_dict

def path_dict_to_path(start,end,path_dict):
    if len(path_dict)==0:
        return []
    edge_path=[]
    e=path_dict[end]
    edge_path.append(e)
    while e.u!=start:
        e=path_dict[e.u]
        edge_path.append(e)
    return list(reversed(edge_path))

    
                
    
    
