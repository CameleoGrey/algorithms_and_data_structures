import heapq

def prim_mst(graph):
    """
    Implementation of Prim's algorithm to find Minimum Spanning Tree (MST)
    
    Args:
        graph: Dictionary representing adjacency list {vertex: [(neighbor, weight), ...]}
    
    Returns:
        List of edges in the MST as tuples (u, v, weight)
        Total weight of the MST
    """
    if not graph:
        return [], 0
    
    # Initialize variables
    mst_edges = []
    total_weight = 0
    visited = set()
    min_heap = []
    
    # Start with an arbitrary vertex (first vertex in the graph)
    start_vertex = next(iter(graph))
    visited.add(start_vertex)
    
    # Add all edges from start vertex to the heap
    for neighbor, weight in graph[start_vertex]:
        heapq.heappush(min_heap, (weight, start_vertex, neighbor))
    
    while min_heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(min_heap)
        
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            # Add all edges from v to unvisited vertices
            for neighbor, edge_weight in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(min_heap, (edge_weight, v, neighbor))
    
    # Check if all vertices are connected
    if len(visited) != len(graph):
        return [], 0  # Graph is disconnected
    
    return mst_edges, total_weight

########################################################
# Kruskal's
class UnionFind:
    """Union-Find (Disjoint Set Union) data structure for Kruskal's algorithm"""
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        
        if x_root == y_root:
            return False  # Already in the same set
        
        # Union by rank
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            if self.rank[x_root] == self.rank[y_root]:
                self.rank[x_root] += 1
        return True

def kruskal_mst(graph):
    """
    Implementation of Kruskal's algorithm to find Minimum Spanning Tree (MST)
    
    Args:
        graph: Dictionary representing adjacency list {vertex: [(neighbor, weight), ...]}
               Vertices should be 0-indexed integers for UnionFind to work efficiently
    
    Returns:
        List of edges in the MST as tuples (u, v, weight)
        Total weight of the MST
    """
    if not graph:
        return [], 0
    
    # Prepare all edges and sort them by weight
    edges = []
    for u in graph:
        for v, weight in graph[u]:
            edges.append((weight, u, v))
    edges.sort()  # Sorts by first element of tuple (weight)
    
    uf = UnionFind(len(graph))
    mst_edges = []
    total_weight = 0
    
    for weight, u, v in edges:
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            if len(mst_edges) == len(graph) - 1:
                break  # MST has V-1 edges
    
    # Check if MST includes all vertices (graph is connected)
    if len(mst_edges) != len(graph) - 1:
        return [], 0  # Graph is disconnected
    
    return mst_edges, total_weight

########################################################


print()
print("Note: A minimum spanning tree (MST) or minimum weight spanning tree is a " \
"subset of the edges of a connected, edge-weighted undirected graph that connects " \
"all the vertices together, without any cycles and with the minimum possible total edge weight.")
print()

# Example graph represented as adjacency list
graph = {
    0: [(1, 2), (3, 6)],
    1: [(0, 2), (2, 3), (3, 8), (4, 5)],
    2: [(1, 3), (4, 7)],
    3: [(0, 6), (1, 8), (4, 9)],
    4: [(1, 5), (2, 7), (3, 9)]
}

print("Edges in MST (Prim):")
mst_edges, total_weight = prim_mst(graph)
for edge in mst_edges:
    print(f"{edge[0]} -- {edge[1]} (weight: {edge[2]})")
print(f"Total weight of MST: {total_weight}")
print()

graph = {
    0: [(1, 2), (3, 6)],
    1: [(0, 2), (2, 3), (3, 8), (4, 5)],
    2: [(1, 3), (4, 7)],
    3: [(0, 6), (1, 8), (4, 9)],
    4: [(1, 5), (2, 7), (3, 9)]
}
print("Edges in MST (Kruskal):")
mst_edges, total_weight = kruskal_mst(graph)
for edge in mst_edges:
    print(f"{edge[0]} -- {edge[1]} (weight: {edge[2]})")
print(f"Total weight of MST: {total_weight}")