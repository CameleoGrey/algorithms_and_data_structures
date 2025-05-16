

"""
A TST is a space-efficient data structure similar to a Trie, 
where each node has three children: less, equal, and greater. 
It is especially useful for storing strings with efficient prefix search and symbol table operations.
"""

class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.middle = None
        self.right = None
        self.value = None

class TernarySearchTrie:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        def _insert(node, key, index):
            ch = key[index]
            if node is None:
                node = TSTNode(ch)
            if ch < node.char:
                node.left = _insert(node.left, key, index)
            elif ch > node.char:
                node.right = _insert(node.right, key, index)
            else:
                if index + 1 == len(key):
                    node.value = value
                else:
                    node.middle = _insert(node.middle, key, index + 1)
            return node

        self.root = _insert(self.root, key, 0)

    def search(self, key):
        def _search(node, key, index):
            if node is None:
                return None
            ch = key[index]
            if ch < node.char:
                return _search(node.left, key, index)
            elif ch > node.char:
                return _search(node.right, key, index)
            else:
                if index + 1 == len(key):
                    return node.value
                return _search(node.middle, key, index + 1)

        return _search(self.root, key, 0)

    def starts_with(self, prefix):
        results = []

        def _collect(node, prefix_so_far):
            if node is None:
                return
            # Traverse left subtree
            _collect(node.left, prefix_so_far)
            # Check middle subtree
            new_prefix = prefix_so_far + node.char
            if node.value is not None:
                results.append((new_prefix, node.value))
            _collect(node.middle, new_prefix)
            # Traverse right subtree
            _collect(node.right, prefix_so_far)

        def _find_node(node, prefix, index):
            if node is None:
                return None
            ch = prefix[index]
            if ch < node.char:
                return _find_node(node.left, prefix, index)
            elif ch > node.char:
                return _find_node(node.right, prefix, index)
            else:
                if index + 1 == len(prefix):
                    return node
                return _find_node(node.middle, prefix, index + 1)

        start_node = _find_node(self.root, prefix, 0)
        if start_node:
            _collect(start_node, prefix[:-1])
        return results

# Usage example
tst = TernarySearchTrie()

# Insert key-value pairs
tst.insert("cat", 1)
tst.insert("cap", 2)
tst.insert("dog", 3)
tst.insert("cart", 4)
tst.insert("cattle", 5)

# Search for keys
print("Search 'cat':", tst.search("cat"))  # Output: 1
print("Search 'cap':", tst.search("cap"))  # Output: 2
print("Search 'cow':", tst.search("cow"))  # Output: None

# Find all keys starting with a prefix
print("Keys starting with 'ca':", tst.starts_with("ca"))
# Output: [('cat', 1), ('cap', 2), ('cart', 4), ('cattle', 5)]
