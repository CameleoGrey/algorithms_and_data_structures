
"""
Key Features of this Implementation:

This implementation provides O(1) time complexity for all primary operations (add/remove from both ends), 
making it efficient for use cases that require frequent access to both ends of the collection.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def is_empty(self):
        return self.size == 0
    
    def __len__(self):
        return self.size
    
    def add_front(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node
        self.size += 1
    
    def add_rear(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.prev = self.rear
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
    
    def remove_front(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        data = self.front.data
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
            self.front.prev = None
        self.size -= 1
        return data
    
    def remove_rear(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        data = self.rear.data
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.rear = self.rear.prev
            self.rear.next = None
        self.size -= 1
        return data
    
    def peek_front(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.front.data
    
    def peek_rear(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.rear.data
    
    def __str__(self):
        items = []
        current = self.front
        while current:
            items.append(str(current.data))
            current = current.next
        return '[' + ', '.join(items) + ']'
    
    def clear(self):
        self.front = self.rear = None
        self.size = 0

# Usage Examples
if __name__ == "__main__":
    print("Creating a new deque...")
    dq = Deque()
    
    print("\nAdding elements to the front:")
    dq.add_front(10)
    dq.add_front(20)
    dq.add_front(30)
    print(dq)  # [30, 20, 10]
    
    print("\nAdding elements to the rear:")
    dq.add_rear(40)
    dq.add_rear(50)
    print(dq)  # [30, 20, 10, 40, 50]
    
    print("\nRemoving from front:", dq.remove_front())  # 30
    print("Removing from rear:", dq.remove_rear())     # 50
    print(dq)  # [20, 10, 40]
    
    print("\nPeeking at front and rear:")
    print("Front element:", dq.peek_front())  # 20
    print("Rear element:", dq.peek_rear())    # 40
    
    print("\nChecking deque size and emptiness:")
    print("Size:", len(dq))            # 3
    print("Is empty?", dq.is_empty())  # False
    
    print("\nClearing the deque...")
    dq.clear()
    print("Is empty after clear?", dq.is_empty())  # True
    
    print("\nUsing deque as both stack and queue:")
    # As stack (LIFO) - using rear for both add and remove
    print("\nAs stack:")
    dq.add_rear(1)
    dq.add_rear(2)
    dq.add_rear(3)
    print(dq)  # [1, 2, 3]
    print("Pop:", dq.remove_rear())  # 3
    print("Pop:", dq.remove_rear())  # 2
    print(dq)  # [1]
    
    # As queue (FIFO) - add to rear, remove from front
    print("\nAs queue:")
    dq.clear()
    dq.add_rear('a')
    dq.add_rear('b')
    dq.add_rear('c')
    print(dq)  # ['a', 'b', 'c']
    print("Dequeue:", dq.remove_front())  # 'a'
    print("Dequeue:", dq.remove_front())  # 'b'
    print(dq)  # ['c']