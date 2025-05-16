



def quick_sort(arr):
    """
    Key Characteristics
    Divide and Conquer: Like merge sort, but partitions the array first
    Time Complexity:
    Worst case: O(n²) (when poor pivot choices are made)
    Best case: O(n log n)
    Average case: O(n log n)
    Space Complexity: O(log n) for the recursion stack (in-place version)
    Unstable Sort: May change the relative order of equal elements

    Quick sort is generally faster than merge sort for small to medium datasets due to 
    better cache performance and lower constant factors, though merge sort has more predictable performance.

    Optimizations
    Pivot Selection:
    Median-of-three: Choose median of first, middle, and last elements
    Random pivot: Helps avoid worst-case scenarios
    Sorts a list in ascending order using the quick sort algorithm.
    
    Args:
        arr (list): The list to be sorted
        
    Returns:
        list: A new sorted list (does not modify the original)
    """
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr.copy()
    
    # Choose pivot (here we use the last element)
    pivot = arr[-1]
    
    # Partition the array into elements less than, equal to, and greater than pivot
    less = [x for x in arr[:-1] if x <= pivot]
    greater = [x for x in arr[:-1] if x > pivot]
    
    # Recursively sort the partitions and combine with pivot
    return quick_sort(less) + [pivot] + quick_sort(greater)


def quick_sort_in_place(arr, low=0, high=None):
    """
    In-place quick sort implementation (modifies the original array)
    
    Args:
        arr: List to be sorted
        low: Starting index (default 0)
        high: Ending index (default len(arr)-1)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition the array and get the pivot index
        pivot_idx = partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        quick_sort_in_place(arr, low, pivot_idx - 1)
        quick_sort_in_place(arr, pivot_idx + 1, high)

def partition(arr, low, high):
    """
    Helper function for in-place quick sort that partitions the array
    and returns the pivot index.
    """
    # Choose the rightmost element as pivot
    pivot = arr[high]
    
    # Pointer for greater element
    i = low - 1
    
    for j in range(low, high):
        # If current element is smaller than the pivot
        if arr[j] <= pivot:
            # Increment the pointer for greater element
            i += 1
            # Swap elements
            arr[i], arr[j] = arr[j], arr[i]
    
    # Swap the pivot element with the greater element
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Return the position from where partition is done
    return i + 1

import random

def randomized_quick_sort(arr):
    if len(arr) <= 1:
        return arr.copy()
    
    # Choose random pivot
    pivot = random.choice(arr)
    
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    
    return randomized_quick_sort(less) + equal + randomized_quick_sort(greater)

def quick_sort_3way(arr, low=0, high=None):
    """
    3-way partition based quick sort that handles duplicate elements efficiently.
    Modifies the original array in-place.

    Key Characteristics
    Efficient with Duplicates: Handles multiple equal elements optimally
    Dutch National Flag: Based on Dijkstra's algorithm for partitioning

    Time Complexity:
    Worst case: O(n²) (with poor pivot choices)
    Best case: O(n) (when all elements are equal)
    Average case: O(n log n)
    Space Complexity: O(log n) for recursion stack

    Comparison with Standard Quick Sort
    Feature	Standard Quick Sort	3-Way Quick Sort
    Duplicate Handling	Less efficient	Highly efficient
    Partition Scheme	2-way	3-way
    Best Case (all equal)	O(n log n)	O(n)
    Implementation	Simpler	More complex

    This 3-way partitioning is particularly useful when:
    Your data contains many duplicate keys
    You need to partition data into three categories (<, =, >)
    You're implementing a quicksort-based selection algorithm

    Args:
        arr: List to be sorted
        low: Starting index (default 0)
        high: Ending index (default len(arr)-1)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition the array and get the left and right bounds
        lt, gt = partition_3way(arr, low, high)
        
        # Recursively sort elements before lt and after gt
        quick_sort_3way(arr, low, lt - 1)
        quick_sort_3way(arr, gt + 1, high)

def partition_3way(arr, low, high):
    """
    Dutch National Flag partition (3-way partition)
    Returns:
        tuple: (lt, gt) where:
            - all elements < pivot are in arr[low..lt-1]
            - all elements = pivot are in arr[lt..gt]
            - all elements > pivot are in arr[gt+1..high]
    """
    pivot = arr[high]  # Choose last element as pivot (can be optimized)
    lt = low    # Pointer for elements less than pivot
    gt = high   # Pointer for elements greater than pivot
    i = low     # Current element being processed
    
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1
    
    return lt, gt

def quick_sort_3way_optimized(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if high - low > 16:  # Use insertion sort for small subarrays
        # Median-of-three pivot selection
        mid = (low + high) // 2
        # Sort low, mid, high
        if arr[high] < arr[low]:
            arr[low], arr[high] = arr[high], arr[low]
        if arr[mid] < arr[low]:
            arr[mid], arr[low] = arr[low], arr[mid]
        if arr[high] < arr[mid]:
            arr[high], arr[mid] = arr[mid], arr[high]
        
        # Partition
        lt, gt = partition_3way(arr, low, high)
        
        # Recursive calls
        quick_sort_3way_optimized(arr, low, lt - 1)
        quick_sort_3way_optimized(arr, gt + 1, high)
    else:
        # Insertion sort for small subarrays
        insertion_sort(arr, low, high)

def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


numbers = [10, 7, 8, 9, 1, 5]
sorted_numbers = quick_sort(numbers)
print("Original:", numbers)
print("Sorted:", sorted_numbers)
# Output:
# Original: [10, 7, 8, 9, 1, 5]
# Sorted: [1, 5, 7, 8, 9, 10]

# Using in-place version
quick_sort_in_place(numbers)
print("In-place sorted:", numbers)
# Output: In-place sorted: [1, 5, 7, 8, 9, 10]

words = ["banana", "apple", "pear", "orange", "grape"]
sorted_words = quick_sort(words)
print("Original:", words)
print("Sorted:", sorted_words)
# Output:
# Original: ['banana', 'apple', 'pear', 'orange', 'grape']
# Sorted: ['apple', 'banana', 'grape', 'orange', 'pear']

data = [5, 2, 8, 2, 5, 1, 3, 1]
sorted_data = quick_sort(data)
print("Original:", data)
print("Sorted:", sorted_data)
# Output:
# Original: [5, 2, 8, 2, 5, 1, 3, 1]
# Sorted: [1, 1, 2, 2, 3, 5, 5, 8]