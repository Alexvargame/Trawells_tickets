from heapq import heappush, heappop


class PriorityQueue():
    def __init__(self):
        self.container=[]
        
    @property
    def empty(self):
        return not self.container
    def push(self, item):
        heappush(self.container, item)
    def pop(self):
        return heappop(self.container)
    def __repr__(self):
        return repr(self.container)

    
