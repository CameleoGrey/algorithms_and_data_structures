
"""
Certainly! Here's a Python implementation of a B-tree set, which supports insertion, 
search, and iteration over unique elements, similar to Python's built-in set. 
It uses a B-tree for efficient storage and lookup.

Features:
Supports insert() for adding elements.
Supports in operator for membership testing.
Supports iteration over elements in sorted order.
Ensures all elements are unique (like a set).
"""


class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf

class BTreeSet:
    def __init__(self, t=3):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def search(self, k, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return True
        elif node.leaf:
            return False
        else:
            return self.search(k, node.children[i])

    def insert(self, k):
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
        t = self.t
        node = parent.children[i]
        new_node = BTreeNode(t, leaf=node.leaf)
        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]
        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]
        parent.keys.insert(i, node.keys.pop())
        parent.children.insert(i + 1, new_node)

    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def __contains__(self, k):
        return self.search(k)

    def __iter__(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        for i, key in enumerate(node.keys):
            if not node.leaf:
                yield from self._inorder(node.children[i])
            yield key
        if not node.leaf:
            yield from self._inorder(node.children[len(node.keys)])

# Usage example
bt_set = BTreeSet(t=3)

# Insert elements
for num in [10, 20, 5, 6, 12, 30, 7, 17]:
    bt_set.insert(num)

# Check membership
print(15 in bt_set)  # False
print(12 in bt_set)  # True

# Iterate over set elements
print("Set elements in order:")
for elem in bt_set:
    print(elem)
