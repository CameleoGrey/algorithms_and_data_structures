
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
        new_root, _ = self._insert(self.root, key)
        if new_root:
            self.root = new_root

    def _insert(self, node, key):
        if node.is_leaf():
            node.insert_key(key)
            if len(node.keys) > 2:
                return self._split_node(node)
            return None, None
        # Internal node
        # Decide which child to descend
        if key < node.keys[0]:
            index = 0
        elif len(node.keys) == 1 or key < node.keys[1]:
            index = 1
        else:
            index = 2
        child = node.children[index]
        new_child, promoted = self._insert(child, key)
        if new_child:
            # Insert promoted key into current node
            node.keys.insert(index, promoted)
            node.children[index] = new_child[0]
            node.children.insert(index + 1, new_child[1])
            if len(node.keys) > 2:
                return self._split_node(node)
        return None, None

    def _split_node(self, node):
        middle_key, left_node, right_node = node.split()
        return (left_node, right_node), middle_key

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
                result.extend(node.keys)
                result.extend(_traverse(node.children[1]))
                if len(node.children) == 3:
                    result.extend(_traverse(node.children[2]))
            return result
        return _traverse(self.root)

# Usage example
tree = TwoThreeTree()

# Insert elements
for num in [10, 20, 5, 15, 25, 30, 2]:
    tree.insert(num)

# Search for elements
print("Search 15:", tree.search(15))  # True
print("Search 100:", tree.search(100))  # False

# Traverse the tree
print("Tree traversal:", tree.traverse())
