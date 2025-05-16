


"""
Shell sort is an optimization of insertion sort that allows the exchange of 
items that are far apart. It works by sorting elements at specific intervals (gaps) 
and gradually reducing these intervals until the entire list is sorted. Shell sort 
has a time complexity ranging from O(n log n) to O(n²) depending on the gap sequence used.

Key Characteristics of Shell Sort
Time Complexity:
Depends on the gap sequence used
Worst-case: O(n²) (with poor gap sequences)
Best-case: O(n log n) (with good gap sequences)
Average-case: Typically between O(n log n) and O(n^(3/2))
Space Complexity: O(1) - It's an in-place sorting algorithm

Advantages:
More efficient than insertion sort for medium-sized lists
No additional memory required
Performs well on partially sorted arrays
Can be implemented with various gap sequences for optimization

Disadvantages:
Complexity depends on gap sequence choice
Not as efficient as more advanced algorithms like quicksort or merge sort for large datasets
Unstable sort (doesn't maintain relative order of equal elements)

How It Works
Shell sort works by:
Choosing an initial gap size (typically half the array length)
Performing insertion sort on elements separated by this gap
Reducing the gap size and repeating the process
Continuing until the gap becomes 1 (at which point it becomes a standard insertion sort)

The efficiency of Shell sort depends heavily on the gap sequence used. Common sequences include:
Shell's original sequence (n/2, n/4, ..., 1)
Knuth's sequence (1, 4, 13, 40, ...)
Sedgewick's sequence (1, 5, 19, 41, 109, ...)
"""

def shell_sort(arr):
    """
    Sorts an array in ascending order using Shell sort algorithm
    :param arr: List of elements to be sorted
    """
    n = len(arr)
    # Start with a large gap, then reduce the gap
    gap = n // 2
    
    while gap > 0:
        # Do a gapped insertion sort for this gap size
        for i in range(gap, n):
            # Save the current element and make a hole at position i
            temp = arr[i]
            # Shift earlier gap-sorted elements up until the correct location
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            # Put the saved element in the correct location
            arr[j] = temp
        # Reduce the gap for the next iteration
        gap //= 2


# Usage Examples
if __name__ == "__main__":
    # Example 1: Sorting a list of integers
    data = [12, 34, 54, 2, 3]
    print("Original array:", data)
    shell_sort(data)
    print("Sorted array:", data)
    
    # Example 2: Sorting a list of floating-point numbers
    float_data = [5.2, 1.1, 3.7, 2.8, 4.4]
    print("\nOriginal array:", float_data)
    shell_sort(float_data)
    print("Sorted array:", float_data)
    
    # Example 3: Sorting a list of characters
    char_data = ['z', 'a', 'c', 'f', 'b']
    print("\nOriginal array:", char_data)
    shell_sort(char_data)
    print("Sorted array:", char_data)
    
    # Example 4: Sorting an already sorted array
    sorted_data = [1, 2, 3, 4, 5]
    print("\nOriginal array:", sorted_data)
    shell_sort(sorted_data)
    print("Sorted array:", sorted_data)
    
    # Example 5: Sorting a large array
    import random
    large_data = random.sample(range(1, 1000), 20)
    print("\nOriginal large array (first 20 elements):", large_data)
    shell_sort(large_data)
    print("Sorted large array (first 20 elements):", large_data)
    
    # Example 6: Custom gap sequence (Knuth's sequence)
    def shell_sort_knuth(arr):
        n = len(arr)
        gap = 1
        # Generate Knuth's sequence: 1, 4, 13, 40, 121, ...
        while gap < n // 3:
            gap = 3 * gap + 1
        
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 3
    
    knuth_data = [84, 23, 62, 44, 16, 30, 95, 51]
    print("\nOriginal array (Knuth's sequence):", knuth_data)
    shell_sort_knuth(knuth_data)
    print("Sorted array (Knuth's sequence):", knuth_data)