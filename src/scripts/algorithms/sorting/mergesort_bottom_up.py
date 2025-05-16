def bottom_up_merge_sort(arr):
    """
    Key Characteristics
    Iterative Approach: Unlike top-down merge sort, this version uses loops instead of recursion
    Same Time Complexity:
    Worst case: O(n log n)
    Best case: O(n log n)
    Average case: O(n log n)
    Space Complexity: O(n) for the auxiliary space used in merging
    Better for Large Datasets: Avoids recursion stack limits for very large arrays

    Comparison with Top-Down Merge Sort
    Performance: Generally similar performance, but bottom-up can be slightly faster in practice due to better cache locality
    Implementation: Bottom-up is purely iterative while top-down is recursive
    Readability: Top-down is often considered more intuitive as it follows the natural divide-and-conquer approach

    Sorts a list in ascending order using the bottom-up merge sort algorithm.
    
    Args:
        arr (list): The list to be sorted
        
    Returns:
        list: A new sorted list (does not modify the original)
    """
    n = len(arr)
    # Create a copy of the array to avoid modifying the original
    arr = arr.copy()
    
    # Start with subarrays of size 1 and double each time
    size = 1
    while size < n:
        # Merge adjacent subarrays
        for start in range(0, n - size, 2 * size):
            mid = start + size
            end = min(start + 2 * size, n)
            merged = merge(arr[start:mid], arr[mid:end])
            # Copy the merged portion back to the original array
            arr[start:end] = merged
        size *= 2
    
    return arr

def merge(left, right):
    """
    Merges two sorted lists into one sorted list.
    (Same helper function as in top-down merge sort)
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def bottom_up_merge_sort_in_place(arr):
    """
    In-place bottom-up merge sort implementation

    Bottom-up merge sort is particularly useful when:
    Working with very large datasets where recursion depth might be a concern
    Implementing in languages where recursion is expensive
    You need a stable, O(n log n) sorting algorithm with predictable performance
        
    """
    n = len(arr)
    size = 1
    
    while size < n:
        for start in range(0, n - size, 2 * size):
            mid = start + size
            end = min(start + 2 * size, n)
            
            # Merge in-place using temporary storage
            left = arr[start:mid]
            right = arr[mid:end]
            merged = merge(left, right)
            arr[start:end] = merged
            
        size *= 2
    
    return arr

numbers = [38, 27, 43, 3, 9, 82, 10]
sorted_numbers = bottom_up_merge_sort_in_place(numbers)
print("Original:", numbers)
print("Sorted:", sorted_numbers)
# Output:
# Original: [38, 27, 43, 3, 9, 82, 10]
# Sorted: [3, 9, 10, 27, 38, 43, 82]

words = ["banana", "apple", "pear", "orange", "grape"]
sorted_words = bottom_up_merge_sort_in_place(words)
print("Original:", words)
print("Sorted:", sorted_words)
# Output:
# Original: ['banana', 'apple', 'pear', 'orange', 'grape']
# Sorted: ['apple', 'banana', 'grape', 'orange', 'pear']

import random
large_data = [random.randint(0, 10000) for _ in range(1000)]
sorted_large = bottom_up_merge_sort_in_place(large_data)
print("First 10 elements:", sorted_large[:10])
# Output will vary, but will show the first 10 sorted elements