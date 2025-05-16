

"""
This implementation uses separate chaining with linked lists to handle collisions.

This implementation provides a basic but functional hash map with 
collision handling via chaining, resizing, and common dictionary operations. 
If you'd like to extend it with features like iterators, custom hash functions, or thread safety, just ask!

Core Features:
Insert key-value pairs (put)
Retrieve values by key (get)
Remove key-value pairs (remove)
Check if key exists (contains)
Get current size (size)
Clear the hash map (clear)
Support for iteration over keys
"""

class HashMap:
    class Node:
        def __init__(self, key, value, next_node=None):
            self.key = key
            self.value = value
            self.next = next_node

    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.buckets = [None] * self.capacity
        self.size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        head = self.buckets[index]
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        new_node = self.Node(key, value, head)
        self.buckets[index] = new_node
        self.size += 1
        # Optional: resize if load factor exceeds threshold
        if self.size / self.capacity > 0.75:
            self._resize()

    def get(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None  # or raise KeyError

    def remove(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        return False

    def contains(self, key):
        return self.get(key) is not None

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for head in old_buckets:
            current = head
            while current:
                self.put(current.key, current.value)
                current = current.next

    def clear(self):
        self.buckets = [None] * self.capacity
        self.size = 0

    def __len__(self):
        return self.size

    def keys(self):
        for bucket in self.buckets:
            current = bucket
            while current:
                yield current.key
                current = current.next

    def values(self):
        for bucket in self.buckets:
            current = bucket
            while current:
                yield current.value
                current = current.next

    def items(self):
        for bucket in self.buckets:
            current = bucket
            while current:
                yield (current.key, current.value)
                current = current.next

    def __repr__(self):
        items = list(self.items())
        return f"HashMap({items})"

# Create a hash map
hash_map = HashMap()

# Insert key-value pairs
hash_map.put("apple", 3)
hash_map.put("banana", 5)
hash_map.put("orange", 2)

# Retrieve values
print("Apple count:", hash_map.get("apple"))  # 3
print("Banana count:", hash_map.get("banana"))  # 5

# Check existence
print("Contains 'orange'?", hash_map.contains("orange"))  # True
print("Contains 'grape'?", hash_map.contains("grape"))  # False

# Remove a key
hash_map.remove("banana")
print("After removing 'banana':", list(hash_map.items()))

# Size
print("Size:", len(hash_map))  # 2

# Iterate over keys
print("Keys:", list(hash_map.keys()))

# Clear the hash map
hash_map.clear()
print("After clearing:", list(hash_map.items()))  # []

# Insert more items to test resizing
for i in range(20):
    hash_map.put(f"key{i}", i)

print("Size after insertions:", len(hash_map))
print("All items:", list(hash_map.items()))
