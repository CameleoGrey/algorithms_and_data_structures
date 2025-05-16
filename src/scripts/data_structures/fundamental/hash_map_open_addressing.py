

"""
This hash map resolves collisions via linear probing and supports dynamic resizing.

This implementation provides a basic but functional hash map based on open addressing with linear probing, 
including resizing and rehashing. If you'd like to extend it with features like quadratic probing, 
double hashing, or support for custom hash functions, just ask!

Features:
Insert (put)
Retrieve (get)
Delete (remove)
Check existence (contains)
Get size (__len__)
Clear all entries (clear)
Supports iteration over keys, values, items
"""

class HashMapOpenAddressing:
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor_threshold = 0.75
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        old_keys = self.keys
        old_values = self.values
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        for i in range(len(old_keys)):
            if old_keys[i] is not None:
                self.put(old_keys[i], old_values[i])

    def put(self, key, value):
        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()

        index = self._hash(key)
        start_index = index
        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.values[index] = value
                return
            index = (index + 1) % self.capacity
            if index == start_index:
                raise Exception("HashMap is full, resize failed.")

        self.keys[index] = key
        self.values[index] = value
        self.size += 1

    def get(self, key):
        index = self._hash(key)
        start_index = index
        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return None  # or raise KeyError

    def remove(self, key):
        index = self._hash(key)
        start_index = index
        while self.keys[index] is not None:
            if self.keys[index] == key:
                # Remove the key-value pair
                self.keys[index] = None
                self.values[index] = None
                self.size -= 1
                # Rehash subsequent elements to fill the gap
                self._rehash_from(index)
                return True
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return False

    def _rehash_from(self, start_index):
        index = (start_index + 1) % self.capacity
        while self.keys[index] is not None:
            key_to_rehash = self.keys[index]
            value_to_rehash = self.values[index]
            self.keys[index] = None
            self.values[index] = None
            self.size -= 1
            self.put(key_to_rehash, value_to_rehash)
            index = (index + 1) % self.capacity

    def contains(self, key):
        return self.get(key) is not None

    def __len__(self):
        return self.size

    def clear(self):
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0

    def keys_iter(self):
        for key in self.keys:
            if key is not None:
                yield key

    def values_iter(self):
        for key, value in zip(self.keys, self.values):
            if key is not None:
                yield value

    def items_iter(self):
        for key, value in zip(self.keys, self.values):
            if key is not None:
                yield (key, value)

    def __repr__(self):
        items = list(self.items_iter())
        return f"HashMap({items})"


# Create a hash map
hash_map = HashMapOpenAddressing()

# Insert key-value pairs
hash_map.put("apple", 3)
hash_map.put("banana", 5)
hash_map.put("orange", 2)

# Retrieve values
print("Apple:", hash_map.get("apple"))  # 3
print("Banana:", hash_map.get("banana"))  # 5

# Check existence
print("Contains 'orange'?", hash_map.contains("orange"))  # True
print("Contains 'grape'?", hash_map.contains("grape"))  # False

# Remove a key
hash_map.remove("banana")
print("After removing 'banana':", list(hash_map.items_iter()))

# Size
print("Size:", len(hash_map))  # 2

# Iterate over keys
print("Keys:", list(hash_map.keys_iter()))

# Clear all
hash_map.clear()
print("After clear:", list(hash_map.items_iter()))  # []

# Insert more items to test resizing
for i in range(20):
    hash_map.put(f"key{i}", i)

print("Size after insertions:", len(hash_map))
print("All items:", list(hash_map.items_iter()))
