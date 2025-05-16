
"""
How to Use the KDTree:
Construction: Create with KDTree(points, k) where k is the number of dimensions
Insertion: Add new points with insert(point)
Nearest Neighbors: Find closest points with nearest_neighbor(target, k)
Range Search: Find points in a bounding box with range_search(bounds)

Applications of KD-Trees:
Spatial indexing for efficient range searches
Nearest neighbor queries in machine learning
Computer graphics for ray tracing acceleration
Geographic information systems (GIS)
Collision detection in physics simulations

The implementation uses NumPy for efficient distance calculations but can be modified to work without it if needed. 
The tree maintains balance during construction but may become unbalanced with many 
insertions (for a perfectly balanced tree, you would need to rebuild periodically).
"""


import heapq
from collections import deque
import numpy as np

class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:
    def __init__(self, points, k=2):
        """
        Initialize a k-d tree with given points.
        
        Parameters:
            points (list): List of k-dimensional points
            k (int): Number of dimensions
        """
        self.k = k
        self.root = self.build(points)
    
    def build(self, points, depth=0):
        if not points:
            return None
        
        # Select axis based on depth (cycles through all dimensions)
        axis = depth % self.k
        
        # Sort points and choose median as pivot
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2
        
        # Create node and construct subtrees
        return Node(
            point=points[median],
            left=self.build(points[:median], depth + 1),
            right=self.build(points[median + 1:], depth + 1)
        )
    
    def insert(self, point, node=None, depth=0):
        if node is None:
            return Node(point)
        
        axis = depth % self.k
        if point[axis] < node.point[axis]:
            node.left = self.insert(point, node.left, depth + 1)
        else:
            node.right = self.insert(point, node.right, depth + 1)
        
        return node
    
    def nearest_neighbor(self, target, k=1):
        """
        Find k nearest neighbors to target point.
        
        Returns:
            list: List of tuples (distance, point)
        """
        if self.root is None:
            return []
        
        # Use a max-heap to keep track of k nearest neighbors
        heap = []
        
        def search(node, depth=0):
            if node is None:
                return
            
            axis = depth % self.k
            distance = self._euclidean_distance(target, node.point)
            
            # Push to heap (using negative distance for max-heap simulation)
            if len(heap) < k:
                heapq.heappush(heap, (-distance, node.point))
            elif distance < -heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (-distance, node.point))
            
            # Decide which branch to explore first
            if target[axis] < node.point[axis]:
                search(node.left, depth + 1)
                # Check if we need to explore the other branch
                if len(heap) < k or (node.point[axis] - target[axis])**2 < -heap[0][0]:
                    search(node.right, depth + 1)
            else:
                search(node.right, depth + 1)
                # Check if we need to explore the other branch
                if len(heap) < k or (target[axis] - node.point[axis])**2 < -heap[0][0]:
                    search(node.left, depth + 1)
        
        search(self.root)
        return sorted([(-d, p) for d, p in heap])
    
    def _euclidean_distance(self, a, b):
        return np.sqrt(sum((a[i] - b[i])**2 for i in range(self.k)))
    
    def range_search(self, bounds):
        """
        Find all points within the given bounds.
        
        Parameters:
            bounds (list): List of tuples (min, max) for each dimension
        
        Returns:
            list: Points within the bounds
        """
        result = []
        
        def search(node, depth=0):
            if node is None:
                return
            
            axis = depth % self.k
            point = node.point
            
            # Check if current point is within bounds
            in_range = True
            for i in range(self.k):
                if not (bounds[i][0] <= point[i] <= bounds[i][1]):
                    in_range = False
                    break
            if in_range:
                result.append(point)
            
            # Decide which branches to explore
            if bounds[axis][0] <= point[axis]:
                search(node.left, depth + 1)
            if bounds[axis][1] >= point[axis]:
                search(node.right, depth + 1)
        
        search(self.root)
        return result
    
    def __str__(self):
        if not self.root:
            return "Empty KDTree"
        
        lines = []
        queue = deque([(self.root, 0)])
        
        while queue:
            node, level = queue.popleft()
            prefix = "    " * level
            lines.append(f"{prefix}Level {level}: {node.point}")
            
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))
        
        return "\n".join(lines)

# Example usage
if __name__ == "__main__":
    # Create some 2D points
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    
    # Build the KDTree
    kdtree = KDTree(points, k=2)
    print("KDTree structure:")
    print(kdtree)
    
    # Find nearest neighbors
    target = (6, 3)
    neighbors = kdtree.nearest_neighbor(target, k=3)
    print(f"\n3 nearest neighbors to {target}:")
    for dist, point in neighbors:
        print(f"Point: {point}, Distance: {dist:.2f}")
    
    # Range search
    bounds = [(3, 8), (2, 7)]  # x between 3-8, y between 2-7
    in_range = kdtree.range_search(bounds)
    print(f"\nPoints in range {bounds}:")
    for point in in_range:
        print(point)
    
    # Insert a new point
    new_point = (6, 5)
    kdtree.insert(new_point)
    print(f"\nAfter inserting {new_point}:")
    print(kdtree)