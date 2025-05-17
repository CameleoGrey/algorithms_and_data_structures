
"""
A 2-3 Tree is a balanced search tree where each internal node has either 2 or 3 children, 
and all leaves are at the same depth. It maintains balance through node splitting during insertions.

Summary
Supports insertion with balancing via node splitting.
Supports search operation.
Traversal returns elements in sorted order.
"""

class Node23:
    def __init__(self, keys=None, children=None):
        self.keys = keys or []  # List of 1 or 2 keys
        self.children = children or []  # List of 2 or 3 children

    def is_leaf(self):
        return len(self.children) == 0

    def insert_key(self, key):
        self.keys.append(key)
        self.keys.sort()

    def split(self):
        # Split a node with 3 keys into two nodes and promote middle key
        middle_key = self.keys[1]
        left_node = Node23([self.keys[0]], self.children[:2])
        right_node = Node23([self.keys[2]], self.children[2:])
        return middle_key, left_node, right_node

class TwoThreeTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node23([key])
            return
        
        # Perform insertion
        split_result = self._insert(self.root, key)
        
        # Handle root split if needed
        if split_result:
            left, right, promoted_key = split_result
            self.root = Node23([promoted_key], [left, right])

    def _insert(self, node, key):
        if node.is_leaf():
            node.insert_key(key)
            if len(node.keys) > 2:
                middle, left, right = node.split()
                return left, right, middle
            return None
        
        # Internal node: find the correct child
        if key < node.keys[0]:
            index = 0
        elif len(node.keys) == 1 or key < node.keys[1]:
            index = 1
        else:
            index = 2
            
        # Recursive insertion
        split_result = self._insert(node.children[index], key)
        
        if split_result:
            left, right, promoted_key = split_result
            # Insert promoted key into current node
            node.keys.insert(index, promoted_key)
            node.children[index] = left
            node.children.insert(index + 1, right)
            
            if len(node.keys) > 2:
                middle, new_left, new_right = node.split()
                return new_left, new_right, middle
                
        return None

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key in node.keys:
            return True
        if node.is_leaf():
            return False
        if key < node.keys[0]:
            return self._search(node.children[0], key)
        elif len(node.keys) == 1 or key < node.keys[1]:
            return self._search(node.children[1], key)
        else:
            return self._search(node.children[2], key)

    def traverse(self):
        def _traverse(node):
            if node is None:
                return []
            result = []
            if node.is_leaf():
                result.extend(node.keys)
            else:
                result.extend(_traverse(node.children[0]))
                result.extend(node.keys[:1])
                result.extend(_traverse(node.children[1]))
                if len(node.keys) > 1:
                    result.extend(_traverse(node.children[2]))
            return result
        return _traverse(self.root)

# Test the corrected implementation
tree = TwoThreeTree()
for num in [10, 20, 5, 15, 25, 30, 2]:
    tree.insert(num)
print("Tree traversal:", tree.traverse())  # Should print [2, 5, 10, 15, 20, 25, 30]
print("Search 15:", tree.search(15))      # Should print True
print("Search 100:", tree.search(100))    # Should print False