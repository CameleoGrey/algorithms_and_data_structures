


def boyer_moore_search(text, pattern):
    """
    Perform Boyer-Moore substring search using the bad character heuristic.
    
    Key Features of this Implementation:
    Bad Character Heuristic: Uses the rightmost occurrence of each character in the pattern to determine shifts
    Efficient Skipping: Often skips large portions of text, especially with large alphabets
    Time Complexity: O(n/m) in best case, O(nm) in worst case (but typically sub-linear in practice)
    Space Complexity: O(k) where k is the alphabet size

    When to Use Boyer-Moore:
    When searching through very large texts
    With patterns that are relatively long
    When the alphabet is large (English text, DNA sequences, etc.)
    When you can afford O(k) space for the shift tables
    When average-case performance is more important than worst-case

    The Boyer-Moore algorithm is often faster in practice than other linear-time string matching algorithms 
    because it can skip large portions of the text when mismatches occur. The bad character heuristic works 
    particularly well when the text contains characters that don't appear in the pattern.

    Args:
        text: The text to search within (string)
        pattern: The pattern to search for (string)
    
    Returns:
        The index of the first occurrence of pattern in text, or -1 if not found
    """
    def build_bad_char_table(pat):
        """Build the bad character shift table."""
        table = {}
        for i in range(len(pat)):
            table[pat[i]] = i
        return table
    
    # Edge cases
    if not pattern:
        return 0
    if len(pattern) > len(text):
        return -1
    
    bad_char = build_bad_char_table(pattern)
    m = len(pattern)
    n = len(text)
    s = 0  # shift of the pattern with respect to text
    
    while s <= n - m:
        j = m - 1
        
        # Keep reducing index j while characters match
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            return s  # Pattern found at shift s
        else:
            # Shift pattern using bad character rule
            char = text[s + j]
            shift = j - bad_char.get(char, -1)
            s += max(1, shift)
    
    return -1  # Pattern not found

# Example Usage
if __name__ == "__main__":
    # Example 1: Simple search
    text1 = "ABAAABCDBBABCDDEBCABC"
    pattern1 = "ABC"
    index1 = boyer_moore_search(text1, pattern1)
    print(f"Text: {text1}")
    print(f"Pattern: {pattern1}")
    print(f"Found at index: {index1}")
    if index1 != -1:
        print(f"Matched substring: {text1[index1:index1+len(pattern1)]}")
    else:
        print("Pattern not found")
    
    # Example 2: Pattern not found
    text2 = "This is a test string for Boyer-Moore algorithm"
    pattern2 = "testing"
    index2 = boyer_moore_search(text2, pattern2)
    print(f"\nText: {text2}")
    print(f"Pattern: {pattern2}")
    print(f"Found at index: {index2}")
    
    # Example 3: Multiple occurrences (finds first one)
    text3 = "GCATCGCAGAGAGTATACAGTACG"
    pattern3 = "GCAGAGAG"
    index3 = boyer_moore_search(text3, pattern3)
    print(f"\nText: {text3}")
    print(f"Pattern: {pattern3}")
    print(f"Found at index: {index3}")
    if index3 != -1:
        print(f"Matched substring: {text3[index3:index3+len(pattern3)]}")
    
    # Example 4: Empty pattern
    text4 = "Sample text for empty pattern test"
    pattern4 = ""
    index4 = boyer_moore_search(text4, pattern4)
    print(f"\nText: {text4}")
    print(f"Pattern: '{pattern4}'")
    print(f"Found at index: {index4}")