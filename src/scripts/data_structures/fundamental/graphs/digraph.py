

"""
A Directed Graph consists of nodes (vertices) connected by edges with a direction.

Core Features:
Add/remove vertices
Add/remove edges
Check adjacency
Get neighbors
Get in-degree and out-degree
Represent the graph as adjacency list
Support for iteration and string representation
"""

class DirectedGraph:
    def __init__(self):
        self._adjacency = {}  # {vertex: set of neighbors}
        self._in_degree = {}  # {vertex: in-degree count}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self._adjacency:
            self._adjacency[vertex] = set()
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
                    neighbors.remove(vertex)
                    self._in_degree[vertex] -= 1
            # Remove vertex
            del self._adjacency[vertex]
            del self._in_degree[vertex]

    def add_edge(self, from_vertex, to_vertex):
        """Add a directed edge from 'from_vertex' to 'to_vertex'."""
        if from_vertex not in self._adjacency:
            self.add_vertex(from_vertex)
        if to_vertex not in self._adjacency:
            self.add_vertex(to_vertex)
        if to_vertex not in self._adjacency[from_vertex]:
            self._adjacency[from_vertex].add(to_vertex)
            self._in_degree[to_vertex] += 1

    def remove_edge(self, from_vertex, to_vertex):
        """Remove a directed edge."""
        if from_vertex in self._adjacency and to_vertex in self._adjacency[from_vertex]:
            self._adjacency[from_vertex].remove(to_vertex)
            self._in_degree[to_vertex] -= 1

    def neighbors(self, vertex):
        """Return neighbors (outgoing edges) of a vertex."""
        return self._adjacency.get(vertex, set())

    def in_degree(self, vertex):
        """Return in-degree of a vertex."""
        return self._in_degree.get(vertex, 0)

    def out_degree(self, vertex):
        """Return out-degree of a vertex."""
        return len(self._adjacency.get(vertex, []))

    def vertices(self):
        """Return all vertices."""
        return list(self._adjacency.keys())

    def has_edge(self, from_vertex, to_vertex):
        """Check if an edge exists."""
        return to_vertex in self._adjacency.get(from_vertex, set())

    def __repr__(self):
        return f"DirectedGraph({self._adjacency})"

# Create a new directed graph
graph = DirectedGraph()

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

print("In-degree of C:", graph.in_degree('C'))
# Output: 2

print("Out-degree of A:", graph.out_degree('A'))
# Output: 2

# Check edge existence
print("Does edge A -> B exist?", graph.has_edge('A', 'B'))  # True
print("Does edge B -> A exist?", graph.has_edge('B', 'A'))  # False

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
