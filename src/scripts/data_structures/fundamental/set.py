


"""
This custom set uses a hash table with open addressing for collision resolution.

This implementation provides a basic set with collision handling via open addressing, 
resizing, and set operations. If you'd like to extend it further or need a specific feature, just ask!

Features:
Add elements (add)
Remove elements (remove)
Check membership (contains)
Union, intersection, difference
Clear set
Get size
Iteration over elements
String representation
"""

class MySet:
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor_threshold = 0.75
        self.buckets = [None] * self.capacity

    def _hash(self, element):
        return hash(element) % self.capacity

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for item in old_buckets:
            if item is not None:
                self.add(item)

    def add(self, element):
        if self.contains(element):
            return
        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()
        index = self._hash(element)
        start_index = index
        while self.buckets[index] is not None:
            index = (index + 1) % self.capacity
            if index == start_index:
                raise Exception("HashSet is full, resize failed.")
        self.buckets[index] = element
        self.size += 1

    def remove(self, element):
        index = self._hash(element)
        start_index = index
        while self.buckets[index] is not None:
            if self.buckets[index] == element:
                self.buckets[index] = None
                self.size -= 1
                self._rehash_from(index)
                return True
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return False

    def _rehash_from(self, start_index):
        index = (start_index + 1) % self.capacity
        while self.buckets[index] is not None:
            element = self.buckets[index]
            self.buckets[index] = None
            self.size -= 1
            self.add(element)
            index = (index + 1) % self.capacity

    def contains(self, element):
        index = self._hash(element)
        start_index = index
        while self.buckets[index] is not None:
            if self.buckets[index] == element:
                return True
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return False

    def clear(self):
        self.buckets = [None] * self.capacity
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        for item in self.buckets:
            if item is not None:
                yield item

    def union(self, other_set):
        result = MySet()
        for item in self:
            result.add(item)
        for item in other_set:
            result.add(item)
        return result

    def intersection(self, other_set):
        result = MySet()
        for item in self:
            if other_set.contains(item):
                result.add(item)
        return result

    def difference(self, other_set):
        result = MySet()
        for item in self:
            if not other_set.contains(item):
                result.add(item)
        return result

    def __repr__(self):
        return "{" + ", ".join(repr(item) for item in self) + "}"

# Create sets
set1 = MySet()
set2 = MySet()

# Add elements
set1.add(1)
set1.add(2)
set1.add(3)

set2.add(3)
set2.add(4)
set2.add(5)

print("Set1:", set1)  # {1, 2, 3}
print("Set2:", set2)  # {3, 4, 5}

# Check membership
print("Does set1 contain 2?", set1.contains(2))  # True
print("Does set2 contain 2?", set2.contains(2))  # False

# Remove element
set1.remove(2)
print("Set1 after removing 2:", set1)  # {1, 3}

# Union
union_set = set1.union(set2)
print("Union:", union_set)  # {1, 3, 4, 5}

# Intersection
intersect_set = set1.intersection(set2)
print("Intersection:", intersect_set)  # {3}

# Difference
diff_set = set1.difference(set2)
print("Difference (set1 - set2):", diff_set)  # {1}

# Length
print("Length of set1:", len(set1))  # 2

# Iterate
print("Elements in set2:")
for item in set2:
    print(item)

# Clear set
set1.clear()
print("Set1 after clear:", set1)  # {}
