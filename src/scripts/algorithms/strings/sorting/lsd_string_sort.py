def lsd_sort(strings, width=None):
    """

    LSD (Least Significant Digit) radix sort is an efficient algorithm for sorting fixed-length strings. 
    It works by processing characters from right to left, performing stable counting sorts at each character position.
    
    Sorts an array of fixed-length strings using LSD radix sort.
    
    Args:
        strings: List of strings to be sorted
        width: Fixed length of strings (optional, will use max length if not provided)
    
    Returns:
        Sorted list of strings
    """
    if not strings:
        return []
    
    # Determine width if not provided
    if width is None:
        width = max(len(s) for s in strings)
    
    # Pad strings with spaces to make them all the same length
    padded_strings = [s.ljust(width) for s in strings]
    
    # Sort from least significant character to most significant
    for i in range(width-1, -1, -1):
        # Perform counting sort on the i-th character
        # ASCII range from 0 (null) to 127 (DEL)
        R = 128  # Number of possible ASCII characters
        count = [0] * (R + 1)
        
        # Count frequencies of each character
        for s in padded_strings:
            char = s[i]
            count[ord(char) + 1] += 1
        
        # Compute cumulates
        for r in range(R):
            count[r + 1] += count[r]
        
        # Distribute the strings
        aux = [None] * len(padded_strings)
        for s in padded_strings:
            char = s[i]
            aux[count[ord(char)]] = s
            count[ord(char)] += 1
        
        # Copy back
        padded_strings = aux
    
    # Remove padding before returning
    return [s.strip() for s in padded_strings]


## Example Usage
if __name__ == "__main__":
    # Example with fixed-width strings
    fixed_width_strings = [
        "ABC",
        "XYZ",
        "ABD",
        "AAA",
        "XAA",
        "BBC"
    ]
    
    print("Original strings:", fixed_width_strings)
    sorted_strings = lsd_sort(fixed_width_strings)
    print("Sorted strings:", sorted_strings)
    
    # Example with variable-length strings (will be padded)
    variable_length_strings = [
        "banana",
        "apple",
        "orange",
        "grape",
        "kiwi",
        "pear"
    ]
    
    print("\nOriginal strings:", variable_length_strings)
    sorted_variable = lsd_sort(variable_length_strings)
    print("Sorted strings:", sorted_variable)
    
    # Example with numbers as strings
    number_strings = [
        "123",
        "001",
        "345",
        "100",
        "999"
    ]
    
    print("\nOriginal number strings:", number_strings)
    sorted_numbers = lsd_sort(number_strings)
    print("Sorted number strings:", sorted_numbers)