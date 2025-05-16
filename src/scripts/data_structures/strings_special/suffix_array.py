


"""
A Suffix Array is a data structure that provides an efficient way to 
handle string pattern matching, substring queries, and other string-related operations. 
It is an array of all suffixes of a string sorted in lexicographical order.
"""

# naive implementation
def build_suffix_array(s):
    """
    Build suffix array for string s using a naive approach.
    """
    suffixes = [(s[i:], i) for i in range(len(s))]
    suffixes.sort(key=lambda x: x[0])
    sa = [idx for (suf, idx) in suffixes]
    return sa

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


# Example string
text = "banana"

# Naive suffix array
sa_naive = build_suffix_array(text)
print("Naive Suffix Array:", sa_naive)

# Efficient suffix array
sa_efficient = build_suffix_array_efficient(text)
print("Efficient Suffix Array:", sa_efficient)

# Output:
# Naive Suffix Array: [5, 3, 1, 0, 4, 2]
# Efficient Suffix Array: [5, 3, 1, 0, 4, 2]


##################################################################

def pattern_search(s, sa, pattern):
    """
    Search for pattern in string s using suffix array sa.
    Returns list of starting indices where pattern occurs.
    """
    n = len(s)
    left, right = 0, n - 1
    result = []

    # Find lower bound
    while left <= right:
        mid = (left + right) // 2
        start = sa[mid]
        suffix = s[start:]
        if suffix.startswith(pattern):
            # Expand to find all matches
            l = mid
            while l >= 0 and s[sa[l]:].startswith(pattern):
                result.append(sa[l])
                l -= 1
            r = mid + 1
            while r < n and s[sa[r]:].startswith(pattern):
                result.append(sa[r])
                r += 1
            break
        elif suffix < pattern:
            left = mid + 1
        else:
            right = mid - 1
    return sorted(result)

# Example pattern search
pattern = "ana"
matches = pattern_search(text, sa_efficient, pattern)
print(f"Pattern '{pattern}' found at positions: {matches}")

# Output:
# Pattern 'ana' found at positions: [1, 3]
