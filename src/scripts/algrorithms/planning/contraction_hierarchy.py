
"""
Contraction Hierarchy (CH) is a speed-up technique for route planning in road networks.

Key Components of the Implementation:

Graph Representation:
Node class represents each vertex with edges and contraction information
Graph class manages the entire network

Contraction Hierarchy:
ContractionHierarchy class handles the preprocessing
Node ordering based on importance heuristic
Shortcut addition during contraction

Query Algorithm:
Bidirectional Dijkstra that only considers upward edges in forward search
And downward edges in backward search

Optimizations:
Importance heuristic for node ordering
Bidirectional search for queries
Separate upward and downward graphs

Performance Characteristics:

Preprocessing:
The contraction hierarchy needs to be built once for a graph
This can take significant time (O(n²) in worst case)
But only needs to be done once for static graphs

Query Performance:
Queries are typically much faster than regular Dijkstra
Speedup depends on the graph structure and quality of node ordering
In road networks, speedups of 100-1000x are common

This implementation provides a complete foundation that can be further optimized with:
Better node ordering heuristics
Parallel contraction
Custom priority queues
Arc flags or other additional speedup techniques


"""

import heapq
from collections import defaultdict
import math
import random

class Edge:
    def __init__(self, target, weight):
        self.target = target
        self.weight = weight

class Node:
    def __init__(self, node_id, lat, lon):
        self.id = node_id
        self.lat = lat
        self.lon = lon
        self.edges = []
        self.contraction_order = -1  # -1 means not contracted yet
        self.level = 0  # Used for ordering
        self.shortcuts_added = 0

    def add_edge(self, target, weight):
        self.edges.append(Edge(target, weight))

class Graph:
    def __init__(self):
        self.nodes = {}
        self.num_nodes = 0
        self.num_edges = 0
    
    def add_node(self, node_id, lat, lon):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, lat, lon)
            self.num_nodes += 1
    
    def add_edge(self, source, target, weight):
        if source in self.nodes and target in self.nodes:
            self.nodes[source].add_edge(target, weight)
            self.num_edges += 1
    
    def dijkstra(self, start, end, max_level=math.inf):
        """Dijkstra's algorithm with level constraint"""
        distances = {node_id: math.inf for node_id in self.nodes}
        distances[start] = 0
        heap = [(0, start)]
        visited = set()
        
        while heap:
            current_dist, current_node = heapq.heappop(heap)
            
            if current_node == end:
                return current_dist
            
            if current_node in visited:
                continue
            visited.add(current_node)
            
            for edge in self.nodes[current_node].edges:
                neighbor = edge.target
                if self.nodes[neighbor].level > max_level:
                    continue
                
                distance = current_dist + edge.weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))
        
        return math.inf  # No path found
    
    def bidirectional_dijkstra(self, start, end, max_level=math.inf):
        """Bidirectional Dijkstra with level constraint"""
        # Forward search
        forward_dist = {node_id: math.inf for node_id in self.nodes}
        forward_dist[start] = 0
        forward_heap = [(0, start)]
        forward_visited = set()
        
        # Backward search
        backward_dist = {node_id: math.inf for node_id in self.nodes}
        backward_dist[end] = 0
        backward_heap = [(0, end)]
        backward_visited = set()
        
        shortest_distance = math.inf
        meeting_node = None
        
        while forward_heap and backward_heap:
            # Forward step
            if forward_heap:
                current_dist, current_node = heapq.heappop(forward_heap)
                
                if current_node in forward_visited:
                    continue
                forward_visited.add(current_node)
                
                # Check if we've found a shorter path
                if backward_dist[current_node] + current_dist < shortest_distance:
                    shortest_distance = backward_dist[current_node] + current_dist
                    meeting_node = current_node
                
                # Stop if we've processed this node in both searches
                if current_node in backward_visited:
                    break
                
                for edge in self.nodes[current_node].edges:
                    neighbor = edge.target
                    if self.nodes[neighbor].level > max_level:
                        continue
                    
                    distance = current_dist + edge.weight
                    if distance < forward_dist[neighbor]:
                        forward_dist[neighbor] = distance
                        heapq.heappush(forward_heap, (distance, neighbor))
            
            # Backward step
            if backward_heap:
                current_dist, current_node = heapq.heappop(backward_heap)
                
                if current_node in backward_visited:
                    continue
                backward_visited.add(current_node)
                
                # Check if we've found a shorter path
                if forward_dist[current_node] + current_dist < shortest_distance:
                    shortest_distance = forward_dist[current_node] + current_dist
                    meeting_node = current_node
                
                # Stop if we've processed this node in both searches
                if current_node in forward_visited:
                    break
                
                # Need to look at incoming edges for backward search
                for source_node_id, node in self.nodes.items():
                    for edge in node.edges:
                        if edge.target == current_node and self.nodes[source_node_id].level <= max_level:
                            distance = current_dist + edge.weight
                            if distance < backward_dist[source_node_id]:
                                backward_dist[source_node_id] = distance
                                heapq.heappush(backward_heap, (distance, source_node_id))
        
        return shortest_distance if shortest_distance != math.inf else None

class ContractionHierarchy:
    def __init__(self, graph):
        self.graph = graph
        self.upward_graph = Graph()  # Contains only edges to higher-level nodes
        self.downward_graph = Graph()  # Contains only edges to lower-level nodes
        self.contraction_order = []
    
    def compute_importance(self, node_id):
        """Compute importance heuristic for node ordering"""
        node = self.graph.nodes[node_id]
        
        # Number of neighbors
        edge_diff = len(node.edges)
        
        # Number of contracted neighbors
        contracted_neighbors = sum(1 for edge in node.edges 
                                 if self.graph.nodes[edge.target].contraction_order != -1)
        
        # Shortcuts that would be added if we contract this node
        shortcut_count = self.estimate_shortcuts(node_id)
        
        # Importance heuristic (lower is better)
        importance = (edge_diff - contracted_neighbors) + shortcut_count + node.shortcuts_added
        
        return importance
    
    def estimate_shortcuts(self, node_id):
        """Estimate how many shortcuts would be needed if we contract this node"""
        node = self.graph.nodes[node_id]
        neighbors = [edge.target for edge in node.edges 
                    if self.graph.nodes[edge.target].contraction_order == -1]
        
        if len(neighbors) < 2:
            return 0
        
        # For estimation, we don't do full Dijkstra
        return len(neighbors) * (len(neighbors) - 1)
    
    def contract_node(self, node_id):
        """Contract a node by adding shortcuts between its neighbors"""
        node = self.graph.nodes[node_id]
        neighbors = [edge.target for edge in node.edges 
                    if self.graph.nodes[edge.target].contraction_order == -1]
        
        shortcuts_added = 0
        
        # Check all pairs of neighbors
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                u = neighbors[i]
                v = neighbors[j]
                
                # Find edge weights if they exist
                uv_weight = None
                vu_weight = None
                
                for edge in self.graph.nodes[u].edges:
                    if edge.target == v:
                        uv_weight = edge.weight
                        break
                
                for edge in self.graph.nodes[v].edges:
                    if edge.target == u:
                        vu_weight = edge.weight
                        break
                
                # Check if path through node_id is better
                path_through = None
                path_through_rev = None
                
                # Find edge weights from u to node and node to v
                u_node_weight = None
                node_v_weight = None
                v_node_weight = None
                node_u_weight = None
                
                for edge in self.graph.nodes[u].edges:
                    if edge.target == node_id:
                        u_node_weight = edge.weight
                        break
                
                for edge in node.edges:
                    if edge.target == v:
                        node_v_weight = edge.weight
                        break
                
                for edge in self.graph.nodes[v].edges:
                    if edge.target == node_id:
                        v_node_weight = edge.weight
                        break
                
                for edge in node.edges:
                    if edge.target == u:
                        node_u_weight = edge.weight
                        break
                
                if u_node_weight is not None and node_v_weight is not None:
                    path_through = u_node_weight + node_v_weight
                
                if v_node_weight is not None and node_u_weight is not None:
                    path_through_rev = v_node_weight + node_u_weight
                
                # Add shortcuts if needed
                if path_through is not None and (uv_weight is None or path_through < uv_weight):
                    self.graph.add_edge(u, v, path_through)
                    shortcuts_added += 1
                
                if path_through_rev is not None and (vu_weight is None or path_through_rev < vu_weight):
                    self.graph.add_edge(v, u, path_through_rev)
                    shortcuts_added += 1
        
        node.shortcuts_added = shortcuts_added
        return shortcuts_added
    
    def build(self):
        """Build the contraction hierarchy"""
        # Create a copy of the original graph
        self.upward_graph = Graph()
        self.downward_graph = Graph()
        
        # Add all nodes to both graphs
        for node_id, node in self.graph.nodes.items():
            self.upward_graph.add_node(node_id, node.lat, node.lon)
            self.downward_graph.add_node(node_id, node.lat, node.lon)
        
        order = 0
        remaining_nodes = set(self.graph.nodes.keys())
        
        while remaining_nodes:
            # Find the node with lowest importance
            min_importance = math.inf
            next_node = None
            
            for node_id in remaining_nodes:
                importance = self.compute_importance(node_id)
                if importance < min_importance:
                    min_importance = importance
                    next_node = node_id
            
            if next_node is None:
                break
            
            # Contract the node
            self.contract_node(next_node)
            self.graph.nodes[next_node].contraction_order = order
            self.graph.nodes[next_node].level = order
            self.contraction_order.append(next_node)
            remaining_nodes.remove(next_node)
            order += 1
        
        # Build upward and downward graphs
        for node_id, node in self.graph.nodes.items():
            for edge in node.edges:
                target_node = self.graph.nodes[edge.target]
                if node.contraction_order < target_node.contraction_order:
                    # Upward edge
                    self.upward_graph.add_edge(node_id, edge.target, edge.weight)
                else:
                    # Downward edge
                    self.downward_graph.add_edge(edge.target, node_id, edge.weight)
    
    def query(self, start, end):
        """Query the shortest path using bidirectional Dijkstra on the hierarchy"""
        # Forward search in upward graph
        forward_dist = {node_id: math.inf for node_id in self.graph.nodes}
        forward_dist[start] = 0
        forward_heap = [(0, start)]
        forward_visited = set()
        
        # Backward search in downward graph
        backward_dist = {node_id: math.inf for node_id in self.graph.nodes}
        backward_dist[end] = 0
        backward_heap = [(0, end)]
        backward_visited = set()
        
        shortest_distance = math.inf
        
        while forward_heap and backward_heap:
            # Forward step
            if forward_heap:
                current_dist, current_node = heapq.heappop(forward_heap)
                
                if current_dist > shortest_distance:
                    break
                
                if current_node in forward_visited:
                    continue
                forward_visited.add(current_node)
                
                # Update shortest distance if we've found a better path
                if backward_dist[current_node] + current_dist < shortest_distance:
                    shortest_distance = backward_dist[current_node] + current_dist
                
                # Explore upward edges
                for edge in self.upward_graph.nodes[current_node].edges:
                    neighbor = edge.target
                    distance = current_dist + edge.weight
                    if distance < forward_dist[neighbor]:
                        forward_dist[neighbor] = distance
                        heapq.heappush(forward_heap, (distance, neighbor))
            
            # Backward step
            if backward_heap:
                current_dist, current_node = heapq.heappop(backward_heap)
                
                if current_dist > shortest_distance:
                    break
                
                if current_node in backward_visited:
                    continue
                backward_visited.add(current_node)
                
                # Update shortest distance if we've found a better path
                if forward_dist[current_node] + current_dist < shortest_distance:
                    shortest_distance = forward_dist[current_node] + current_dist
                
                # Explore downward edges (which are stored in reverse)
                for edge in self.downward_graph.nodes[current_node].edges:
                    neighbor = edge.target
                    distance = current_dist + edge.weight
                    if distance < backward_dist[neighbor]:
                        backward_dist[neighbor] = distance
                        heapq.heappush(backward_heap, (distance, neighbor))
        
        return shortest_distance if shortest_distance != math.inf else None

# Example usage
def create_sample_graph():
    """Create a sample graph for testing"""
    graph = Graph()
    
    # Add nodes (ID, latitude, longitude)
    graph.add_node(1, 0, 0)
    graph.add_node(2, 1, 0)
    graph.add_node(3, 0, 1)
    graph.add_node(4, 1, 1)
    graph.add_node(5, 0.5, 0.5)
    
    # Add edges (source, target, weight)
    graph.add_edge(1, 2, 1)
    graph.add_edge(2, 1, 1)
    graph.add_edge(1, 3, 1)
    graph.add_edge(3, 1, 1)
    graph.add_edge(2, 4, 1)
    graph.add_edge(4, 2, 1)
    graph.add_edge(3, 4, 1)
    graph.add_edge(4, 3, 1)
    graph.add_edge(1, 5, 0.5)
    graph.add_edge(5, 1, 0.5)
    graph.add_edge(2, 5, 0.5)
    graph.add_edge(5, 2, 0.5)
    graph.add_edge(3, 5, 0.5)
    graph.add_edge(5, 3, 0.5)
    graph.add_edge(4, 5, 0.5)
    graph.add_edge(5, 4, 0.5)
    
    return graph

def benchmark():
    """Benchmark the contraction hierarchy vs regular Dijkstra"""
    # Create a larger random graph
    graph = Graph()
    num_nodes = 100
    grid_size = 10
    
    # Create grid nodes
    for i in range(grid_size):
        for j in range(grid_size):
            node_id = i * grid_size + j + 1
            graph.add_node(node_id, i, j)
    
    # Add random edges
    for i in range(grid_size):
        for j in range(grid_size):
            node_id = i * grid_size + j + 1
            # Connect to right neighbor
            if j < grid_size - 1:
                target = i * grid_size + (j + 1) + 1
                weight = random.uniform(0.5, 1.5)
                graph.add_edge(node_id, target, weight)
                graph.add_edge(target, node_id, weight)
            # Connect to bottom neighbor
            if i < grid_size - 1:
                target = (i + 1) * grid_size + j + 1
                weight = random.uniform(0.5, 1.5)
                graph.add_edge(node_id, target, weight)
                graph.add_edge(target, node_id, weight)
            # Add some random diagonals
            if random.random() < 0.3:
                if i < grid_size - 1 and j < grid_size - 1:
                    target = (i + 1) * grid_size + (j + 1) + 1
                    weight = random.uniform(1.0, 2.0)
                    graph.add_edge(node_id, target, weight)
                    graph.add_edge(target, node_id, weight)
    
    print(f"Graph with {graph.num_nodes} nodes and {graph.num_edges} edges")
    
    # Build contraction hierarchy
    import time
    print("Building contraction hierarchy...")
    start_time = time.time()
    ch = ContractionHierarchy(graph)
    ch.build()
    build_time = time.time() - start_time
    print(f"Built in {build_time:.2f} seconds")
    
    # Test queries
    test_cases = [
        (1, grid_size * grid_size),  # Top-left to bottom-right
        (1, grid_size),  # Top-left to top-right
        (grid_size, grid_size * grid_size),  # Top-right to bottom-right
        (1, (grid_size - 1) * grid_size + 1),  # Top-left to bottom-left
        (grid_size // 2 * grid_size + grid_size // 2, grid_size * grid_size)  # Center to bottom-right
    ]
    
    for start, end in test_cases:
        print(f"\nQuery from {start} to {end}")
        
        # Regular bidirectional Dijkstra
        start_time = time.time()
        dist = graph.bidirectional_dijkstra(start, end)
        dijkstra_time = time.time() - start_time
        print(f"Dijkstra: {dist:.2f} (took {dijkstra_time:.4f} sec)")
        
        # CH query
        start_time = time.time()
        ch_dist = ch.query(start, end)
        ch_time = time.time() - start_time
        print(f"CH: {ch_dist:.2f} (took {ch_time:.4f} sec)")
        
        # Verify results match
        if abs(dist - ch_dist) > 1e-6:
            print("WARNING: Results don't match!")
            print(f"Dijkstra: {dist}, CH: {ch_dist}")

if __name__ == "__main__":
    # Simple example
    print("Simple example:")
    graph = create_sample_graph()
    ch = ContractionHierarchy(graph)
    ch.build()
    
    print("Shortest path from 1 to 4:")
    print(f"CH result: {ch.query(1, 4)}")
    print(f"Dijkstra result: {graph.bidirectional_dijkstra(1, 4)}")
    
    # Benchmark on larger graph
    print("\nBenchmark on larger graph:")
    benchmark()