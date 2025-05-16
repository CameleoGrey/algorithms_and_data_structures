


"""
This linked list supports insertion, deletion, traversal, searching, and more.

This implementation provides a full-featured singly linked list with common operations. 
If you'd like a doubly linked list or additional methods, just ask!

Features:
Append at end
Insert at position
Remove by value
Remove at position
Search for value
Get size
Clear list
Iterate over elements
String representation
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        """Add element at the end."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1

    def insert(self, index, data):
        """Insert element at specific position."""
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")
        new_node = Node(data)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.size += 1

    def remove(self, data):
        """Remove first occurrence of data."""
        current = self.head
        prev = None
        while current:
            if current.data == data:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        return False

    def remove_at(self, index):
        """Remove element at specific position."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        current = self.head
        prev = None
        for _ in range(index):
            prev = current
            current = current.next
        if prev:
            prev.next = current.next
        else:
            self.head = current.next
        self.size -= 1
        return current.data

    def search(self, data):
        """Search for data, return index or -1."""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def get(self, index):
        """Get data at index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def clear(self):
        """Clear the list."""
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __repr__(self):
        return "->".join(str(data) for data in self)


# Create a linked list
ll = LinkedList()

# Append elements
ll.append(10)
ll.append(20)
ll.append(30)
print("List after appending:", ll)  # 10->20->30

# Insert at position
ll.insert(1, 15)
print("After inserting 15 at index 1:", ll)  # 10->15->20->30

# Search for element
print("Index of 20:", ll.search(20))  # 2

# Get element at index
print("Element at index 3:", ll.get(3))  # 30

# Remove element by value
ll.remove(15)
print("After removing 15:", ll)  # 10->20->30

# Remove at position
removed_value = ll.remove_at(0)
print(f"Removed value at index 0: {removed_value}")
print("List after removal:", ll)  # 20->30

# Length of list
print("Length:", len(ll))  # 2

# Iterate over list
print("Iterate over list:")
for item in ll:
    print(item)

# Clear list
ll.clear()
print("After clearing:", ll)  # (empty)
