def kmp_search(text, pattern):
    """

    The KMP algorithm improves upon brute-force search by using information about the pattern to skip 
    unnecessary comparisons. It preprocesses the pattern to create a "partial match" 
    table (also called failure function) that helps optimize the search process.

    Perform Knuth-Morris-Pratt substring search to find pattern in text.

    Key Features
    Efficiency: Time complexity O(n+m) where n is text length and m is pattern length
    LPS Array: Uses longest prefix suffix array to skip unnecessary comparisons
    Optimal: Never backs up in the text (unlike brute-force)
    Space Complexity: O(m) for storing the LPS array

    How KMP Works
    Preprocessing: Builds the LPS array for the pattern
    LPS[i] = length of the longest proper prefix of pat[0..i] which is also a suffix
    Searching:
    Compare pattern with text character by character
    On mismatch, use LPS array to determine how many characters to skip
    Never re-compare characters that matched before

    When to Use KMP
    When searching for the same pattern in multiple texts
    With patterns that contain many repeating subpatterns
    When worst-case performance is important
    When text is very large and efficiency matters

    The KMP algorithm is particularly effective when the pattern contains many repeating subpatterns, 
    as the LPS array helps skip large portions of the text after a mismatch.
    
    Args:
        text: The text to search within (string)
        pattern: The pattern to search for (string)
    
    Returns:
        The index of the first occurrence of pattern in text, or -1 if not found
    """
    def build_lps_array(pat):
        """Build the longest prefix suffix (LPS) array for the pattern."""
        lps = [0] * len(pat)
        length = 0
        i = 1
        
        while i < len(pat):
            if pat[i] == pat[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    # Edge cases
    if not pattern:
        return 0
    if len(pattern) > len(text):
        return -1
    
    lps = build_lps_array(pattern)
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
            if j == len(pattern):
                return i - j  # Pattern found
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return -1  # Pattern not found


## Example Usage
if __name__ == "__main__":
    # Example 1: Simple search
    text1 = "ABABDABACDABABCABAB"
    pattern1 = "ABABCABAB"
    index1 = kmp_search(text1, pattern1)
    print(f"Text: {text1}")
    print(f"Pattern: {pattern1}")
    print(f"Found at index: {index1}")
    print(f"Matched substring: {text1[index1:index1+len(pattern1)] if index1 != -1 else 'Not found'}")
    
    # Example 2: Pattern not found
    text2 = "This is a sample text for testing KMP algorithm"
    pattern2 = "testingxyz"
    index2 = kmp_search(text2, pattern2)
    print(f"\nText: {text2}")
    print(f"Pattern: {pattern2}")
    print(f"Found at index: {index2}")
    
    # Example 3: Multiple occurrences (finds first one)
    text3 = "AAACAAAAACAAACAAAA"
    pattern3 = "AAACAAAA"
    index3 = kmp_search(text3, pattern3)
    print(f"\nText: {text3}")
    print(f"Pattern: {pattern3}")
    print(f"Found at index: {index3}")
    print(f"Matched substring: {text3[index3:index3+len(pattern3)] if index3 != -1 else 'Not found'}")
    
    # Example 4: Empty pattern
    text4 = "Any text"
    pattern4 = ""
    index4 = kmp_search(text4, pattern4)
    print(f"\nText: {text4}")
    print(f"Pattern: '{pattern4}'")
    print(f"Found at index: {index4}")