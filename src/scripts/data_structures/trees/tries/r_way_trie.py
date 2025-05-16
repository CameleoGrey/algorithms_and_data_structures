

"""
An R-way Trie is a generalization of a Trie where each node 
has up to R children, typically used for fixed alphabets (like ASCII). 
It is efficient for prefix-based searches and symbol tables.

Summary
insert(key, value): Adds a key-value pair.
search(key): Retrieves the value for a key.
starts_with(prefix): Retrieves all key-value pairs with keys starting with the prefix.
This implementation assumes ASCII characters (size 256). For other alphabets, adjust R accordingly.
"""

class RTrieNode:
    def __init__(self, R):
        self.R = R
        self.children = [None] * R
        self.value = None

class RTrie:
    def __init__(self, R=256):
        self.R = R  # Size of alphabet, e.g., 256 for extended ASCII
        self.root = RTrieNode(R)

    def _char_to_index(self, ch):
        # Convert character to index (assuming ASCII)
        return ord(ch)

    def insert(self, key, value):
        node = self.root
        for ch in key:
            idx = self._char_to_index(ch)
            if node.children[idx] is None:
                node.children[idx] = RTrieNode(self.R)
            node = node.children[idx]
        node.value = value

    def search(self, key):
        node = self.root
        for ch in key:
            idx = self._char_to_index(ch)
            if node.children[idx] is None:
                return None
            node = node.children[idx]
        return node.value

    def starts_with(self, prefix):
        """Return list of all keys starting with prefix."""
        results = []

        def dfs(node, path):
            if node.value is not None:
                results.append((''.join(path), node.value))
            for i, child in enumerate(node.children):
                if child is not None:
                    dfs(child, path + [chr(i)])

        # Traverse to the node corresponding to prefix
        node = self.root
        for ch in prefix:
            idx = self._char_to_index(ch)
            if node.children[idx] is None:
                return []
            node = node.children[idx]
        dfs(node, list(prefix))
        return results

# Usage example
trie = RTrie(R=256)

# Insert key-value pairs
trie.insert("cat", 1)
trie.insert("car", 2)
trie.insert("dog", 3)
trie.insert("cart", 4)
trie.insert("dogma", 5)

# Search for keys
print("Search 'cat':", trie.search("cat"))  # Output: 1
print("Search 'car':", trie.search("car"))  # Output: 2
print("Search 'cow':", trie.search("cow"))  # Output: None

# Find all keys starting with a prefix
print("Keys starting with 'ca':", trie.starts_with("ca"))
# Output: [('cat', 1), ('car', 2), ('cart', 4)]

print("Keys starting with 'do':", trie.starts_with("do"))
# Output: [('dog', 3), ('dogma', 5)]
