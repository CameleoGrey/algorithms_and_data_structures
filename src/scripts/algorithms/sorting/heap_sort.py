
"""
Heap sort is a comparison-based sorting algorithm that uses a binary heap data structure. It has O(n log n) time complexity for all cases.

Key Points
The algorithm first builds a max heap from the input data.
The largest item is moved to the end of the array (root of the heap is swapped with the last item).
The heap size is reduced by one, and heapify is called on the new root.
This process is repeated until the heap size is 1.

Heap sort is an in-place algorithm but is not stable (doesn't maintain the relative order of equal elements).
"""

def heapify(arr, n, i):
    """
    Heapify subtree rooted at index i.
    :param arr: The array to heapify
    :param n: Size of the heap
    :param i: Index of the root node
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2

    # If left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Change root if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        heapify(arr, n, largest)  # Heapify the affected sub-tree


def heap_sort(arr):
    """
    Main function to perform heap sort
    :param arr: Array to be sorted
    """
    n = len(arr)

    # Build a maxheap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)  # Heapify root element


# Usage Examples
if __name__ == "__main__":
    # Example 1: Sorting a list of integers
    data = [12, 11, 13, 5, 6, 7]
    print("Original array:", data)
    heap_sort(data)
    print("Sorted array:", data)
    
    # Example 2: Sorting a list of floating-point numbers
    float_data = [4.2, 6.1, 3.5, 9.8, 2.7, 5.5]
    print("\nOriginal array:", float_data)
    heap_sort(float_data)
    print("Sorted array:", float_data)
    
    # Example 3: Sorting a list of characters
    char_data = ['d', 'b', 'a', 'c', 'f', 'e']
    print("\nOriginal array:", char_data)
    heap_sort(char_data)
    print("Sorted array:", char_data)
    
    # Example 4: Sorting an already sorted array
    sorted_data = [1, 2, 3, 4, 5]
    print("\nOriginal array:", sorted_data)
    heap_sort(sorted_data)
    print("Sorted array:", sorted_data)
    
    # Example 5: Sorting a large array
    import random
    large_data = random.sample(range(1, 1000), 20)
    print("\nOriginal large array (first 20 elements):", large_data[:20])
    heap_sort(large_data)
    print("Sorted large array (first 20 elements):", large_data[:20])