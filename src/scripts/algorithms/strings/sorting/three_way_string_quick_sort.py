


def three_way_string_quicksort(strings):
    """

    Three-way string quicksort is a hybrid of quicksort and radix sort that is particularly 
    efficient for sorting strings. It handles common prefixes efficiently and works well with strings that have long shared prefixes.

    Key features:
    Three-way Partitioning: Divides strings into three groups based on the current character
    Recursive Processing: Handles each partition recursively
    Variable-Length Support: Naturally handles strings of different lengths
    Prefix Optimization: Efficient with strings that share common prefixes
    In-Place Sorting: Requires only logarithmic extra space (for recursion)

    Performance Characteristics
    Time Complexity: O(wn) to O(wn log n) where w is average string length
    Space Complexity: O(log n) for recursion stack
    Adaptive: Performs better on partially sorted data
    Cache Friendly: Good locality of reference

    When to Use Three-Way String Quicksort
    Sorting large collections of strings
    When strings share common prefixes
    When memory usage is a concern
    For general-purpose string sorting
    When you need an in-place sorting algorithm
    
    Args:
        strings: List of strings to be sorted
    
    Returns:
        Sorted list of strings
    """
    def _sort(strings, low, high, d):
        if high <= low:
            return
        
        # Partition
        lt = low
        gt = high
        pivot = char_at(strings[low], d)
        i = low + 1
        
        while i <= gt:
            t = char_at(strings[i], d)
            if t < pivot:
                strings[lt], strings[i] = strings[i], strings[lt]
                lt += 1
                i += 1
            elif t > pivot:
                strings[i], strings[gt] = strings[gt], strings[i]
                gt -= 1
            else:
                i += 1
        
        # Recursively sort three partitions
        _sort(strings, low, lt-1, d)
        if pivot >= 0:
            _sort(strings, lt, gt, d+1)
        _sort(strings, gt+1, high, d)
    
    def char_at(s, d):
        return ord(s[d]) if d < len(s) else -1
    
    # Make a copy to avoid modifying the original list
    strings = list(strings)
    _sort(strings, 0, len(strings)-1, 0)
    return strings


if __name__ == "__main__":
    # Example 1: Simple strings
    strings1 = [
        "she", "sells", "seashells", "by", "the", "sea", 
        "shore", "the", "shells", "she", "sells", "are", 
        "surely", "seashells"
    ]
    print("Original strings:")
    print(strings1)
    sorted1 = three_way_string_quicksort(strings1)
    print("\nSorted strings:")
    print(sorted1)
    
    # Example 2: Strings with common prefixes
    strings2 = [
        "apple", "application", "appetizer", "banana", 
        "band", "bandana", "carrot", "carpet"
    ]
    print("\nOriginal strings with common prefixes:")
    print(strings2)
    sorted2 = three_way_string_quicksort(strings2)
    print("\nSorted strings:")
    print(sorted2)
    
    # Example 3: Mixed case strings
    strings3 = [
        "Apple", "apple", "Banana", "banana", 
        "Carrot", "carrot", "applepie"
    ]
    print("\nOriginal mixed case strings:")
    print(strings3)
    sorted3 = three_way_string_quicksort(strings3)
    print("\nSorted strings:")
    print(sorted3)