
"""

Translation (Java --> Python) of ALGORITHM 5.9 Regular expression pattern matching (grep) (p.802) from Sedgewick's book "Algorithms in Java" (4th edition)

Key improvements in the Python version:
More concise syntax without type declarations
Using list/set comprehensions where appropriate
More Pythonic naming conventions
Simplified stack operations using Python lists
More readable string operations with in operator
Better iteration patterns (e.g., for char in text)

The implementation maintains the same algorithm but presents it in a more Pythonic way. 
The helper classes (Digraph and DirectedDFS) are simplified versions that provide the minimum functionality needed for the NFA to work.
"""


class Digraph:
    def __init__(self, V):
        self._V = V  # Changed to _V to avoid conflict
        self.adj = [[] for _ in range(V)]
    
    def add_edge(self, v, w):
        self.adj[v].append(w)
    
    def V(self):
        return self._V  # Now consistently using method


class DirectedDFS:
    def __init__(self, G, sources):
        self._marked = [False] * G.V()  # Call V() as method
        for s in sources:
            if not self._marked[s]:
                self._dfs(G, s)
    
    def _dfs(self, G, v):
        self._marked[v] = True
        for w in G.adj[v]:
            if not self._marked[w]:
                self._dfs(G, w)
    
    def marked(self, v):
        return self._marked[v]


class NFA:
    def __init__(self, regexp):
        """Create the NFA for the given regular expression."""
        self.re = list(regexp)
        self.M = len(self.re)
        self.G = Digraph(self.M + 1)  # epsilon transitions
        ops = []
        
        for i in range(self.M):
            lp = i
            if self.re[i] in ('(', '|'):
                ops.append(i)
            elif self.re[i] == ')':
                or_op = ops.pop()
                if self.re[or_op] == '|':
                    lp = ops.pop()
                    self.G.add_edge(lp, or_op + 1)
                    self.G.add_edge(or_op, i)
                else:
                    lp = or_op
            
            # Lookahead for closure operator *
            if i < self.M - 1 and self.re[i + 1] == '*':
                self.G.add_edge(lp, i + 1)
                self.G.add_edge(i + 1, lp)
            
            if self.re[i] in ('(', '*', ')'):
                self.G.add_edge(i, i + 1)
    
    def recognizes(self, text):
        """Does the NFA recognize the text?"""
        # Initialize states reachable from start via epsilon transitions
        pc = set()
        dfs = DirectedDFS(self.G, [0])
        for v in range(self.G.V()):  # Call V() as method
            if dfs.marked(v):
                pc.add(v)
        
        for char in text:
            # Compute states reachable after consuming the character
            matches = set()
            for v in pc:
                if v < self.M:
                    if self.re[v] == char or self.re[v] == '.':
                        matches.add(v + 1)
            
            # Follow epsilon transitions
            pc = set()
            dfs = DirectedDFS(self.G, matches)
            for v in range(self.G.V()):  # Call V() as method
                if dfs.marked(v):
                    pc.add(v)
        
        # Accept if any state is in the accept state
        return any(v == self.M for v in pc)


# Test cases
if __name__ == "__main__":
    # Example 1: Simple pattern matching
    nfa = NFA("((A*B|AC)D)")
    print(nfa.recognizes("AABD"))    # True
    print(nfa.recognizes("ACD"))     # True
    print(nfa.recognizes("BD"))      # True
    print(nfa.recognizes("ABCD"))    # False

    # Example 2: Wildcard matching
    nfa = NFA(".*STAR.*")
    print(nfa.recognizes("STAR"))        # True
    print(nfa.recognizes("MYSTAR"))      # True
    print(nfa.recognizes("STARLIGHT"))   # True
    print(nfa.recognizes("STAR123"))     # True
    print(nfa.recognizes("NO-MATCH"))    # False

    # Example 3: Complex pattern
    nfa = NFA("(a|b)*c")
    print(nfa.recognizes("aabac"))       # True
    print(nfa.recognizes("bbbbc"))       # True
    print(nfa.recognizes("c"))           # True
    print(nfa.recognizes("aabaa"))       # False