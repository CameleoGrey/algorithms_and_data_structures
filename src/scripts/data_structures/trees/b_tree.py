

"""
A B-tree is a self-balancing search tree optimized for systems that read and write large blocks of data. 
It maintains sorted data and allows efficient insertion, deletion, and search operations.

Key properties:
Each node contains multiple keys.
All leaves are at the same depth.
Nodes have a minimum and maximum number of keys (defined by the order t).

Insertion Operation
Process:
Locate the correct leaf node where the new key should be inserted (using the search process).
Insert the key into the leaf node in sorted order.
Handle overflow:
If the node exceeds the maximum number of keys, split the node into two.
Promote the middle key to the parent node.
If the parent overflows, split it as well, propagating upward.
If the root splits, a new root is created, increasing the height of the tree.
Example:
Inserting key K:

Find the leaf node.
Insert K in sorted order.
If the node has too many keys, split it:
For example, if the node has 4 keys and the maximum is 3, split into two nodes with 2 keys each.
Promote the middle key to the parent.

Deletion Operation
Process:
Find the key to delete.
If the key is in an internal node:
Replace it with its in-order predecessor or successor (from a leaf).
Delete the predecessor/successor from the leaf.
If the key is in a leaf:
Remove it directly.
Handle underflow:
If a node has fewer than the minimum number of keys, rebalance:
Borrow a key from a sibling if possible.
Or merge with a sibling and adjust the parent.
Continue rebalancing upward if necessary.

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
        
        # The key that will move up to the parent
        median_key = node.keys[t - 1]
        
        # Move second half of keys to new node (excluding median)
        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]
        
        # Move children if not leaf
        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]
        
        # Insert median key into parent
        parent.keys.insert(i, median_key)
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

# Test the B-tree
b_tree = BTree(t=3)
for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    b_tree.insert(key)

print("B-Tree traversal:")
b_tree.traverse()
print()

search_key = 12
result = b_tree.search(search_key)
if result:
    node, index = result
    print(f"Found key {search_key} in node: {node}")
else:
    print(f"Key {search_key} not found.")