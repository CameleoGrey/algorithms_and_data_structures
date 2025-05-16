


"""
A Bag (or multiset) is a collection that allows multiple occurrences of elements, tracking their counts.

Core Methods:
add(element, count=1) — add elements with optional count.
remove(element, count=1) — remove a specified number of elements.
count(element) — get the number of occurrences of an element.
elements() — return all elements considering their counts.
__contains__(element) — check if an element exists.
__len__() — total number of elements (including duplicates).
__repr__() — string representation for debugging.
"""

class Bag:
    def __init__(self):
        self._elements = {}

    def add(self, element, count=1):
        """Add an element with the specified count."""
        if count <= 0:
            return
        self._elements[element] = self._elements.get(element, 0) + count

    def remove(self, element, count=1):
        """Remove a specified count of an element."""
        if element not in self._elements:
            return
        if count >= self._elements[element]:
            del self._elements[element]
        else:
            self._elements[element] -= count

    def count(self, element):
        """Return the count of an element."""
        return self._elements.get(element, 0)

    def elements(self):
        """Return a list of all elements considering their counts."""
        result = []
        for element, count in self._elements.items():
            result.extend([element] * count)
        return result

    def __contains__(self, element):
        """Check if element exists in the bag."""
        return element in self._elements

    def __len__(self):
        """Total number of elements in the bag."""
        return sum(self._elements.values())

    def __repr__(self):
        return f"Bag({self._elements})"

# Create a new bag
bag = Bag()

# Add elements
bag.add('apple', 3)
bag.add('banana', 2)
bag.add('orange')

print("After additions:", bag)
# Output: Bag({'apple': 3, 'banana': 2, 'orange': 1})

# Check counts
print("Count of 'apple':", bag.count('apple'))  # 3
print("Total elements:", len(bag))             # 6

# Remove some elements
bag.remove('apple', 2)
print("After removing 2 'apple':", bag)
# Output: Bag({'apple': 1, 'banana': 2, 'orange': 1})

# Check if an element exists
print("'banana' in bag?", 'banana' in bag)  # True
print("'grape' in bag?", 'grape' in bag)    # False

# Get all elements
print("All elements:", bag.elements())
# Output: ['apple', 'banana', 'banana', 'orange']

# Remove all 'banana'
bag.remove('banana', 2)
print("After removing all 'banana':", bag)
# Output: Bag({'apple': 1, 'orange': 1})

