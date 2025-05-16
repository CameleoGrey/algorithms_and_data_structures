



def kosaraju(graph):
    # Step 1: First DFS to fill the stack
    visited = set()
    stack = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)
    
    for node in graph:
        if node not in visited:
            dfs(node)
    
    # Step 2: Reverse the graph
    reversed_graph = {}
    for node in graph:
        for neighbor in graph[node]:
            reversed_graph.setdefault(neighbor, []).append(node)
    
    # Step 3: Second DFS on reversed graph in stack order
    visited = set()
    components = []
    
    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            dfs_stack = [node]
            visited.add(node)
            
            while dfs_stack:
                current = dfs_stack.pop()
                component.append(current)
                for neighbor in reversed_graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        dfs_stack.append(neighbor)
            
            components.append(component)
    
    return components

def tarjan(graph):
    index = 0
    indices = {}
    low_links = {}
    on_stack = set()
    stack = []
    components = []
    
    def strongconnect(node):
        nonlocal index
        indices[node] = index
        low_links[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in indices:
                strongconnect(neighbor)
                low_links[node] = min(low_links[node], low_links[neighbor])
            elif neighbor in on_stack:
                low_links[node] = min(low_links[node], indices[neighbor])
        
        if low_links[node] == indices[node]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == node:
                    break
            components.append(component)
    
    for node in graph:
        if node not in indices:
            strongconnect(node)
    
    return components


"""graph = {
    0: [1, 2],
    1: [0],
    2: [0, 3],
    3: [2],
    4: [5],
    5: [4],
    6: []
}"""

# from wiki picture
# https://en.wikipedia.org/wiki/Strongly_connected_component
graph = {
    0: [1],
    1: [2, 3, 5],
    2: [0, 3],
    3: [4],
    4: [3],
    5: [4, 6],
    6: [5, 7],
    7: [4, 6]
}

components = kosaraju(graph)
print("Strongly connected components (kosaraju):")
for i, component in enumerate(components, 1):
    print(f"Component {i}: {component}")


components = tarjan(graph)
print("Strongly connected components (tarjan):")
for i, component in enumerate(components, 1):
    print(f"Component {i}: {component}")