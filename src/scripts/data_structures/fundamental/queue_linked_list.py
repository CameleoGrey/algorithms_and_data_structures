


"""
This queue supports enqueue, dequeue, peek, size, and iteration.

Features:
Enqueue (add to rear)
Dequeue (remove from front)
Peek (view front element)
Check if empty
Get size
Clear
Iterate over elements
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        """Add element to the rear of the queue."""
        new_node = Node(data)
        if not self.front:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        """Remove and return element from the front of the queue."""
        if not self.front:
            raise IndexError("Dequeue from empty queue")
        data = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self.size -= 1
        return data

    def peek(self):
        """View the front element without removing."""
        if not self.front:
            raise IndexError("Peek from empty queue")
        return self.front.data

    def is_empty(self):
        """Check if the queue is empty."""
        return self.size == 0

    def __len__(self):
        return self.size

    def clear(self):
        """Clear the queue."""
        self.front = None
        self.rear = None
        self.size = 0

    def __iter__(self):
        current = self.front
        while current:
            yield current.data
            current = current.next

    def __repr__(self):
        return "Queue(" + " -> ".join(str(item) for item in self) + ")"

# Create a queue
q = Queue()

# Enqueue elements
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print("Queue after enqueuing:", q)  # Queue(1 -> 2 -> 3)

# Peek at front
print("Front element:", q.peek())  # 1

# Dequeue elements
print("Dequeued:", q.dequeue())  # 1
print("Queue after dequeue:", q)  # Queue(2 -> 3)

# Check if empty
print("Is empty?", q.is_empty())  # False

# Dequeue remaining
q.dequeue()
q.dequeue()
print("Is empty after removing all elements?", q.is_empty())  # True

# Try to dequeue from empty (will raise error)
try:
    q.dequeue()
except IndexError as e:
    print("Error:", e)

# Enqueue again
q.enqueue('a')
q.enqueue('b')
print("Queue:", q)  # Queue(a -> b)

# Iterate over queue
print("Iterate over queue:")
for item in q:
    print(item)

# Clear queue
q.clear()
print("After clearing:", q)  # Queue()
