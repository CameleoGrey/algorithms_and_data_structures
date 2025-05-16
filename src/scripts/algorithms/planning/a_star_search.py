



import heapq
from math import sqrt

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic (estimated cost from current to end)
        self.f = 0  # Total cost (g + h)
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __repr__(self):
        return f"Node({self.position}, f={self.f})"

def heuristic(a, b):
    # Euclidean distance heuristic
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return sqrt(dx*dx + dy*dy)

def a_star_search(grid, start, end):
    """
    Perform A* search on a 2D grid.
    
    Parameters:
    - grid: 2D list where 0 represents walkable and 1 represents blocked
    - start: tuple (x, y) representing start position
    - end: tuple (x, y) representing end position
    
    Returns:
    - path: list of positions as tuples from start to end, or None if no path exists
    """
    
    # Create start and end nodes
    start_node = Node(start)
    end_node = Node(end)
    
    # Initialize both open and closed lists
    open_list = []
    closed_list = []
    
    # Add the start node
    heapq.heappush(open_list, start_node)
    
    # Define possible movements (4-directional or 8-directional)
    movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 4-directional
    # movements = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8-directional
    
    # Loop until the open list is empty
    while open_list:
        # Get the current node (node with lowest f)
        current_node = heapq.heappop(open_list)
        
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path
        
        # Generate children
        children = []
        for move in movements:
            # Get node position
            node_position = (current_node.position[0] + move[0], 
                             current_node.position[1] + move[1])
            
            # Make sure within grid boundaries
            if (node_position[0] >= len(grid) or node_position[0] < 0 or 
                node_position[1] >= len(grid[0]) or node_position[1] < 0):
                continue
            
            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] != 0:
                continue
            
            # Create new node
            new_node = Node(node_position, current_node)
            children.append(new_node)
        
        # Loop through children
        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue
            
            # Calculate f, g, and h values
            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h
            
            # Child is already in open list with lower g
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            
            # Add the child to the open list
            heapq.heappush(open_list, child)
        
        # Add current node to closed list
        closed_list.append(current_node)
    
    # No path found
    return None

# Example usage
if __name__ == "__main__":
    # Define a grid (0 = walkable, 1 = blocked)
    grid = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    end = (7, 6)
    
    path = a_star_search(grid, start, end)
    
    if path:
        print("Path found:")
        for step in path:
            print(step)
    else:
        print("No path found")