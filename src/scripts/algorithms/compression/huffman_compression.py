import heapq
from collections import defaultdict

class TreeNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char    # Character (leaf nodes only)
        self.freq = freq    # Frequency of the character
        self.left = left    # Left child
        self.right = right  # Right child
    
    # For heap comparison (priority queue)
    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1
    return freq

def build_huffman_tree(freq_dict):
    heap = []
    # Push all leaf nodes into the min-heap
    for char, freq in freq_dict.items():
        heapq.heappush(heap, TreeNode(char=char, freq=freq))
    
    # Merge nodes until only one remains (the root)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = TreeNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    return heapq.heappop(heap)  # Root of the Huffman tree

def generate_codes(root, current_code="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if root is None:
        return
    if root.char is not None:  # Leaf node
        code_dict[root.char] = current_code
        return
    generate_codes(root.left, current_code + "0", code_dict)
    generate_codes(root.right, current_code + "1", code_dict)
    return code_dict

def encode(text, code_dict):
    encoded_text = ""
    for char in text:
        encoded_text += code_dict[char]
    return encoded_text

def decode(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.char is not None:  # Reached a leaf
            decoded_text += current_node.char
            current_node = root  # Reset to root for next character
    return decoded_text

# Example Usage
if __name__ == "__main__":
    text = "ABRACADABRA"
    print(f"Original Text: {text}")

    # Step 1: Build frequency dictionary
    freq_dict = build_frequency_dict(text)
    print("Frequency Dictionary:", freq_dict)

    # Step 2: Build Huffman tree
    huffman_tree = build_huffman_tree(freq_dict)

    # Step 3: Generate Huffman codes
    huffman_codes = generate_codes(huffman_tree)
    print("Huffman Codes:", huffman_codes)

    # Step 4: Encode the text
    encoded_text = encode(text, huffman_codes)
    print(f"Encoded Text: {encoded_text} (Length: {len(encoded_text)} bits)")

    # Step 5: Decode the text
    decoded_text = decode(encoded_text, huffman_tree)
    print(f"Decoded Text: {decoded_text}")

    # Compression ratio (vs. 8-bit ASCII)
    original_bits = len(text) * 8
    compressed_bits = len(encoded_text)
    print(f"Compression Ratio: {compressed_bits / original_bits * 100:.2f}%")