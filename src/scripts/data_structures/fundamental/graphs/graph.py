


"""
An Undirected Graph consists of vertices connected by edges that have no direction; edges are bidirectional.

Core Features:
Add/remove vertices
Add/remove edges
Check adjacency
Get neighbors
Get degree of vertices
Represent the graph as adjacency list
Support iteration and string representation
"""

class UndirectedGraph:
    def __init__(self):
        self._adjacency = {}  # {vertex: set of neighbors}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self._adjacency:
            self._adjacency[vertex] = set()

    def remove_vertex(self, vertex):
        """Remove a vertex and all associated edges."""
        if vertex in self._adjacency:
            # Remove edges from vertex to neighbors
            for neighbor in self._adjacency[vertex]:
                self._adjacency[neighbor].remove(vertex)
            # Remove vertex
            del self._adjacency[vertex]

    def add_edge(self, v1, v2):
        """Add an undirected edge between v1 and v2."""
        if v1 not in self._adjacency:
            self.add_vertex(v1)
        if v2 not in self._adjacency:
            self.add_vertex(v2)
        self._adjacency[v1].add(v2)
        self._adjacency[v2].add(v1)

    def remove_edge(self, v1, v2):
        """Remove the edge between v1 and v2."""
        if v1 in self._adjacency and v2 in self._adjacency[v1]:
            self._adjacency[v1].remove(v2)
        if v2 in self._adjacency and v1 in self._adjacency[v2]:
            self._adjacency[v2].remove(v1)

    def neighbors(self, vertex):
        """Return neighbors of a vertex."""
        return self._adjacency.get(vertex, set())

    def degree(self, vertex):
        """Return degree of a vertex."""
        return len(self._adjacency.get(vertex, []))

    def vertices(self):
        """Return all vertices."""
        return list(self._adjacency.keys())

    def has_edge(self, v1, v2):
        """Check if an edge exists between v1 and v2."""
        return v2 in self._adjacency.get(v1, set())

    def __repr__(self):
        return f"UndirectedGraph({self._adjacency})"

# Create a new undirected graph
graph = UndirectedGraph()

# Add vertices
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Add edges
graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('B', 'C')

print("Vertices:", graph.vertices())
# Output: ['A', 'B', 'C']

print("Neighbors of A:", graph.neighbors('A'))
# Output: {'B', 'C'}

print("Degree of A:", graph.degree('A'))
# Output: 2

print("Does edge A - B exist?", graph.has_edge('A', 'B'))  # True
print("Does edge B - A exist?", graph.has_edge('B', 'A'))  # True

# Remove an edge
graph.remove_edge('A', 'C')
print("Neighbors of A after removal:", graph.neighbors('A'))
# Output: {'B'}

# Remove a vertex
graph.remove_vertex('B')
print("Vertices after removing B:", graph.vertices())
# Output: ['A', 'C']
print("Neighbors of A after B removal:", graph.neighbors('A'))
# Output: set()
