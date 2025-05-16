


"""
This graph supports vertices connected by edges with weights, where edges are bidirectional.

Core Features:
Add/remove vertices
Add/remove edges with weights
Retrieve neighbors and edge weights
Check adjacency
Get degree of vertices
Represent the graph as adjacency list
String representation
"""

class WeightedUndirectedGraph:
    def __init__(self):
        self._adjacency = {}  # {vertex: {neighbor: weight, ...}}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self._adjacency:
            self._adjacency[vertex] = {}

    def remove_vertex(self, vertex):
        """Remove a vertex and all associated edges."""
        if vertex in self._adjacency:
            # Remove edges from neighbors to this vertex
            for neighbor in list(self._adjacency[vertex]):
                del self._adjacency[neighbor][vertex]
            # Remove the vertex itself
            del self._adjacency[vertex]

    def add_edge(self, v1, v2, weight):
        """Add an undirected edge with weight."""
        if v1 not in self._adjacency:
            self.add_vertex(v1)
        if v2 not in self._adjacency:
            self.add_vertex(v2)
        self._adjacency[v1][v2] = weight
        self._adjacency[v2][v1] = weight

    def remove_edge(self, v1, v2):
        """Remove the edge between v1 and v2."""
        if v1 in self._adjacency and v2 in self._adjacency[v1]:
            del self._adjacency[v1][v2]
        if v2 in self._adjacency and v1 in self._adjacency[v2]:
            del self._adjacency[v2][v1]

    def get_weight(self, v1, v2):
        """Get weight of the edge between v1 and v2."""
        return self._adjacency.get(v1, {}).get(v2)

    def neighbors(self, vertex):
        """Return neighbors with weights."""
        return self._adjacency.get(vertex, {}).copy()

    def degree(self, vertex):
        """Return degree of a vertex."""
        return len(self._adjacency.get(vertex, {}))

    def vertices(self):
        """Return all vertices."""
        return list(self._adjacency.keys())

    def has_edge(self, v1, v2):
        """Check if an edge exists."""
        return v2 in self._adjacency.get(v1, {})

    def __repr__(self):
        return f"WeightedUndirectedGraph({self._adjacency})"


# Create a new weighted undirected graph
graph = WeightedUndirectedGraph()

# Add vertices
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Add edges with weights
graph.add_edge('A', 'B', 4.5)
graph.add_edge('A', 'C', 2.0)
graph.add_edge('B', 'C', 3.2)

print("Vertices:", graph.vertices())
# Output: ['A', 'B', 'C']

print("Neighbors of A:", graph.neighbors('A'))
# Output: {'B': 4.5, 'C': 2.0}

print("Weight of edge A - C:", graph.get_weight('A', 'C'))
# Output: 2.0

print("Degree of A:", graph.degree('A'))
# Output: 2

print("Does edge B - C exist?", graph.has_edge('B', 'C'))  # True

# Remove an edge
graph.remove_edge('A', 'C')
print("Neighbors of A after removal:", graph.neighbors('A'))
# Output: {'B': 4.5}

# Remove a vertex
graph.remove_vertex('B')
print("Vertices after removing B:", graph.vertices())
# Output: ['A', 'C']
print("Neighbors of A after B removal:", graph.neighbors('A'))
# Output: {}
