



def rabin_karp_search(text, pattern, prime=101):
    """

    The Rabin-Karp algorithm uses hashing (fingerprinting) to find patterns in text. 
    It's particularly effective for multiple pattern searches or when searching for similar patterns.

    Key Features
    Rolling Hash: Efficient hash recomputation in O(1) time per shift
    Prime Modulo: Uses modular arithmetic to keep hash values manageable
    Multiple Matches: Returns all occurrences of the pattern
    Verification Step: Double-checks hash matches to prevent false positives
    Alphabet Size: Configurable for different character sets

    Performance Characteristics
    Average Case: O(n+m) where n is text length and m is pattern length
    Worst Case: O(nm) when hash collisions occur frequently
    Space Complexity: O(1) additional space (excluding result storage)

    When to Use Rabin-Karp
    Searching for multiple patterns simultaneously
    Finding approximate matches (with modified hash comparison)
    When patterns are of similar length
    When you need to detect duplicate substrings
    In plagiarism detection or document similarity checks

    The algorithm is particularly effective when you need to find multiple occurrences of a pattern or 
    when searching for multiple patterns at once (by computing their hashes first). The prime number helps 
    reduce hash collisions, and the rolling hash makes it efficient for long texts.

    ###################
    The provided Rabin-Karp implementation uses the Las Vegas approach, not Monte Carlo. Here's why:

    Key Distinction:
    Las Vegas (this implementation):
    Always verifies potential matches by comparing actual characters when hashes match
    Guarantees 100% correct results (no false positives)
    Has a worst-case O(nm) time complexity when many hash collisions occur

    Monte Carlo (not used here):
    Would skip character verification after hash match
    Accepts some probability of false positives
    Runs in guaranteed O(n+m) time but with possible incorrect results

    Evidence in the Code:
    if p == t:  # Hash match
        # Las Vegas verification step:
        for j in range(m):
            if text[i+j] != pattern[j]:
                break
        else:
            result.append(i)  # Only add if full match confirmed


    Why This Matters:
    Las Vegas is preferred when absolute correctness is required (most common case)
    Monte Carlo might be used in scenarios where:
    Extremely large texts make verification expensive
    Occasional false positives are acceptable
    You can use a second verification pass for potential matches

    Practical Implications:
    Correctness: This implementation will never return false positives
    
    Performance:
    Best-case: O(n+m) when few hash collisions
    Worst-case: O(nm) when many collisions (unlikely with good prime choice)
    Real-world Use: Most production implementations use Las Vegas for reliability

    To convert this to Monte Carlo, you would:
    Remove the character-by-character verification
    Accept that some returned matches might be incorrect
    Use a larger prime/modulo to reduce collision probability
    The current implementation is the more conservative and widely-used approach.  
    ###################

    Perform Rabin-Karp substring search using rolling hash.
    
    Args:
        text: The text to search within (string)
        pattern: The pattern to search for (string)
        prime: A prime number for hash calculation
        
    Returns:
        List of starting indices where pattern is found
    """
    d = 256  # Number of characters in the input alphabet
    m = len(pattern)
    n = len(text)
    h = pow(d, m-1, prime)  # d^(m-1) % prime
    p = 0  # hash value for pattern
    t = 0  # hash value for current text window
    result = []

    if m == 0 or n < m:
        return result

    # Calculate initial hash values
    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        t = (d * t + ord(text[i])) % prime

    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        # Check hash values first
        if p == t:
            # If hash matches, verify characters one by one
            for j in range(m):
                if text[i+j] != pattern[j]:
                    break
            else:
                result.append(i)  # Pattern found at index i

        # Calculate hash for next window
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i+m])) % prime
            t = t if t >= 0 else t + prime  # Ensure positive hash

    return result

if __name__ == "__main__":
    # Example 1: Simple search
    text1 = "ABCCDDAEFGCCDDHIJKLMNOPCCDDQRS"
    pattern1 = "CCDD"
    matches1 = rabin_karp_search(text1, pattern1)
    print(f"Text: {text1}")
    print(f"Pattern: {pattern1}")
    print(f"Found at indices: {matches1}")
    for idx in matches1:
        print(f"Match at {idx}: {text1[idx:idx+len(pattern1)]}")

    # Example 2: No matches
    text2 = "This is a test string for Rabin-Karp algorithm"
    pattern2 = "xyz123"
    matches2 = rabin_karp_search(text2, pattern2)
    print(f"\nText: {text2}")
    print(f"Pattern: {pattern2}")
    print(f"Found at indices: {matches2}")

    # Example 3: Multiple patterns
    text3 = "AABAACAADAABAABA"
    pattern3 = "AABA"
    matches3 = rabin_karp_search(text3, pattern3)
    print(f"\nText: {text3}")
    print(f"Pattern: {pattern3}")
    print(f"Found at indices: {matches3}")
    for idx in matches3:
        print(f"Match at {idx}: {text3[idx:idx+len(pattern3)]}")

    # Example 4: Empty pattern
    text4 = "Sample text for empty pattern test"
    pattern4 = ""
    matches4 = rabin_karp_search(text4, pattern4)
    print(f"\nText: {text4}")
    print(f"Pattern: '{pattern4}'")
    print(f"Found at indices: {matches4}")