



import heapq

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
    
    def shortest_path(self, start):
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous_nodes = {node: None for node in self.graph}
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances, previous_nodes

def reconstruct_path(previous_nodes, start, target):
    """
    Reconstruct shortest path from start to target using previous_nodes dictionary
    
    Args:
        previous_nodes: Dictionary from Dijkstra's algorithm
        start: Starting node
        target: Target node
    
    Returns:
        List representing the shortest path from start to target
    """
    path = []
    current_node = target
    
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    
    # Reverse to get path from start to target
    path = path[::-1]
    
    # Check if path exists (start and target are connected)
    if path[0] == start:
        return path
    return []

# Example graph (weighted, directed)
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 5), ('D', 10)],
    'C': [('D', 3)],
    'D': [('E', 4)],
    'E': []
}

# Usage:
dijkstra = Dijkstra(graph)
start_node = 'A'
distances, previous_nodes = dijkstra.shortest_path('A')

print(f"Shortest distances from {start_node}:")
for node, distance in distances.items():
    print(f"{node}: {distance}")

target_node = 'E'
path = reconstruct_path(previous_nodes, start_node, target_node)
print(f"\nShortest path from {start_node} to {target_node}: {path}")