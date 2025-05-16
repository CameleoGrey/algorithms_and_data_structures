
"""

Simple (word) Trie

When to Choose Which?
Use insert(word) if:
You only need to check word existence or prefixes (e.g., autocomplete).
Memory efficiency is critical.

Use insert(key, value) if:
You're building a prefix-aware dictionary (e.g., storing definitions).
You need to retrieve data by string keys (e.g., router paths, file systems).
Both are "correct" but serve different engineering needs. The choice depends on whether your problem requires keys-only or key-value pairs.

Key Features
Core Operations:
insert(word): Adds a word to the trie
search(word): Checks if a complete word exists
starts_with(prefix): Checks if any word starts with the prefix
delete(word): Removes a word from the trie

Extended Functionality:
get_all_words(): Returns all stored words
autocomplete(prefix): Finds all words starting with prefix
count_words(): Returns the total number of words

Space Efficiency:
Only stores necessary characters for words with common prefixes
More memory efficient than hash tables for many similar strings

Time Complexity:
Insertion: O(m) where m is word length
Search: O(m) where m is word length
Prefix search: O(m) where m is prefix length

Practical Applications
Autocomplete systems
Spell checkers
IP routing (longest prefix matching)
Word games (finding all words with given letters)
Search engines (prefix-based suggestions)
The implementation includes proper cleanup during deletion to maintain efficient memory usage by removing unnecessary nodes when they're no longer part of any word.
"""


class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Marks if this node completes a word

class Trie:
    def __init__(self):
        self.root = TrieNode()  # Initialize with empty root node
    
    def insert(self, word):
        """Inserts a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # Create new node if char doesn't exist
            node = node.children[char]  # Move to child node
        node.is_end_of_word = True  # Mark end of word
    
    def search(self, word):
        """Returns True if the word is in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False  # Character not found
            node = node.children[char]
        return node.is_end_of_word  # Check if it's a complete word
    
    def starts_with(self, prefix):
        """Returns True if any word in the trie starts with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False  # Prefix not found
            node = node.children[char]
        return True  # Prefix exists in trie
    
    def delete(self, word):
        """Deletes a word from the trie if it exists."""
        def _delete_helper(node, word, index):
            if index == len(word):
                # If word exists in trie, unmark end of word
                if node.is_end_of_word:
                    node.is_end_of_word = False
                    # Return True if node has no children (can be removed)
                    return len(node.children) == 0
                return False  # Word doesn't exist
            
            char = word[index]
            if char not in node.children:
                return False  # Word doesn't exist
            
            should_delete_child = _delete_helper(node.children[char], word, index + 1)
            
            if should_delete_child:
                # Remove the child node if it's safe to do so
                del node.children[char]
                # Return True if current node has no other children and isn't end of another word
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        _delete_helper(self.root, word, 0)
    
    def get_all_words(self):
        """Returns all words stored in the trie."""
        words = []
        
        def _collect_words(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child_node in node.children.items():
                _collect_words(child_node, current_word + char)
        
        _collect_words(self.root, "")
        return words
    
    def autocomplete(self, prefix):
        """Returns all words that start with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # Prefix not found
            node = node.children[char]
        
        words = []
        def _collect_from_node(node, current_word):
            if node.is_end_of_word:
                words.append(prefix + current_word)
            for char, child_node in node.children.items():
                _collect_from_node(child_node, current_word + char)
        
        _collect_from_node(node, "")
        return words

    def count_words(self):
        """Returns the number of words stored in the trie."""
        count = 0
        
        def _count_helper(node):
            nonlocal count
            if node.is_end_of_word:
                count += 1
            for child_node in node.children.values():
                _count_helper(child_node)
        
        _count_helper(self.root)
        return count
    
if __name__ == "__main__":
    # Initialize a trie
    trie = Trie()
    
    # Insert words
    words = ["apple", "app", "application", "banana", "ball", "bat", "batman"]
    for word in words:
        trie.insert(word)
    
    # Search for words
    print("Search results:")
    print("apple:", trie.search("apple"))      # True
    print("app:", trie.search("app"))          # True
    print("appl:", trie.search("appl"))        # False (not a complete word)
    print("orange:", trie.search("orange"))    # False
    
    # Prefix search
    print("\nPrefix search:")
    print("app:", trie.starts_with("app"))     # True
    print("ban:", trie.starts_with("ban"))     # True
    print("cat:", trie.starts_with("cat"))     # False
    
    # Autocomplete
    print("\nAutocomplete suggestions:")
    print("app:", trie.autocomplete("app"))    # ['app', 'apple', 'application']
    print("ba:", trie.autocomplete("ba"))      # ['ball', 'banana', 'bat', 'batman']
    print("bat:", trie.autocomplete("bat"))    # ['bat', 'batman']
    
    # Get all words
    print("\nAll words in trie:")
    print(trie.get_all_words())  # ['app', 'apple', 'application', 'ball', 'banana', 'bat', 'batman']
    
    # Count words
    print("\nWord count:", trie.count_words())  # 7
    
    # Delete words
    print("\nDeleting 'app' and 'batman':")
    trie.delete("app")
    trie.delete("batman")
    
    print("All words after deletion:")
    print(trie.get_all_words())  # ['apple', 'application', 'ball', 'banana', 'bat']
    
    print("Word count after deletion:", trie.count_words())  # 5