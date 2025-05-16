

def merge_sort(arr):
    """
    Key Characteristics
    Divide and Conquer: Merge sort divides the input array into two halves, recursively sorts them, and then merges the sorted halves.
    Stable Sort: Maintains the relative order of equal elements.
    
    Time Complexity:
    Worst case: O(n log n)
    Best case: O(n log n)
    Average case: O(n log n)
    Space Complexity: O(n) for the auxiliary space used in merging

    Sorts a list in ascending order using the top-down merge sort algorithm.
    
    Args:
        arr (list): The list to be sorted
        
    Returns:
        list: A new sorted list (does not modify the original)
    """
    # Base case: if the list has 0 or 1 elements, it's already sorted
    if len(arr) <= 1:
        return arr.copy()  # Return a copy to maintain consistency
    
    # Divide the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)
    
    # Merge the sorted halves
    return merge(left_sorted, right_sorted)

def merge(left, right):
    """
    Merges two sorted lists into one sorted list.
    
    Args:
        left (list): First sorted list
        right (list): Second sorted list
        
    Returns:
        list: Merged sorted list
    """
    result = []
    i = j = 0  # Pointers for left and right lists
    
    # Traverse both lists and compare elements
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Append any remaining elements from left or right
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def merge_sort_in_place(arr, start=0, end=None):
    """In-place merge sort implementation (modifies original array)"""
    if end is None:
        end = len(arr)
    if end - start > 1:
        mid = (start + end) // 2
        merge_sort_in_place(arr, start, mid)
        merge_sort_in_place(arr, mid, end)
        merge_in_place(arr, start, mid, end)

def merge_in_place(arr, start, mid, end):
    """In-place merge implementation"""
    left = arr[start:mid]
    right = arr[mid:end]
    i = j = 0
    k = start
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

numbers = [38, 27, 43, 3, 9, 82, 10]
sorted_numbers = merge_sort(numbers)
print("Original:", numbers)
print("Sorted:", sorted_numbers)
# Output:
# Original: [38, 27, 43, 3, 9, 82, 10]
# Sorted: [3, 9, 10, 27, 38, 43, 82]

words = ["banana", "apple", "pear", "orange", "grape"]
sorted_words = merge_sort(words)
print("Original:", words)
print("Sorted:", sorted_words)
# Output:
# Original: ['banana', 'apple', 'pear', 'orange', 'grape']
# Sorted: ['apple', 'banana', 'grape', 'orange', 'pear']

data = [5, 2, 8, 2, 5, 1, 3, 1]
sorted_data = merge_sort(data)
print("Original:", data)
print("Sorted:", sorted_data)
# Output:
# Original: [5, 2, 8, 2, 5, 1, 3, 1]
# Sorted: [1, 1, 2, 2, 3, 5, 5, 8]

