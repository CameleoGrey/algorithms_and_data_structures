


"""
This stack supports typical operations: push, pop, peek, check if empty, size, and clear.

This provides a full-featured stack implementation suitable for most use cases. 
If you'd like a version with additional features or a different type of stack (e.g., bounded), just ask!

Features:
Push element onto stack
Pop element from stack
Peek at top element
Check if stack is empty
Get current size
Clear the stack
String representation
"""

class Stack:
    def __init__(self):
        self._elements = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._elements.append(item)

    def pop(self):
        """Remove and return the top item of the stack."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._elements.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._elements[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self._elements) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._elements)

    def clear(self):
        """Remove all items from the stack."""
        self._elements.clear()

    def __repr__(self):
        return f"Stack({self._elements})"

# Create a stack
stack = Stack()

# Push elements
stack.push(10)
stack.push(20)
stack.push(30)
print("Stack after pushes:", stack)  # Stack([10, 20, 30])

# Peek at the top element
print("Top element:", stack.peek())  # 30

# Pop elements
print("Popped:", stack.pop())  # 30
print("Stack after pop:", stack)  # Stack([10, 20])

# Check if empty
print("Is stack empty?", stack.is_empty())  # False

# Pop remaining elements
stack.pop()
stack.pop()

print("Stack after removing all elements:", stack)  # Stack([])

# Try to pop from empty stack (raises exception)
try:
    stack.pop()
except IndexError as e:
    print("Error:", e)

# Push again and clear
stack.push(100)
stack.push(200)
print("Before clear:", stack)
stack.clear()
print("After clear:", stack)
