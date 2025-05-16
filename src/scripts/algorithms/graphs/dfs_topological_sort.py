



from collections import defaultdict

def topological_sort(graph):
    """
    Perform topological sort using DFS with cycle detection.
    Returns:
        - List of nodes in topological order if no cycle exists
        - None if a cycle is detected (graph is not a DAG)
    """
    visited = set()
    temp_visited = set()  # For cycle detection
    result = []
    is_dag = True  # Flag to track if graph is a DAG
    
    def dfs(node):
        nonlocal is_dag
        if node in temp_visited:
            # Cycle detected
            is_dag = False
            return
        
        if node in visited:
            return
        
        temp_visited.add(node)
        
        for neighbor in graph[node]:
            dfs(neighbor)
            if not is_dag:
                return  # Early exit if cycle found
        
        temp_visited.remove(node)
        visited.add(node)
        result.append(node)
    
    # Convert graph to defaultdict if needed
    if not isinstance(graph, defaultdict):
        default_graph = defaultdict(list)
        for node in graph:
            default_graph[node] = list(graph[node])
        graph = default_graph
    
    # Process all nodes
    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)
            if not is_dag:
                return None  # Cycle exists
    
    return result[::-1]  # Reverse to get topological order

from collections import deque

def topological_sort_kahn(graph):
    """
    Perform topological sort using Kahn's algorithm (indegree-based).
    Returns a list of vertices in topological order or None if cycle exists.
    """
    # Calculate in-degree for each node
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Initialize queue with nodes having 0 in-degree
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycles
    if len(topo_order) != len(graph):
        return None  # Cycle exists
    
    return topo_order

print()
print("Topological sort is suitable for DAGs only.")
print()

# Example DAG (Directed Acyclic Graph)
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': ['E'],
    'E': []
}

# Using DFS approach
print("Topological Sort (DFS):", topological_sort(graph))

# Using Kahn's algorithm
print("Topological Sort (Kahn):", topological_sort_kahn(graph))