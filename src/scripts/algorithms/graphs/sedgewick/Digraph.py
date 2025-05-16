


class Digraph:
    def __init__(self, V):
        self.V = V  # number of vertices
        self.E = 0   # number of edges
        self.adj = [[] for _ in range(V)]  # adjacency list using Python lists
    
    def V(self):
        return self.V
    
    def E(self):
        return self.E
    
    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.E += 1
    
    def adj(self, v):
        return self.adj[v]
    
    def reverse(self):
        R = Digraph(self.V)
        for v in range(self.V):
            for w in self.adj(v):
                R.add_edge(w, v)
        return R