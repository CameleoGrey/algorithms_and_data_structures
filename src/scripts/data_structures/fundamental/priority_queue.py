import heapq

class PriorityQueue:
    def __init__(self):
        """Initialize an empty priority queue."""
        self._heap = []
        self._index = 0  # Used to break ties when priorities are equal

    def push(self, item, priority):
        """Add an item to the queue with a given priority.
        
        Args:
            item: The item to be added.
            priority: The priority of the item (lower values have higher priority).
        """
        heapq.heappush(self._heap, (priority, self._index, item))
        self._index += 1

    def pop(self):
        """Remove and return the highest priority item from the queue.
        
        Returns:
            The item with the highest priority.
        
        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return heapq.heappop(self._heap)[-1]  # Return just the item

    def peek(self):
        """Return the highest priority item without removing it.
        
        Returns:
            The item with the highest priority.
            
        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._heap[0][-1]  # Return just the item

    def is_empty(self):
        """Check if the priority queue is empty.
        
        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self._heap) == 0

    def size(self):
        """Return the number of items in the priority queue.
        
        Returns:
            int: The number of items in the queue.
        """
        return len(self._heap)

    def change_priority(self, item, new_priority):
        """Change the priority of an existing item in the queue.
        
        Args:
            item: The item whose priority needs to be changed.
            new_priority: The new priority for the item.
            
        Returns:
            bool: True if the priority was changed, False if the item wasn't found.
        """
        for i, (priority, _, existing_item) in enumerate(self._heap):
            if existing_item == item:
                self._heap[i] = (new_priority, self._index, item)
                self._index += 1
                heapq.heapify(self._heap)  # Rebuild the heap
                return True
        return False

    def __str__(self):
        """Return a string representation of the priority queue."""
        items = [f"{item} (priority: {priority})" for priority, _, item in sorted(self._heap)]
        return "PriorityQueue: [" + ", ".join(items) + "]"


# Usage Examples
if __name__ == "__main__":
    print("=== Priority Queue Examples ===")
    
    # Example 1: Basic usage
    print("\nExample 1: Basic operations")
    pq = PriorityQueue()
    pq.push("task1", 3)
    pq.push("task2", 1)
    pq.push("task3", 2)
    
    print(pq)  # PriorityQueue: [task2 (priority: 1), task3 (priority: 2), task1 (priority: 3)]
    
    print("Popped:", pq.pop())  # task2
    print("Peek:", pq.peek())   # task3
    print("Queue size:", pq.size())  # 2
    
    # Example 2: Changing priority
    print("\nExample 2: Changing priority")
    pq = PriorityQueue()
    pq.push("taskA", 5)
    pq.push("taskB", 3)
    pq.push("taskC", 4)
    
    print("Before priority change:")
    print(pq)
    
    pq.change_priority("taskA", 2)
    
    print("After changing taskA's priority to 2:")
    print(pq)
    
    # Example 3: Emergency room simulation
    print("\nExample 3: Emergency room simulation")
    er_queue = PriorityQueue()
    er_queue.push("Patient with mild fever", 4)  # Lower priority
    er_queue.push("Patient with chest pain", 1)  # Highest priority
    er_queue.push("Patient with broken arm", 3)
    er_queue.push("Patient with severe bleeding", 1)  # Also highest priority
    
    print("Patients in order of treatment:")
    while not er_queue.is_empty():
        print(f"Treating: {er_queue.pop()}")
    
    # Example 4: Handling empty queue
    print("\nExample 4: Handling empty queue")
    empty_pq = PriorityQueue()
    try:
        empty_pq.pop()
    except IndexError as e:
        print(f"Error: {e}")