


"""
Insertion sort is a simple comparison-based sorting algorithm that builds the 
final sorted array one item at a time. It is efficient for small datasets and 
nearly sorted data, with O(n²) time complexity in the worst case but O(n) in the best case (already sorted).

Key Characteristics of Insertion Sort
Time Complexity:
Worst-case: O(n²) - When array is reverse sorted
Best-case: O(n) - When array is already sorted
Average-case: O(n²)
Space Complexity: O(1) - It's an in-place sorting algorithm

Advantages:
Simple implementation
Efficient for small data sets
More efficient than bubble sort and selection sort in practice
Adaptive: Efficient for data sets that are already substantially sorted
Stable: Maintains relative order of equal elements
Online: Can sort a list as it receives it

Disadvantages:
Poor performance on large lists
Generally performs worse than more advanced algorithms like quicksort or merge sort

How It Works
Insertion sort works similarly to how you might sort playing cards in your hands:
Start with the second element (index 1) and compare it with the elements before it
If the current element is smaller than the previous element, shift the previous elements to the right
Insert the current element in its correct position
Repeat for all elements in the array

This algorithm is particularly useful when the data is nearly sorted or when the dataset is small. 
Many more complex algorithms switch to insertion sort when the subproblems become small enough.
"""

def insertion_sort(arr):
    """
    Sorts an array in ascending order using insertion sort algorithm
    :param arr: List of elements to be sorted
    """
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]  # Current element to be inserted
        j = i - 1     # Index of previous element
        
        # Move elements of arr[0..i-1] that are greater than key
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert the key at its correct position
        arr[j + 1] = key


# Usage Examples
if __name__ == "__main__":
    # Example 1: Sorting a list of integers
    data = [12, 11, 13, 5, 6]
    print("Original array:", data)
    insertion_sort(data)
    print("Sorted array:", data)
    
    # Example 2: Sorting a list of floating-point numbers
    float_data = [5.2, 1.1, 3.7, 2.8, 4.4]
    print("\nOriginal array:", float_data)
    insertion_sort(float_data)
    print("Sorted array:", float_data)
    
    # Example 3: Sorting a list of characters
    char_data = ['z', 'a', 'c', 'f', 'b']
    print("\nOriginal array:", char_data)
    insertion_sort(char_data)
    print("Sorted array:", char_data)
    
    # Example 4: Sorting an already sorted array
    sorted_data = [1, 2, 3, 4, 5]
    print("\nOriginal array:", sorted_data)
    insertion_sort(sorted_data)
    print("Sorted array:", sorted_data)
    
    # Example 5: Sorting a nearly sorted array
    nearly_sorted = [1, 3, 2, 4, 6, 5]
    print("\nOriginal nearly sorted array:", nearly_sorted)
    insertion_sort(nearly_sorted)
    print("Sorted array:", nearly_sorted)
    
    # Example 6: Sorting a large array (not recommended for insertion sort)
    import random
    large_data = random.sample(range(1, 1000), 10)  # Keeping it small for demonstration
    print("\nOriginal large array:", large_data)
    insertion_sort(large_data)
    print("Sorted large array:", large_data)