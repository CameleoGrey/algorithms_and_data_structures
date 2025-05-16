

"""
A Dequeue allows insertion and removal of elements from both ends.
"""

class Dequeue:
    def __init__(self):
        self._items = []

    def append(self, item):
        """Add item to the right end."""
        self._items.append(item)

    def appendleft(self, item):
        """Add item to the left end."""
        self._items.insert(0, item)

    def pop(self):
        """
        Remove and return item from the right end.
        O(1)
        """
        if self.is_empty():
            raise IndexError("pop from an empty deque")
        return self._items.pop()

    def popleft(self):
        """
        Remove and return item from the left end.
        O(N)
        """
        if self.is_empty():
            raise IndexError("popleft from an empty deque")
        return self._items.pop(0)

    def peek(self):
        """View the rightmost item without removing."""
        if self.is_empty():
            raise IndexError("peek from an empty deque")
        return self._items[-1]

    def peekleft(self):
        """View the leftmost item without removing."""
        if self.is_empty():
            raise IndexError("peekleft from an empty deque")
        return self._items[0]

    def is_empty(self):
        """Check if the deque is empty."""
        return len(self._items) == 0

    def __len__(self):
        """Number of items in the deque."""
        return len(self._items)

    def __repr__(self):
        return f"Dequeue({self._items})"
    
# Create a new deque
dq = Dequeue()

# Add elements to both ends
dq.append(10)
dq.appendleft(20)
dq.append(30)

print("Deque after additions:", dq)
# Output: Dequeue([20, 10, 30])

# View elements without removing
print("Peek left:", dq.peekleft())   # 20
print("Peek right:", dq.peek())       # 30

# Remove elements from both ends
print("Popped from right:", dq.pop())     # 30
print("Popped from left:", dq.popleft())  # 20

print("Deque after removals:", dq)
# Output: Dequeue([10])

# Check if empty
print("Is empty?", dq.is_empty())  # False

# Remove last element
dq.popleft()
print("Is empty after removing last element?", dq.is_empty())  # True

# Attempting to pop from empty deque raises error
try:
    dq.pop()
except IndexError as e:
    print("Error:", e)
