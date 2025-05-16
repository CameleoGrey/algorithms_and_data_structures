
"""
A BST is a binary tree where for each node:

All nodes in the left subtree have values less than the node's value.
All nodes in the right subtree have values greater than the node's value.
This property allows efficient search, insertion, and deletion operations.

Summary
Supports insertion, search, deletion.
Inorder traversal returns sorted keys.
No duplicates are inserted.
"""


class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert a key into the BST."""
        if self.root is None:
            self.root = BSTNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
            else:
                self._insert(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key)
            else:
                self._insert(node.right, key)
        # If key == node.key, do nothing (no duplicates)

    def search(self, key):
        """Search for a key in the BST. Returns True if found, else False."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def inorder_traversal(self):
        """Return a list of keys in inorder."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def delete(self, key):
        """Delete a key from the BST."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children: get inorder successor
            min_larger_node = self._min_value_node(node.right)
            node.key = min_larger_node.key
            node.right = self._delete(node.right, min_larger_node.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

# Usage example
bst = BinarySearchTree()

# Insert elements
for num in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(num)

# Search for elements
print("Search 40:", bst.search(40))  # True
print("Search 25:", bst.search(25))  # False

# Inorder traversal (should be sorted)
print("Inorder traversal:", bst.inorder_traversal())

# Delete a node
bst.delete(70)
print("Inorder after deleting 70:", bst.inorder_traversal())
