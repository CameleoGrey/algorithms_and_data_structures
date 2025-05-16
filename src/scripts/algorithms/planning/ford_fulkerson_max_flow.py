


"""
Here's a complete implementation of the Ford-Fulkerson algorithm 
using the shortest augmenting path approach (also known as the Edmonds-Karp algorithm) for 
finding maximum flow in a network:

Key Components of the Implementation:
Edge Class:
Represents edges in the flow network with capacity, flow, and reverse edge information
Each edge knows its reverse edge (important for residual network)

FlowNetwork Class:
Manages the entire flow network with adjacency lists

Ford-Fulkerson Method (Generic Framework)
Concept: The Ford-Fulkerson method is a general approach (not a specific algorithm) for finding the maximum flow in a network.

How it works:
Start with an initial flow (usually zero).
While there exists an augmenting path (a path from source to sink with available capacity), push flow along it.
Update residual capacities (forward edges decrease, backward edges increase).
Key Limitation: It doesn't specify how to find augmenting paths, so its runtime depends on the method used (can be very slow if poor path choices are made).

Implements two algorithms:
Edmonds-Karp (Ford-Fulkerson with BFS)
Dinic's algorithm (more efficient variant)

Dinic's Algorithm:
Uses BFS to construct level graphs and DFS to find blocking flows
Time complexity: O(V²E) for general graphs, O(E√V) for unit capacity networks
More efficient than Edmonds-Karp for many practical cases

Edmonds-Karp Algorithm:
A specialization of Ford-Fulkerson that uses BFS to find augmenting paths
Time complexity: O(VE²)
Simpler to implement but generally slower than Dinic's

Edmonds-Karp Algorithm:
Uses BFS to always find the shortest augmenting path
Time complexity O(VE²) where V is vertices, E is edges
More efficient than generic Ford-Fulkerson which can have poor performance on certain graphs

Dinic's Algorithm:
More advanced algorithm included for comparison
Builds level graphs and uses blocking flows
Time complexity O(V²E) - often performs better in practice

Applications:
Network Flow Problems:
Maximum flow in pipes, computer networks
Traffic flow optimization

Bipartite Matching:
Job assignments
Dating/matching applications
Resource allocation

Image Segmentation:
In computer vision for separating foreground/background

Baseball Elimination:
Determining if a team can still win a league

The implementation includes both Edmonds-Karp (which is what you asked for) and Dinic's 
algorithm (which is more efficient) for comparison. The Edmonds-Karp algorithm is a specific 
implementation of the Ford-Fulkerson method that uses BFS to find the shortest augmenting path in 
each iteration, guaranteeing polynomial time complexity.
"""

from collections import deque

class FlowEdge:
    """Represents an edge in the flow network with capacity and flow tracking."""
    def __init__(self, to_node, reverse_index, capacity):
        self.to_node = to_node          # Where this edge leads to
        self.reverse_index = reverse_index  # Index of reverse edge in neighbor's list
        self.capacity = capacity        # Maximum flow this edge can carry

class FlowNetwork:
    """Base class for flow network algorithms."""
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.graph = [[] for _ in range(num_nodes)]  # Adjacency list of edges
    
    def add_edge(self, from_node, to_node, capacity):
        """Adds a directed edge with given capacity to the flow network."""
        # Forward edge (original capacity) and backward edge (0 capacity)
        forward_edge = FlowEdge(to_node, len(self.graph[to_node]), capacity)
        backward_edge = FlowEdge(from_node, len(self.graph[from_node]), 0)
        
        self.graph[from_node].append(forward_edge)
        self.graph[to_node].append(backward_edge)

class EdmondsKarp(FlowNetwork):
    """Implements the Edmonds-Karp algorithm (BFS-based Ford-Fulkerson)."""
    
    def max_flow(self, source, sink):
        """Computes maximum flow from source to sink using BFS for shortest paths."""
        total_flow = 0
        
        while True:
            # BFS to find the shortest augmenting path
            parent = [-1] * self.num_nodes
            parent[source] = -2  # Mark source as visited
            queue = deque()
            queue.append((source, float('inf')))
            
            found_path = False
            current_flow = 0
            
            while queue:
                current_node, flow = queue.popleft()
                
                for edge in self.graph[current_node]:
                    # not visited and not backward edge
                    if parent[edge.to_node] == -1 and edge.capacity > 0:
                        parent[edge.to_node] = current_node
                        new_flow = min(flow, edge.capacity)
                        
                        if edge.to_node == sink:
                            current_flow = new_flow
                            found_path = True
                            break
                            
                        queue.append((edge.to_node, new_flow))
                
                if found_path:
                    break
            
            if not found_path:
                break  # No more augmenting paths
            
            total_flow += current_flow
            
            # Update residual capacities along the path
            node = sink
            while node != source:
                prev_node = parent[node]
                
                # Find the edge from prev_node to node
                for edge in self.graph[prev_node]:
                    if edge.to_node == node and edge.capacity >= current_flow:
                        edge.capacity -= current_flow
                        
                        # Update reverse edge
                        reverse_edge = self.graph[node][edge.reverse_index]
                        reverse_edge.capacity += current_flow
                        break
                
                node = prev_node
        
        return total_flow

class Dinic(FlowNetwork):
    """Implements Dinic's algorithm with level graphs and blocking flows."""
    
    def max_flow(self, source, sink):
        """Computes maximum flow using level graphs and blocking flows."""
        total_flow = 0
        level = [-1] * self.num_nodes
        
        def create_level_graph():
            """BFS to create level graph (layers from source)."""
            nonlocal level
            level = [-1] * self.num_nodes
            level[source] = 0
            queue = deque([source])
            
            while queue:
                current_node = queue.popleft()
                
                for edge in self.graph[current_node]:
                    if level[edge.to_node] == -1 and edge.capacity > 0:
                        level[edge.to_node] = level[current_node] + 1
                        queue.append(edge.to_node)
            
            return level[sink] != -1  # Return whether sink is reachable
        
        def send_flow(current_node, flow):
            """DFS to send flow in the level graph."""
            if current_node == sink:
                return flow
            
            while edge_ptr[current_node] < len(self.graph[current_node]):
                edge = self.graph[current_node][edge_ptr[current_node]]
                
                # Only move to nodes in next level with remaining capacity
                if level[edge.to_node] == level[current_node] + 1 and edge.capacity > 0:
                    min_flow = min(flow, edge.capacity)
                    result = send_flow(edge.to_node, min_flow)
                    
                    if result > 0:
                        # Update edge capacities
                        edge.capacity -= result
                        self.graph[edge.to_node][edge.reverse_index].capacity += result
                        return result
                
                edge_ptr[current_node] += 1
            
            return 0
        
        while create_level_graph():
            edge_ptr = [0] * self.num_nodes  # Tracks next edge to explore
            
            while True:
                flow = send_flow(source, float('inf'))
                if flow == 0:
                    break
                total_flow += flow
        
        return total_flow

# ================== Usage Examples ==================

def run_example(name, nodes, edges, source, sink, expected):
    print(f"\n{name} (Expected: {expected})")
    
    # Dinic's algorithm
    dinic = Dinic(nodes)
    for fr, to, cap in edges:
        dinic.add_edge(fr, to, cap)
    print(f"Dinic's result: {dinic.max_flow(source, sink)}")
    
    # Edmonds-Karp algorithm
    ek = EdmondsKarp(nodes)
    for fr, to, cap in edges:
        ek.add_edge(fr, to, cap)
    print(f"Edmonds-Karp result: {ek.max_flow(source, sink)}")
    pass

if __name__ == "__main__":
    # Example 1: Simple network
    simple_edges = [
        (0, 1, 10), (0, 2, 10),
        (1, 2, 2), (1, 3, 8),
        (2, 3, 10)
    ]
    run_example("Simple Network", 4, simple_edges, 0, 3, 18)
    
    # Example 2: Complex network
    complex_edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 10), (1, 3, 12),
        (2, 1, 4), (2, 4, 14),
        (3, 2, 9), (3, 5, 20),
        (4, 3, 7), (4, 5, 4)
    ]
    run_example("Complex Network", 6, complex_edges, 0, 5, 23)
    
    # Example 3: Bipartite matching
    bipartite_edges = [
        # Source to left nodes
        (6, 0, 1), (6, 1, 1), (6, 2, 1),
        # Left to right nodes
        (0, 3, 1), (0, 4, 1),
        (1, 3, 1),
        (2, 4, 1), (2, 5, 1),
        # Right nodes to sink
        (3, 7, 1), (4, 7, 1), (5, 7, 1)
    ]
    run_example("Bipartite Matching", 8, bipartite_edges, 6, 7, 3)