def msd_sort(strings):
    """

    MSD (Most Significant Digit) radix sort is an efficient algorithm for sorting variable-length strings. 
    Unlike LSD sort which processes characters from right to left, MSD sort processes characters from left to 
    right and can handle variable-length strings more naturally.

    Sorts an array of strings using MSD radix sort.

    Comparison with LSD Sort
    Direction: MSD processes left-to-right, LSD right-to-left
    Length Handling: MSD better for variable-length strings
    Performance: MSD can be faster for strings with early distinct characters
    Memory: MSD uses more memory due to recursive calls
    Implementation: MSD is more complex to implement

    When to Use MSD Sort
    Sorting variable-length strings
    Cases where strings differ in early characters
    When you need natural sorting order
    Situations where many strings share long prefixes
    
    Args:
        strings: List of strings to be sorted
    
    Returns:
        Sorted list of strings
    """
    if len(strings) <= 1:
        return strings
    
    # Find the maximum length of strings
    max_len = max(len(s) for s in strings) if strings else 0
    
    # Recursive helper function
    def _msd_sort(strings, position):
        if len(strings) <= 1 or position >= max_len:
            return strings
        
        # ASCII range from 0 (null) to 127 (DEL)
        R = 128  # Number of possible ASCII characters
        count = [0] * (R + 2)  # +2 for empty character and cumulative counts
        
        # Count frequencies of each character at current position
        for s in strings:
            c = ord(s[position]) if position < len(s) else -1
            count[c + 2] += 1
        
        # Compute cumulates
        for r in range(R + 1):
            count[r + 1] += count[r]
        
        # Distribute the strings
        aux = [None] * len(strings)
        for s in strings:
            c = ord(s[position]) if position < len(s) else -1
            aux[count[c + 1]] = s
            count[c + 1] += 1
        
        # Copy back
        strings = aux
        
        # Recursively sort each subarray
        start = 0
        for r in range(R + 1):
            end = count[r]
            if start < end:
                strings[start:end] = _msd_sort(strings[start:end], position + 1)
            start = end
        
        return strings
    
    return _msd_sort(strings, 0)

if __name__ == "__main__":
    # Example with variable-length strings
    strings = [
        "she",
        "sells",
        "seashells",
        "by",
        "the",
        "sea",
        "shore",
        "the",
        "shells",
        "she",
        "sells",
        "are",
        "surely",
        "seashells"
    ]
    
    print("Original strings:")
    print(strings)
    
    sorted_strings = msd_sort(strings)
    print("\nSorted strings:")
    print(sorted_strings)
    
    # Example with mixed case strings
    mixed_case = [
        "Apple",
        "apple",
        "Banana",
        "banana",
        "Carrot",
        "carrot"
    ]
    
    print("\nOriginal mixed case strings:")
    print(mixed_case)
    
    sorted_mixed = msd_sort(mixed_case)
    print("\nSorted mixed case strings:")
    print(sorted_mixed)
    
    # Example with numbers as strings
    numbers = [
        "100",
        "1",
        "10",
        "1000",
        "2",
        "20",
        "200"
    ]
    
    print("\nOriginal number strings:")
    print(numbers)
    
    sorted_numbers = msd_sort(numbers)
    print("\nSorted number strings:")
    print(sorted_numbers)