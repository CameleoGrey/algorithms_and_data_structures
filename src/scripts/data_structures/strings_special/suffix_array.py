


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

def build_suffix_array_efficient(input_string):
    """
    Builds a suffix array for the given string using the prefix doubling algorithm.
    
    Args:
        input_string: The string for which to build the suffix array
        
    Returns:
        A list representing the suffix array of the input string
    """
    length = len(input_string)
    prefix_length = 1  # Current comparison prefix length (doubles each iteration)
    
    # Initial ranks based on single characters
    ranks = [ord(char) for char in input_string]
    suffix_array = list(range(length))
    new_ranks = [0] * length

    while True:
        # Sort suffixes based on current rank pairs
        suffix_array.sort(key=lambda i: (
            ranks[i], 
            ranks[i + prefix_length] if i + prefix_length < length else -1
        ))
        
        # Assign new ranks based on the sorted order
        new_ranks[suffix_array[0]] = 0
        for i in range(1, length):
            prev_suffix, curr_suffix = suffix_array[i - 1], suffix_array[i]
            
            # Give the same rank to suffixes with identical comparison values
            new_ranks[curr_suffix] = new_ranks[prev_suffix]
            
            # Only increment rank if the current suffix is different from previous
            prev_key = (ranks[prev_suffix], 
                       ranks[prev_suffix + prefix_length] if prev_suffix + prefix_length < length else -1)
            curr_key = (ranks[curr_suffix],
                       ranks[curr_suffix + prefix_length] if curr_suffix + prefix_length < length else -1)
            
            if prev_key != curr_key:
                new_ranks[curr_suffix] += 1
        
        ranks = new_ranks[:]  # Update ranks for next iteration
        
        # If all suffixes have unique ranks, we're done
        if ranks[suffix_array[-1]] == length - 1:
            break
            
        prefix_length *= 2  # Double the comparison prefix length
    
    return suffix_array


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
