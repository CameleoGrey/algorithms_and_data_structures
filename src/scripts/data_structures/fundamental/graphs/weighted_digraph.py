

"""
A Weighted Directed Graph consists of vertices connected by directed edges, each with an associated weight.

Core Features:
Add/remove vertices
Add/remove edges with weights
Retrieve neighbors and edge weights
Check existence of vertices and edges
Calculate in-degree and out-degree
Represent the graph as adjacency list with weights
Support iteration and string representation
"""

class WeightedDirectedGraph:
    def __init__(self):
        self._adjacency = {}  # {vertex: {neighbor: weight, ...}, ...}
        self._in_degree = {}  # {vertex: in-degree count}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self._adjacency:
            self._adjacency[vertex] = {}
            self._in_degree[vertex] = 0

    def remove_vertex(self, vertex):
        """Remove a vertex and all associated edges."""
        if vertex in self._adjacency:
            # Remove edges from vertex to others
            for neighbor in self._adjacency[vertex]:
                self._in_degree[neighbor] -= 1
            # Remove edges to vertex
            for v, neighbors in self._adjacency.items():
                if vertex in neighbors:
                    del neighbors[vertex]
                    self._in_degree[vertex] -= 1
            # Remove vertex
            del self._adjacency[vertex]
            del self._in_degree[vertex]

    def add_edge(self, from_vertex, to_vertex, weight):
        """Add a directed edge with weight."""
        if from_vertex not in self._adjacency:
            self.add_vertex(from_vertex)
        if to_vertex not in self._adjacency:
            self.add_vertex(to_vertex)
        if to_vertex not in self._adjacency[from_vertex]:
            self._adjacency[from_vertex][to_vertex] = weight
            self._in_degree[to_vertex] += 1
        else:
            # Update weight if edge exists
            self._adjacency[from_vertex][to_vertex] = weight

    def remove_edge(self, from_vertex, to_vertex):
        """Remove an edge."""
        if from_vertex in self._adjacency and to_vertex in self._adjacency[from_vertex]:
            del self._adjacency[from_vertex][to_vertex]
            self._in_degree[to_vertex] -= 1

    def get_weight(self, from_vertex, to_vertex):
        """Get weight of an edge."""
        return self._adjacency.get(from_vertex, {}).get(to_vertex)

    def neighbors(self, vertex):
        """Return neighbors with weights."""
        return self._adjacency.get(vertex, {}).copy()

    def in_degree(self, vertex):
        """Return in-degree of a vertex."""
        return self._in_degree.get(vertex, 0)

    def out_degree(self, vertex):
        """Return out-degree of a vertex."""
        return len(self._adjacency.get(vertex, {}))

    def vertices(self):
        """Return all vertices."""
        return list(self._adjacency.keys())

    def has_edge(self, from_vertex, to_vertex):
        """Check if an edge exists."""
        return to_vertex in self._adjacency.get(from_vertex, {})

    def __repr__(self):
        return f"WeightedDirectedGraph({self._adjacency})"

# Create a new weighted directed graph
graph = WeightedDirectedGraph()

# Add vertices
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Add edges with weights
graph.add_edge('A', 'B', 5)
graph.add_edge('A', 'C', 10)
graph.add_edge('B', 'C', 3)

print("Vertices:", graph.vertices())
# Output: ['A', 'B', 'C']

print("Neighbors of A:", graph.neighbors('A'))
# Output: {'B': 5, 'C': 10}

print("Weight of edge A -> C:", graph.get_weight('A', 'C'))
# Output: 10

print("In-degree of C:", graph.in_degree('C'))
# Output: 2

print("Out-degree of A:", graph.out_degree('A'))
# Output: 2

# Check if edge exists
print("Edge A -> B exists?", graph.has_edge('A', 'B'))  # True
print("Edge B -> A exists?", graph.has_edge('B', 'A'))  # False

# Update weight
graph.add_edge('A', 'B', 7)
print("Updated weight of edge A -> B:", graph.get_weight('A', 'B'))  # 7

# Remove an edge
graph.remove_edge('A', 'C')
print("Neighbors of A after removal:", graph.neighbors('A'))
# Output: {'B': 7}

# Remove a vertex
graph.remove_vertex('B')
print("Vertices after removing B:", graph.vertices())
# Output: ['A', 'C']
print("Neighbors of A after B removal:", graph.neighbors('A'))
# Output: {}
