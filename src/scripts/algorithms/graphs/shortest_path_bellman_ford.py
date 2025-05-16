



from collections import deque

def bellman_ford_queue(graph, start):
    """
    Queue-based Bellman-Ford algorithm (SPFA) for shortest paths with negative weights
    
    Args:
        graph: Dictionary representing adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
    
    Returns:
        Dictionary of shortest distances from start to each node
        Dictionary of previous nodes for path reconstruction
        False if negative cycle is detected, True otherwise
    """
    # Initialize distances
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    # Track previous nodes for path reconstruction
    previous_nodes = {node: None for node in graph}
    
    # Queue for nodes to process
    queue = deque([start])
    in_queue = {node: False for node in graph}
    in_queue[start] = True
    
    # Count how many times each node is enqueued
    enqueue_count = {node: 0 for node in graph}
    enqueue_count[start] = 1
    
    while queue:
        current_node = queue.popleft()
        in_queue[current_node] = False
        
        for neighbor, weight in graph.get(current_node, []):
            if distances[current_node] + weight < distances[neighbor]:
                distances[neighbor] = distances[current_node] + weight
                previous_nodes[neighbor] = current_node
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
                    enqueue_count[neighbor] += 1
                    
                    # If a node is enqueued V times, there's a negative cycle
                    if enqueue_count[neighbor] > len(graph):
                        return {}, {}, False
    
    return distances, previous_nodes, True


def reconstruct_path_bf(previous_nodes, start, target):
    """
    Reconstruct shortest path from start to target using previous_nodes from Bellman-Ford
    
    Args:
        previous_nodes: Dictionary from Bellman-Ford algorithm
        start: Starting node
        target: Target node
    
    Returns:
        List representing the shortest path from start to target
        Empty list if no path exists
    """
    path = []
    current_node = target
    
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    
    # Reverse to get path from start to target
    path = path[::-1]
    
    # Check if path exists (start and target are connected)
    if path and path[0] == start:
        return path
    return []


# Example graph with negative weights but no negative cycles
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', -3), ('D', 1)],
    'C': [('D', 3)],
    'D': [('E', -2)],
    'E': []
}

start_node = 'A'
distances, previous_nodes, no_negative_cycle = bellman_ford_queue(graph, start_node)

if no_negative_cycle:
    print(f"Shortest distances from {start_node}:")
    for node, distance in distances.items():
        print(f"{node}: {distance}")
    
    target_node = 'E'
    path = reconstruct_path_bf(previous_nodes, start_node, target_node)
    print(f"\nShortest path from {start_node} to {target_node}: {path}")
else:
    print("Negative cycle detected - no shortest paths exist")