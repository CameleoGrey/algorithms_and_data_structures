

"""
Selection sort is a simple comparison-based sorting algorithm with O(n²) time complexity 
for all cases, making it inefficient for large datasets. However, it performs well for small 
lists and has the advantage of minimal memory usage since it's an in-place sorting algorithm.

Key Characteristics of Selection Sort
Time Complexity:
Worst-case: O(n²)
Best-case: O(n²)
Average-case: O(n²)
Space Complexity: O(1) - It's an in-place sorting algorithm

Advantages:
Simple to implement
Performs well on small lists
Doesn't require additional memory space
Makes minimum number of swaps (O(n) swaps)

Disadvantages:
Poor performance on large lists
Not stable (doesn't maintain the relative order of equal elements)
Not adaptive (doesn't take advantage of existing order in input)

The algorithm divides the input list into two parts: the sublist of items already sorted and the sublist of 
items remaining to be sorted. Initially, the sorted sublist is empty, and the unsorted sublist is the entire 
input list. The algorithm proceeds by finding the smallest element in the unsorted sublist, swapping it with the 
leftmost unsorted element, and moving the sublist boundaries one element to the right.

"""

def selection_sort(arr):
    """
    Sorts an array in ascending order using selection sort algorithm
    :param arr: List of elements to be sorted
    """
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# Usage Examples
if __name__ == "__main__":
    # Example 1: Sorting a list of integers
    data = [64, 25, 12, 22, 11]
    print("Original array:", data)
    selection_sort(data)
    print("Sorted array:", data)
    
    # Example 2: Sorting a list of floating-point numbers
    float_data = [5.2, 1.1, 3.7, 2.8, 4.4]
    print("\nOriginal array:", float_data)
    selection_sort(float_data)
    print("Sorted array:", float_data)
    
    # Example 3: Sorting a list of characters
    char_data = ['z', 'a', 'c', 'f', 'b']
    print("\nOriginal array:", char_data)
    selection_sort(char_data)
    print("Sorted array:", char_data)
    
    # Example 4: Sorting an already sorted array
    sorted_data = [1, 2, 3, 4, 5]
    print("\nOriginal array:", sorted_data)
    selection_sort(sorted_data)
    print("Sorted array:", sorted_data)
    
    # Example 5: Sorting a large array (not recommended for selection sort)
    import random
    large_data = random.sample(range(1, 1000), 10)  # Keeping it small for demonstration
    print("\nOriginal large array:", large_data)
    selection_sort(large_data)
    print("Sorted large array:", large_data)