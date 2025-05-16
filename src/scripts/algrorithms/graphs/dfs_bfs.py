

def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node)  # Process the node
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while len(stack) != 0:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node)  # Process the node
            
            # Push neighbors in reverse order to visit them in order
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while len(queue) != 0:
        node = queue.popleft()
        print(node)  # Process the node
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

"""graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}"""

graph = {
    0: [1, 2],
    1: [3, 4],
    2: [5, 6],
    3: [7, 8],
    4: [9, 10],
    5: [2],
    6: [2],
    7: [3],
    8: [3],
    9: [4],
    10: [4]
}

print("DFS Recursive:")
dfs_recursive(graph, 0)

print("\nDFS Iterative:")
dfs_iterative(graph, 0)

print("\nBFS:")
bfs(graph, 0)