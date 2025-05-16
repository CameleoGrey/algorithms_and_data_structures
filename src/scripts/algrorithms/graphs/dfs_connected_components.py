



def find_connected_components(graph):
    visited = set()
    components = []
    
    for node in graph:
        if node not in visited:
            # Start a new component
            component = set()
            stack = [node]
            
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    component.add(current)
                    # Add all unvisited neighbors to the stack
                    for neighbor in graph.get(current, []):
                        if neighbor not in visited:
                            stack.append(neighbor)
            
            components.append(component)
    
    return components

# Example graph (undirected)
graph = {
    0: [1, 2],
    1: [0],
    2: [0, 3],
    3: [2],
    4: [5],
    5: [4],
    6: []
}

components = find_connected_components(graph)
print("Connected components:")
for i, component in enumerate(components, 1):
    print(f"Component {i}: {component}")