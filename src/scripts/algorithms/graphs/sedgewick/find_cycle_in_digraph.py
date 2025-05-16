



class DirectedCycle:
    def __init__(self, digraph):
        self.marked = [False] * digraph.V()
        self.edge_to = [0] * digraph.V()
        self.cycle = None  # vertices on a cycle (if one exists)
        self.on_stack = [False] * digraph.V()  # vertices on recursive call stack
        
        for v in range(digraph.V()):
            if not self.marked[v]:
                self.dfs(digraph, v)
    
    def dfs(self, digraph, v):
        self.on_stack[v] = True
        self.marked[v] = True
        
        for w in digraph.adj(v):
            if self.has_cycle():
                return
            elif not self.marked[w]:
                self.edge_to[w] = v
                self.dfs(digraph, w)
            elif self.on_stack[w]:
                self.cycle = []
                x = v
                while x != w:
                    self.cycle.append(x)
                    x = self.edge_to[x]
                self.cycle.append(w)
                self.cycle.append(v)
                self.cycle.reverse()  # To maintain same order as Java Stack
        
        self.on_stack[v] = False
    
    def has_cycle(self):
        return self.cycle is not None
    
    def get_cycle(self):
        return self.cycle