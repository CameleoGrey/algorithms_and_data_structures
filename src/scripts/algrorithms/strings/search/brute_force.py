def brute_force_search(text, pattern):
    """

    The brute-force substring search algorithm is the simplest method for 
    finding a pattern within a text. It checks all possible positions in the text where the pattern could match.

    Key Features
    Simple Implementation: Easy to understand and implement
    No Preprocessing: Doesn't require any preprocessing of the text or pattern
    Worst-case Time Complexity: O(nm) where n is text length and m is pattern length
    Best-case Time Complexity: O(n) when pattern not found or found at beginning
    Space Complexity: O(1) - uses constant extra space

    When to Use Brute-Force Search
    When implementing substring search for the first time
    For short texts or patterns
    When simplicity is more important than speed
    As a baseline for comparing more advanced algorithms
    When patterns are unlikely to have many partial matches

    Alternative Algorithms
    For better performance with longer texts/patterns:
    Knuth-Morris-Pratt (KMP) algorithm
    Boyer-Moore algorithm
    Rabin-Karp algorithm
    The brute-force method serves as a fundamental building block for understanding more complex string search algorithms.
    
    Args:
        text: The text to search within (string)
        pattern: The pattern to search for (string)
    
    Returns:
        The index of the first occurrence of pattern in text, or -1 if not found
    """
    n = len(text)
    m = len(pattern)
    
    # Handle empty pattern case
    if m == 0:
        return 0
    
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i  # Pattern found starting at index i
    
    return -1  # Pattern not found


## Example Usage
if __name__ == "__main__":
    # Example 1: Simple search
    text1 = "ABACADABRAC"
    pattern1 = "ABRA"
    index1 = brute_force_search(text1, pattern1)
    print(f"Text: {text1}")
    print(f"Pattern: {pattern1}")
    print(f"Found at index: {index1}")
    print(f"Matched substring: {text1[index1:index1+len(pattern1)] if index1 != -1 else 'Not found'}")
    
    # Example 2: Pattern not found
    text2 = "This is a sample text for testing"
    pattern2 = "example"
    index2 = brute_force_search(text2, pattern2)
    print(f"\nText: {text2}")
    print(f"Pattern: {pattern2}")
    print(f"Found at index: {index2}")
    
    # Example 3: Multiple occurrences (finds first one)
    text3 = "The quick brown fox jumps over the lazy dog"
    pattern3 = "the"
    index3 = brute_force_search(text3, pattern3)
    print(f"\nText: {text3}")
    print(f"Pattern: {pattern3}")
    print(f"Found at index: {index3}")
    print(f"Matched substring: {text3[index3:index3+len(pattern3)] if index3 != -1 else 'Not found'}")
    
    # Example 4: Empty pattern
    text4 = "Any text"
    pattern4 = ""
    index4 = brute_force_search(text4, pattern4)
    print(f"\nText: {text4}")
    print(f"Pattern: '{pattern4}'")
    print(f"Found at index: {index4}")