

"""
When to Use a Bloom Filter:
When you need space-efficient probabilistic set membership testing
When false positives are acceptable but false negatives are not
For pre-filtering before more expensive checks (e.g., database lookups)
In network routers, spell checkers, and other applications where memory is constrained

Limitations:
No Item Removal: Standard Bloom filters don't support deletion
False Positives: May incorrectly report that an item is present
Fixed Capacity: Performance degrades if you insert more items than the designed capacity

For scenarios needing deletion, consider a Counting Bloom Filter variant.
"""

# pip install mmh3 bitarray
import mmh3  # MurmurHash3 - a good hash function for bloom filters
from math import log
from bitarray import bitarray  # Efficient bit array implementation

class BloomFilter:
    def __init__(self, capacity, error_rate=0.01):
        """
        Initialize a Bloom filter with given capacity and error rate.
        
        Parameters:
            capacity (int): Expected number of items to store
            error_rate (float): Desired false positive rate (0.01 = 1%)
        """
        self.capacity = capacity
        self.error_rate = error_rate
        
        # Calculate optimal size (m) and number of hash functions (k)
        self.size = self._calculate_size(capacity, error_rate)
        self.hash_count = self._calculate_hash_count(capacity, self.size)
        
        # Initialize bit array
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(False)
    
    def _calculate_size(self, n, p):
        """Calculate optimal size (m) for the filter"""
        m = -(n * log(p)) / (log(2) ** 2)
        return int(m)
    
    def _calculate_hash_count(self, n, m):
        """Calculate optimal number of hash functions (k)"""
        k = (m / n) * log(2)
        return int(k)
    
    def _get_hash_indices(self, item):
        """Get all hash indices for an item"""
        # We use different seeds for each hash function
        return [mmh3.hash(item, i) % self.size for i in range(self.hash_count)]
    
    def add(self, item):
        """Add an item to the filter"""
        for index in self._get_hash_indices(str(item)):
            self.bit_array[index] = True
    
    def __contains__(self, item):
        """Check if item is in the filter (may have false positives)"""
        for index in self._get_hash_indices(str(item)):
            if not self.bit_array[index]:
                return False
        return True
    
    def __repr__(self):
        return f"BloomFilter(capacity={self.capacity}, error_rate={self.error_rate})"

# Example usage
if __name__ == "__main__":
    # Create a Bloom filter with capacity for 1000 items and 1% error rate
    bf = BloomFilter(capacity=1000, error_rate=0.01)
    
    # Add some items
    items_to_add = ["apple", "banana", "cherry", "date", "elderberry"]
    for item in items_to_add:
        bf.add(item)
        print(f"Added: {item}")
    
    # Test for items that are in the filter (should return True)
    print("\nTesting items that were added:")
    for item in items_to_add:
        print(f"'{item}' in filter? {item in bf}")
    
    # Test for items that are NOT in the filter (should usually return False)
    test_items = ["fig", "grape", "honeydew", "apple"]  # Note: "apple" is actually present
    print("\nTesting items that were not added:")
    for item in test_items:
        print(f"'{item}' in filter? {item in bf} (False Positive)" if item in bf and item not in items_to_add else item in bf)
    
    # Show filter statistics
    print("\nBloom Filter Statistics:")
    print(f"Capacity: {bf.capacity}")
    print(f"Error Rate: {bf.error_rate:.2%}")
    print(f"Bit Array Size: {bf.size} bits")
    print(f"Hash Functions Used: {bf.hash_count}")