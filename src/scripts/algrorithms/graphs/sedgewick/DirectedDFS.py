



class DirectedDFS:
    def __init__(self, G, sources=None):
        if isinstance(sources, int):
            # Single source constructor
            self.marked = [False] * G.V()
            self.dfs(G, sources)
        else:
            # Multiple sources constructor
            self.marked = [False] * G.V()
            if sources is not None:
                for s in sources:
                    if not self.marked[s]:
                        self.dfs(G, s)
    
    def dfs(self, G, v):
        self.marked[v] = True
        for w in G.adj(v):
            if not self.marked[w]:
                self.dfs(G, w)
    
    def marked(self, v):
        return self.marked[v]