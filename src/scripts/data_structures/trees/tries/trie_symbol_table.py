
"""
Trie Symbol Table 

When to Choose Which?
Use insert(word) if:
You only need to check word existence or prefixes (e.g., autocomplete).
Memory efficiency is critical.

Use insert(key, value) if:
You're building a prefix-aware dictionary (e.g., storing definitions).
You need to retrieve data by string keys (e.g., router paths, file systems).
Both are "correct" but serve different engineering needs. The choice depends on whether your problem requires keys-only or key-value pairs.

Key Features:
Complete Symbol Table Operations:
put(key, value) - Insert/update key-value pairs
get(key) - Retrieve values
delete(key) - Remove entries
contains(key) - Membership check

Advanced Trie Functionality:
Prefix searches (keys_with_prefix())
Longest prefix matching (longest_prefix_of())
Complete key listing (keys())
Size tracking (size(), is_empty())

Efficient Memory Management:
Automatic cleanup of empty nodes after deletion
Count tracking for quick size operations


"""

class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.value = None   # Value associated with this node
        self.count = 0      # Count of words in this subtree

class TrieSymbolTable:
    def __init__(self):
        self.root = TrieNode()
    
    def put(self, key, value):
        """Insert or update a key-value pair"""
        if value is None:
            self.delete(key)
            return
        
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # Update count if this is a new key
        if node.value is None:
            self._update_counts(key, 1)
        node.value = value
    
    def get(self, key):
        """Retrieve the value for a key"""
        node = self._get_node(key)
        return node.value if node else None
    
    def contains(self, key):
        """Check if key exists in the trie"""
        return self.get(key) is not None
    
    def delete(self, key):
        """Remove a key-value pair"""
        if not self.contains(key):
            return
        
        # Mark as deleted first
        node = self._get_node(key)
        node.value = None
        self._update_counts(key, -1)
        
        # Clean up empty nodes
        self._cleanup(key)
    
    def size(self):
        """Total number of key-value pairs"""
        return self.root.count
    
    def is_empty(self):
        """Check if trie is empty"""
        return self.size() == 0
    
    def keys(self):
        """Return all keys in the trie"""
        return self.keys_with_prefix("")
    
    def keys_with_prefix(self, prefix):
        """Return keys starting with given prefix"""
        results = []
        node = self._get_node(prefix)
        if node:
            self._collect(node, prefix, results)
        return results
    
    def longest_prefix_of(self, query):
        """Find longest key that is a prefix of query"""
        node = self.root
        length = 0
        for i, char in enumerate(query):
            if char not in node.children:
                break
            node = node.children[char]
            if node.value is not None:
                length = i + 1
        return query[:length]
    
    # Helper methods
    def _get_node(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _update_counts(self, key, delta):
        node = self.root
        node.count += delta
        for char in key:
            node = node.children[char]
            node.count += delta
    
    def _cleanup(self, key):
        nodes = []
        node = self.root
        nodes.append((node, None))  # (node, parent_char)
        
        # Collect all nodes along the path
        for char in key:
            if char not in node.children:
                return
            node = node.children[char]
            nodes.append((node, char))
        
        # Remove empty nodes from the end up
        for i in range(len(nodes)-1, 0, -1):
            node, char = nodes[i]
            parent_node, _ = nodes[i-1]
            
            if node.value is None and len(node.children) == 0 and node.count == 0:
                del parent_node.children[char]
    
    def _collect(self, node, prefix, results):
        if node.value is not None:
            results.append(prefix)
        for char, child in node.children.items():
            self._collect(child, prefix + char, results)


# Usage Examples
if __name__ == "__main__":
    print("Trie Symbol Table Demonstration")
    print("=============================")
    
    # Initialize trie
    trie = TrieSymbolTable()
    
    # Insert key-value pairs
    print("\nInserting key-value pairs:")
    pairs = [
        ("apple", 5),
        ("app", 2),
        ("banana", 7),
        ("band", 3),
        ("bat", 4),
        ("zoo", 6)
    ]
    
    for key, value in pairs:
        trie.put(key, value)
        print(f"Inserted: {key} -> {value}")
    
    # Check size
    print(f"\nCurrent size: {trie.size()}")
    
    # Retrieve values
    print("\nGetting values:")
    test_keys = ["apple", "app", "orange", "band"]
    for key in test_keys:
        value = trie.get(key)
        print(f"Key '{key}': {value if value is not None else 'Not found'}")
    
    # Check contains
    print("\nContains checks:")
    print(f"'banana' exists: {trie.contains('banana')}")
    print(f"'pear' exists: {trie.contains('pear')}")
    
    # Prefix search
    print("\nKeys with prefix 'ba':")
    print(trie.keys_with_prefix("ba"))
    
    # Longest prefix
    print("\nLongest prefix of 'bandana':")
    print(trie.longest_prefix_of("bandana"))
    
    # All keys
    print("\nAll keys in trie:")
    print(trie.keys())
    
    # Delete operations
    print("\nDeleting 'app' and 'band'")
    trie.delete("app")
    trie.delete("band")
    
    print("\nKeys after deletion:")
    print(trie.keys())
    print(f"New size: {trie.size()}")
    
    # Edge cases
    print("\nEdge case testing:")
    print("Empty trie check:", trie.is_empty())
    print("Get non-existent key 'pear':", trie.get("pear"))
    print("Longest prefix of 'application':", trie.longest_prefix_of("application"))