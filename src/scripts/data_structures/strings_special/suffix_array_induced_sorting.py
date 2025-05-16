

"""
Certainly! Implementing the SA-IS (Suffix Array Induced Sorting) algorithm is quite involved, 
but it's one of the most efficient algorithms for suffix array construction, running in linear time $O(n)$.
Below is a Python implementation of the SA-IS algorithm for constructing suffix arrays. 
This implementation is suitable for strings with a limited alphabet (e.g., ASCII). For larger alphabets, some modifications might be necessary.
"""

def build_suffix_array_efficient(s):
    """
    Build suffix array for string s using prefix doubling algorithm.
    """
    n = len(s)
    k = 1
    rank = [ord(c) for c in s]
    sa = list(range(n))
    temp = [0] * n

    while True:
        # Key for sorting: (rank[i], rank[i + k]) if i + k < n else -1
        sa.sort(key=lambda x: (rank[x], rank[x + k] if x + k < n else -1))
        temp[sa[0]] = 0
        for i in range(1, n):
            prev, curr = sa[i - 1], sa[i]
            temp[curr] = temp[prev]
            if (rank[prev], rank[prev + k] if prev + k < n else -1) != \
               (rank[curr], rank[curr + k] if curr + k < n else -1):
                temp[curr] += 1
        rank = temp[:]
        if rank[sa[-1]] == n - 1:
            break
        k <<= 1
    return sa

def sais(s):
    """
    Constructs the suffix array of string s using the SA-IS algorithm.
    """
    def get_buckets(s, alphabet_size, end=True):
        """Compute bucket sizes and boundaries."""
        buckets = [0] * alphabet_size
        for c in s:
            buckets[c] += 1
        sum_ = 0
        if end:
            for i in range(alphabet_size):
                sum_ += buckets[i]
                buckets[i] = sum_
        else:
            for i in range(alphabet_size):
                sum_ += buckets[i]
                buckets[i] = sum_ - buckets[i]
        return buckets

    def induce_sort(s, sa, t, buckets, alphabet_size):
        """Induce the sorting of L-type and S-type suffixes."""
        n = len(s)
        # Induce L-type suffixes
        b = buckets.copy()
        for i in range(n):
            j = sa[i] - 1
            if j >= 0 and t[j]:
                sa[b[s[j]]] = j
                b[s[j]] += 1
        # Induce S-type suffixes
        b = buckets.copy()
        for i in range(n - 1, -1, -1):
            j = sa[i] - 1
            if j >= 0 and not t[j]:
                b[s[j]] -= 1
                sa[b[s[j]]] = j

    def build_sa(s, alphabet_size):
        n = len(s)
        sa = [-1] * n
        if n == 0:
            return sa
        if n == 1:
            sa[0] = 0
            return sa

        # Step 1: Classify suffixes as S-type or L-type
        t = [False] * n
        t[-1] = True  # Sentinel is S-type
        for i in range(n - 2, -1, -1):
            t[i] = s[i] < s[i + 1] or (s[i] == s[i + 1] and t[i + 1])

        # Step 2: Find LMS (Leftmost S-type) positions
        lms_positions = [i for i in range(1, n) if t[i] and not t[i - 1]]

        # Step 3: Initialize buckets
        buckets = get_buckets(s, alphabet_size, end=True)

        # Step 4: Place LMS suffixes into their buckets
        for i in range(n):
            sa[i] = -1
        b = buckets.copy()
        for i in lms_positions:
            b[s[i]] -= 1
            sa[b[s[i]]] = i

        # Step 5: Induce sort L and S suffixes
        induce_sort(s, sa, t, buckets, alphabet_size)

        # Step 6: Reduce problem if LMS substrings are not unique
        lms_substrings = []
        prev = -1
        name = 0
        lms_map = [-1] * n
        for i in sa:
            if i in lms_positions:
                if prev == -1:
                    lms_map[i] = name
                    prev = i
                else:
                    # Check if substrings are equal
                    diff = False
                    for d in range(n):
                        if s[i + d] != s[prev + d] or t[i + d] != t[prev + d]:
                            diff = True
                            break
                        if d > 0 and (i + d in lms_positions or prev + d in lms_positions):
                            break
                    if diff:
                        name += 1
                    lms_map[i] = name
                    prev = i
        # If all LMS substrings are unique, no need to recurse
        if name + 1 == len(lms_positions):
            lms_order = [0] * len(lms_positions)
            for i in range(len(lms_positions)):
                lms_order[lms_map[lms_positions[i]]] = lms_positions[i]
        else:
            # Recurse
            reduced_s = [lms_map[i] for i in lms_positions]
            sa_lms = sais(reduced_s)
            lms_order = [lms_positions[i] for i in sa_lms]

        # Step 7: Final induced sort
        sa = [-1] * n
        b = get_buckets(s, alphabet_size, end=True)
        for i in range(len(lms_order) - 1, -1, -1):
            j = lms_order[i]
            b[s[j]] -= 1
            sa[b[s[j]]] = j
        induce_sort(s, sa, t, buckets, alphabet_size)

        return sa

    # Map characters to integers
    max_char = max(s) if isinstance(s, list) else max(ord(c) for c in s)
    s_int = [ord(c) for c in s] if not isinstance(s, list) else s
    return sais(s_int)

# Usage example
text = "banana"
sa = build_suffix_array_efficient(text)
print("Suffix Array:", sa)
print("Suffixes in order:")
for i in sa:
    print(f"{i}: {text[i:]}")
