
"""
Bubble sort has a time complexity of O(n²) in the worst and average cases, 
and O(n) in the best case (when the list is already sorted and using the optimized version). 
It's a simple sorting algorithm but not efficient for large datasets.
"""


def bubble_sort(arr):
    """
    Sorts a list in ascending order using the Bubble Sort algorithm.
    
    Args:
        arr (list): The list to be sorted
        
    Returns:
        list: The sorted list
    """
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    
    return arr

def optimized_bubble_sort(arr):
    """
    Optimized Bubble Sort that stops if no swaps are made in a pass.
    """
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        
        # If no two elements were swapped in inner loop, then break
        if not swapped:
            break
    
    return arr


numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print("Sorted numbers:", sorted_numbers)
# Output: Sorted numbers: [11, 12, 22, 25, 34, 64, 90]

fruits = ["banana", "apple", "orange", "grape", "kiwi"]
sorted_fruits = bubble_sort(fruits)
print("Sorted fruits:", sorted_fruits)
# Output: Sorted fruits: ['apple', 'banana', 'grape', 'kiwi', 'orange']

data = [5, 2, 8, 2, 5, 1, 3, 1]
sorted_data = bubble_sort(data)
print("Sorted data with duplicates:", sorted_data)
# Output: Sorted data with duplicates: [1, 1, 2, 2, 3, 5, 5, 8]

almost_sorted = [1, 2, 3, 4, 6, 5]
sorted_list = optimized_bubble_sort(almost_sorted)
print("Optimized sort result:", sorted_list)
# Output: Optimized sort result: [1, 2, 3, 4, 5, 6]