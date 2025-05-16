
"""
A heap (concrete implementation of ADT Priority Queue) is a specialized tree-based data structure that satisfies the heap property: 
in a max-heap, every parent node is greater than or equal to its children; in a min-heap, 
every parent node is less than or equal to its children. Heaps are commonly implemented as binary trees but can also be d-ary or other structures.

This implementation uses a list to represent the heap, where for any element at index i:
Its parent is at index (i - 1) // 2
Its children are at indices 2 * i + 1 and 2 * i + 2

Key Characteristics:
Complete Binary Tree: All levels are fully filled except possibly the last, which is filled from left to right.
Heap Property: Ensures efficient access to the maximum (max-heap) or minimum (min-heap) element.
Efficient Operations:
Insert: O(log n)
Extract Max/Min: O(log n)
Peek Max/Min: O(1)
"""

# Implementation of a Binary Heap in Python (Min-Heap)

class BinaryHeap:
    def __init__(self):
        self.heap = []

    def insert(self, val):
        """Insert a new element into the heap."""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        """Remove and return the smallest element."""
        if not self.heap:
            return None
        min_val = self.heap[0]
        last_val = self.heap.pop()
        if self.heap:
            self.heap[0] = last_val
            self._heapify_down(0)
        return min_val

    def peek(self):
        """Return the smallest element without removing."""
        return self.heap[0] if self.heap else None

    def _heapify_up(self, index):
        """Maintain heap property after insertion."""
        parent = (index - 1) // 2
        while index > 0 and self.heap[parent] > self.heap[index]:
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        """Maintain heap property after removal."""
        n = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest

# Usage example
heap = BinaryHeap()
for num in [5, 3, 8, 1, 2, 9]:
    heap.insert(num)

print("Heap elements after insertions:", heap.heap)
print("Minimum element (peek):", heap.peek())

print("Extracting elements in order:")
while heap.heap:
    print(heap.extract_min(), end=' ')
# Output:
# Heap elements after insertions: [1, 2, 8, 5, 3, 9]
# Minimum element (peek): 1
# Extracting elements in order:
# 1 2 3 5 8 9
