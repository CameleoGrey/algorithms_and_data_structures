

"""
This queue supports enqueue, dequeue, peek, size, and more.

Features:
Enqueue (add to rear)
Dequeue (remove from front)
Peek (view front element)
Check if empty
Get size
Clear the queue
Iterable over elements
String representation
"""

class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        """Add item to the rear of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item of the queue."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def peek(self):
        """View the front item without removing."""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self._items)

    def clear(self):
        """Clear all items from the queue."""
        self._items.clear()

    def __iter__(self):
        """Iterate over the queue elements."""
        return iter(self._items)

    def __repr__(self):
        return f"Queue({self._items})"

# Create a queue
q = Queue()

# Enqueue elements
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print("Queue after enqueuing:", q)  # Queue([1, 2, 3])

# Peek at front element
print("Front element:", q.peek())  # 1

# Dequeue elements
print("Dequeued:", q.dequeue())  # 1
print("Queue after dequeue:", q)  # Queue([2, 3])

# Check size
print("Size:", q.size())  # 2

# Check if empty
print("Is empty?", q.is_empty())  # False

# Iterate over queue
print("Iterate over queue:")
for item in q:
    print(item)

# Clear the queue
q.clear()
print("After clearing:", q)  # Queue([])
print("Is empty?", q.is_empty()) # True
