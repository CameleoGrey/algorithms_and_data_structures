

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
    
    def is_full(self):
        return len(self.keys) == 2 * self.t - 1

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
    
    def delete(self, k):
        self._delete(self.root, k)
        # If root has no keys but has children, make first child the new root
        if not self.root.keys and self.root.children:
            self.root = self.root.children[0]

    def _delete(self, node, k):
        t = self.t
        idx = 0
        while idx < len(node.keys) and k > node.keys[idx]:
            idx += 1

        # Case 1: Key is present in this node
        if idx < len(node.keys) and node.keys[idx] == k:
            if node.leaf:
                node.keys.pop(idx)  # Simple removal from leaf
            else:
                # Case 2: Internal node
                self._delete_internal_node(node, idx)
        else:
            if node.leaf:
                print(f"Key {k} not found in the tree")
                return

            # Case 3: Key is not in this node, recurse to appropriate child
            flag = (idx == len(node.keys))
            if len(node.children[idx].keys) < t:
                self._fill(node, idx)

            if flag and idx > len(node.keys):
                self._delete(node.children[idx-1], k)
            else:
                self._delete(node.children[idx], k)

    def _delete_internal_node(self, node, idx):
        t = self.t
        k = node.keys[idx]

        # Case 2a: Left child has at least t keys
        if len(node.children[idx].keys) >= t:
            pred = self._get_predecessor(node.children[idx])
            node.keys[idx] = pred
            self._delete(node.children[idx], pred)

        # Case 2b: Right child has at least t keys
        elif len(node.children[idx+1].keys) >= t:
            succ = self._get_successor(node.children[idx+1])
            node.keys[idx] = succ
            self._delete(node.children[idx+1], succ)

        # Case 2c: Both children have t-1 keys, merge them
        else:
            self._merge(node, idx)
            self._delete(node.children[idx], k)

    def _get_predecessor(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def _fill(self, node, idx):
        t = self.t
        if idx != 0 and len(node.children[idx-1].keys) >= t:
            self._borrow_from_prev(node, idx)
        elif idx != len(node.children) - 1 and len(node.children[idx+1].keys) >= t:
            self._borrow_from_next(node, idx)
        else:
            if idx != len(node.children) - 1:
                self._merge(node, idx)
            else:
                self._merge(node, idx-1)

    def _borrow_from_prev(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx-1]

        # Move key from node down to child
        child.keys.insert(0, node.keys[idx-1])
        
        # Move last key from sibling up to node
        node.keys[idx-1] = sibling.keys.pop()
        
        # Move child pointer if not leaf
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx+1]

        # Move key from node down to child
        child.keys.append(node.keys[idx])
        
        # Move first key from sibling up to node
        node.keys[idx] = sibling.keys.pop(0)
        
        # Move child pointer if not leaf
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, node, idx):
        t = self.t
        child = node.children[idx]
        sibling = node.children[idx+1]

        # Pull a key from the current node into child
        child.keys.append(node.keys.pop(idx))
        
        # Move keys from sibling to child
        child.keys.extend(sibling.keys)
        
        # Move children if not leaf
        if not child.leaf:
            child.children.extend(sibling.children)
        
        # Remove sibling
        node.children.pop(idx+1)

    def find_min(self, node=None):
        """Find the minimum key in the tree."""
        if node is None:
            node = self.root
        while not node.leaf:
            node = node.children[0]
        return node.keys[0] if node.keys else None

    def find_max(self, node=None):
        """Find the maximum key in the tree."""
        if node is None:
            node = self.root
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1] if node.keys else None

    def count_keys(self, node=None):
        """Count total number of keys in the tree."""
        if node is None:
            node = self.root
        count = len(node.keys)
        if not node.leaf:
            for child in node.children:
                count += self.count_keys(child)
        return count

    def count_nodes(self, node=None):
        """Count total number of nodes in the tree."""
        if node is None:
            node = self.root
        count = 1  # Count this node
        if not node.leaf:
            for child in node.children:
                count += self.count_nodes(child)
        return count

    def height(self, node=None):
        """Calculate the height of the tree."""
        if node is None:
            node = self.root
        if node.leaf:
            return 1
        return 1 + self.height(node.children[0])

    def range_query(self, low, high, node=None, result=None):
        """Find all keys in the range [low, high]."""
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        i = 0
        while i < len(node.keys):
            if not node.leaf:
                self.range_query(low, high, node.children[i], result)
            
            if low <= node.keys[i] <= high:
                result.append(node.keys[i])
            
            i += 1
        
        if not node.leaf:
            self.range_query(low, high, node.children[i], result)
        
        return result

    def update_key(self, old_key, new_key):
        """Update an existing key to a new value."""
        # First delete the old key
        result = self.search(old_key)
        if not result:
            print(f"Key {old_key} not found in the tree")
            return False
        
        # Delete and re-insert
        self.delete(old_key)
        self.insert(new_key)
        return True

# Test the B-tree
b_tree = BTree(t=100)
for key in [100000 - i for i in range(100000)]:
    b_tree.insert(key)

print("B-Tree traversal:")
#b_tree.traverse()
print()

search_key = 12
result = b_tree.search(search_key)
if result:
    node, index = result
    print(f"Found key {search_key} in node: {node}")
else:
    print(f"Key {search_key} not found.")

print("Minimum key:", b_tree.find_min())
print("Maximum key:", b_tree.find_max())
print("Total keys:", b_tree.count_keys())
print("Total nodes:", b_tree.count_nodes())
print("Tree height:", b_tree.height())
print("Keys in range [7, 17]:", b_tree.range_query(7, 17))

# Test delete and update
print("\nDeleting key 12:")
b_tree.delete(12)
#b_tree.traverse()
print()

print("\nUpdating key 7 to 8:")
b_tree.update_key(7, 8)
#b_tree.traverse()
print()