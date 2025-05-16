
"""
The Aho-Corasick algorithm is a powerful string-searching algorithm that efficiently locates all 
occurrences of multiple patterns in a text simultaneously. It's particularly useful for tasks like 
keyword spotting, virus signature detection, and DNA sequence analysis.

Key Features
Efficient Multi-Pattern Search: Finds all patterns in O(n + m + z) time where:
n = text length
m = total pattern lengths
z = number of matches
Trie Structure: Builds a finite state machine from the patterns
Failure Links: Allows the algorithm to continue searching after mismatches
Output Links: Collects all patterns that end at each node

When to Use Aho-Corasick
Searching for multiple patterns simultaneously
When patterns share common prefixes
In virus signature detection systems
For DNA/RNA sequence analysis
In network intrusion detection systems
For keyword spotting in large texts

The algorithm is particularly efficient when you need to search for many patterns in large texts, 
as it processes the text in a single pass while simultaneously checking for all patterns.
"""


from collections import deque

class AhoCorasickNode:
    __slots__ = ['transitions', 'output', 'fail']

    def __init__(self):
        self.transitions = {}  # Character to child node mapping
        self.output = set()    # Patterns that end at this node
        self.fail = None       # Failure link

class AhoCorasick:
    def __init__(self, patterns=None):
        self.root = AhoCorasickNode()
        if patterns:
            self.build_trie(patterns)
            self.build_failure_links()

    def build_trie(self, patterns):
        """Build the initial trie from patterns."""
        for pattern in patterns:
            node = self.root
            for char in pattern:
                if char not in node.transitions:
                    node.transitions[char] = AhoCorasickNode()
                node = node.transitions[char]
            node.output.add(pattern)

    def build_failure_links(self):
        """Build failure links using BFS."""
        queue = deque()
        
        # First level nodes fail to root
        for node in self.root.transitions.values():
            node.fail = self.root
            queue.append(node)

        # Process remaining nodes
        while queue:
            current_node = queue.popleft()

            for char, child_node in current_node.transitions.items():
                queue.append(child_node)
                fail_node = current_node.fail

                while fail_node is not None and char not in fail_node.transitions:
                    fail_node = fail_node.fail

                child_node.fail = fail_node.transitions[char] if fail_node else self.root
                child_node.output.update(child_node.fail.output)

    def search(self, text):
        """Search for all patterns in the text."""
        current_node = self.root
        results = []

        for i, char in enumerate(text):
            # Follow failure links until we find a matching transition
            while current_node is not None and char not in current_node.transitions:
                current_node = current_node.fail

            if current_node is None:
                current_node = self.root
                continue

            current_node = current_node.transitions[char]

            for pattern in current_node.output:
                results.append((i - len(pattern) + 1, pattern))

        return results

if __name__ == "__main__":
    # Example 1: Basic usage
    patterns = ["he", "she", "his", "hers"]
    text = "ushers"
    print(f"Patterns: {patterns}")
    print(f"Text: {text}")
    
    ac = AhoCorasick(patterns)
    matches = ac.search(text)
    print("\nMatches found:")
    for pos, pattern in matches:
        print(f"'{pattern}' at position {pos}")

    # Example 2: Multiple matches
    patterns2 = ["apple", "app", "banana", "ana"]
    text2 = "bananaappleorange"
    print(f"\nPatterns: {patterns2}")
    print(f"Text: {text2}")
    
    ac2 = AhoCorasick(patterns2)
    matches2 = ac2.search(text2)
    print("\nMatches found:")
    for pos, pattern in matches2:
        print(f"'{pattern}' at position {pos}")

    # Example 3: No matches
    patterns3 = ["cat", "dog"]
    text3 = "The quick brown fox jumps"
    print(f"\nPatterns: {patterns3}")
    print(f"Text: {text3}")
    
    ac3 = AhoCorasick(patterns3)
    matches3 = ac3.search(text3)
    print("\nMatches found:", matches3)

    # Example 4: DNA sequence search
    dna_patterns = ["GATTACA", "TATA", "ACGT"]
    dna_sequence = "ATCGGATTACATATACGT"
    print(f"\nDNA Patterns: {dna_patterns}")
    print(f"DNA Sequence: {dna_sequence}")
    
    dna_searcher = AhoCorasick(dna_patterns)
    dna_matches = dna_searcher.search(dna_sequence)
    print("\nDNA Matches found:")
    for pos, pattern in dna_matches:
        print(f"'{pattern}' at position {pos}")