

"""
A Radix Tree (also called a Patricia Trie or Compact Prefix Tree) is a 
space-optimized version of a Trie (prefix tree) that merges nodes with a single child, 
reducing memory overhead while maintaining fast search, insert, and delete operations. 
It's particularly efficient for string keys or IP routing tables.

How It Works
Key Features
Compressed Paths
Unlike a standard Trie (where each character is a node), a Radix Tree merges single-child nodes into a single edge with a combined string label.
Saves memory by reducing the number of nodes.

Prefix-Based Lookup
Keys are stored based on shared prefixes (e.g., "apple" and "appetizer" share the prefix "app").
Enables efficient longest-prefix matching (useful in IP routing).

Insert/Delete/Search: O(k) (where k = key length).
Memory: More efficient than a standard Trie.

ART (Adaptive Radix Tree)
Optimizes for CPU cache efficiency (used in databases like PostgreSQL).

HAT-Trie
Hybrid of a Radix Tree and hash table for faster lookups.

Summary
Radix Trees compress shared prefixes to save memory.
Faster than Tries for string operations.
Ideal for prefix searches, routing, and autocomplete.
Not as fast as hash tables for exact lookups but more flexible for text processing.
"""

class RadixTreeNode:
    def __init__(self, prefix: str = "", is_leaf: bool = False):
        self.prefix = prefix      # Prefix stored at this edge
        self.children = {}        # Child nodes (key: next character)
        self.is_leaf = is_leaf    # Marks if this node represents a complete key

    def __str__(self):
        return f"Node(prefix='{self.prefix}', is_leaf={self.is_leaf})"


class RadixTree:
    def __init__(self):
        self.root = RadixTreeNode()

    def insert(self, key: str) -> None:
        """Insert a key into the Radix Tree."""
        node = self.root
        i = 0  # Current position in the key

        while i < len(key):
            matched = False
            for child_prefix, child_node in node.children.items():
                # Find the length of the common prefix
                common_len = 0
                min_len = min(len(child_prefix), len(key[i:]))
                while common_len < min_len and child_prefix[common_len] == key[i + common_len]:
                    common_len += 1

                if common_len == 0:
                    continue

                # Case 1: Exact match with child prefix
                if common_len == len(child_prefix):
                    node = child_node
                    i += common_len
                    matched = True
                    break

                # Case 2: Partial match - need to split the node
                # Create new node for the split part
                split_node = RadixTreeNode(
                    prefix=child_prefix[common_len:],
                    is_leaf=child_node.is_leaf
                )
                split_node.children = child_node.children

                # Update the existing child node
                new_node = RadixTreeNode(
                    prefix=child_prefix[:common_len],
                    is_leaf=False
                )
                new_node.children[child_prefix[common_len]] = split_node

                # Replace the old child with the new node
                del node.children[child_prefix]
                node.children[child_prefix[:common_len]] = new_node
                node = new_node
                i += common_len
                matched = True
                break

            if not matched:
                # No matching child - create new leaf node
                new_node = RadixTreeNode(prefix=key[i:], is_leaf=True)
                node.children[key[i:]] = new_node
                return

        # Mark current node as leaf if we've reached the end
        node.is_leaf = True

    def search(self, key: str) -> bool:
        """Check if a key exists in the tree."""
        node = self.root
        i = 0

        while i < len(key):
            matched = False
            for child_prefix, child_node in node.children.items():
                if key.startswith(child_prefix, i):
                    node = child_node
                    i += len(child_prefix)
                    matched = True
                    break

            if not matched:
                return False

        return node.is_leaf

    def delete(self, key: str) -> bool:
        """Delete a key from the tree (if it exists)."""
        path = []
        node = self.root
        i = 0

        # Traverse the tree to find the key
        while i < len(key):
            matched = False
            for child_prefix, child_node in node.children.items():
                if key.startswith(child_prefix, i):
                    path.append((node, child_prefix, child_node))
                    node = child_node
                    i += len(child_prefix)
                    matched = True
                    break

            if not matched:
                return False  # Key not found

        if not node.is_leaf:
            return False  # Key not a complete word

        # Mark as non-leaf and clean up
        node.is_leaf = False

        # Merge nodes if possible
        while path and not node.is_leaf and len(node.children) <= 1:
            parent, prefix, _ = path.pop()
            
            if len(node.children) == 1:
                # Merge with only child
                child_prefix, child_node = next(iter(node.children.items()))
                new_prefix = prefix + child_prefix
                parent.children[new_prefix] = child_node
                del parent.children[prefix]
            elif len(node.children) == 0:
                # Remove empty node
                del parent.children[prefix]
                
            node = parent

        return True

    def starts_with(self, prefix: str) -> list[str]:
        """Find all keys with the given prefix."""
        node = self.root
        i = 0
        result = []

        # Navigate to the prefix node
        while i < len(prefix):
            matched = False
            for child_prefix, child_node in node.children.items():
                if prefix.startswith(child_prefix, i):
                    node = child_node
                    i += len(child_prefix)
                    matched = True
                    break

            if not matched:
                return result  # No keys with this prefix

        # Collect all keys under this node
        self._collect_keys(node, prefix[:i], result)
        return result

    def _collect_keys(self, node: RadixTreeNode, current_prefix: str, result: list[str]) -> None:
        """Helper to collect all keys under a node."""
        if node.is_leaf:
            result.append(current_prefix + node.prefix)

        for child_prefix, child_node in node.children.items():
            self._collect_keys(child_node, current_prefix + node.prefix + child_prefix, result)

    def display(self, node=None, indent="", last=True):
        """Visualize the tree structure."""
        if node is None:
            node = self.root

        print(indent, end="")
        if last:
            print("└── ", end="")
            indent += "    "
        else:
            print("├── ", end="")
            indent += "│   "

        print(f"{node.prefix}{' (leaf)' if node.is_leaf else ''}")

        children = list(node.children.items())
        for i, (prefix, child_node) in enumerate(children):
            self.display(child_node, indent, i == len(children) - 1)


# Example Usage
if __name__ == "__main__":
    rt = RadixTree()

    # Insert keys
    rt.insert("apple")
    rt.insert("appetizer")
    rt.insert("banana")
    rt.insert("band")
    rt.insert("bat")

    print("Radix Tree Structure:")
    rt.display()

    # Search keys
    print("\nSearch Results:")
    print(f"'apple' exists? {rt.search('apple')}")       # True
    print(f"'app' exists? {rt.search('app')}")          # False
    print(f"'banana' exists? {rt.search('banana')}")    # True

    # Prefix search
    print("\nKeys starting with 'app':")
    print(rt.starts_with("app"))  # ['apple', 'appetizer']

    print("\nKeys starting with 'ba':")
    print(rt.starts_with("ba"))   # ['banana', 'band', 'bat']

    # Delete a key
    print("\nDeleting 'banana':")
    rt.delete("banana")
    print(f"'banana' exists after deletion? {rt.search('banana')}")  # False
    print("\nUpdated Tree Structure:")
    rt.display()