

"""
A B-tree is a self-balancing search tree optimized for systems that read and write large blocks of data. 
It maintains sorted data and allows efficient insertion, deletion, and search operations.

Key properties:
Each node contains multiple keys.
All leaves are at the same depth.
Nodes have a minimum and maximum number of keys (defined by the order t).

Summary
The BTree class supports insertion, search, and traversal.
The minimum degree t controls the range of keys per node.
The implementation handles node splitting and maintains balance.
Let me know if you'd like me to add deletion, more detailed traversal, or other features!
"""


class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.keys = []  # List of keys
        self.children = []  # List of child nodes
        self.leaf = leaf  # Is leaf node

    def __repr__(self):
        return f"Node(keys={self.keys}, leaf={self.leaf})"

class BTree:
    def __init__(self, t):
        self.t = t  # Minimum degree
        self.root = BTreeNode(t, leaf=True)

    def search(self, k, node=None):
        """Search for key k starting from node."""
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)
        elif node.leaf:
            return None
        else:
            return self.search(k, node.children[i])

    def insert(self, k):
        """Insert key k into the B-tree."""
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(self.root)
            self.root = new_root
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)

    def _split_child(self, parent, i):
        """Split the child of parent at index i."""
        t = self.t
        node = parent.children[i]
        new_node = BTreeNode(t, leaf=node.leaf)
        # Move second half of keys to new node
        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]
        # Move children if not leaf
        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]
        # Insert new node into parent
        parent.keys.insert(i, node.keys.pop())
        parent.children.insert(i + 1, new_node)

    def _insert_non_full(self, node, k):
        """Insert key into a node that is not full."""
        i = len(node.keys) - 1
        if node.leaf:
            # Insert key in sorted order
            node.keys.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            # Move down the tree
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def traverse(self, node=None):
        """Traverse and print the tree."""
        if node is None:
            node = self.root
        for i in range(len(node.keys)):
            if not node.leaf:
                self.traverse(node.children[i])
            print(node.keys[i], end=' ')
        if not node.leaf:
            self.traverse(node.children[len(node.keys)])

# Create a B-tree of minimum degree 3
b_tree = BTree(t=3)

# Insert some keys
for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    b_tree.insert(key)

# Traverse the tree
print("B-Tree traversal:")
b_tree.traverse()
print()

# Search for a key
search_key = 12
result = b_tree.search(search_key)
if result:
    node, index = result
    print(f"Found key {search_key} in node: {node}")
else:
    print(f"Key {search_key} not found.")
