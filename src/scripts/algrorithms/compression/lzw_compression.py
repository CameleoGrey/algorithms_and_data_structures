def compress(data):
    """
    Compress data using LZW (Lempel-Ziv-Welch (LZW) compression algorithm) algorithm.
    
    Args:
        data: String to be compressed
        
    Returns:
        List of compressed codes
    """
    # Initialize dictionary with all possible single characters
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256  # Next available dictionary code
    w = ""           # Current sequence
    result = []      # Compressed output
    
    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            # Output the code for w
            result.append(dictionary[w])
            # Add wc to the dictionary
            dictionary[wc] = next_code
            next_code += 1
            w = c
    
    # Output the code for remaining w
    if w:
        result.append(dictionary[w])
    
    return result

def decompress(compressed_data):
    """
    Decompress LZW compressed data back to original string.
    
    Args:
        compressed_data: List of compressed codes
        
    Returns:
        Decompressed string
    """
    # Initialize dictionary with all possible single characters
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256  # Next available dictionary code
    result = []      # Decompressed output
    
    # First code is always known
    w = chr(compressed_data[0])
    result.append(w)
    
    for code in compressed_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = w + w[0]
        else:
            raise ValueError("Bad compressed code: %d" % code)
        
        result.append(entry)
        
        # Add w + entry[0] to the dictionary
        dictionary[next_code] = w + entry[0]
        next_code += 1
        
        w = entry
    
    return ''.join(result)

# translation of code from Sedgewick's book (Algorithms in Java)
class LZW:
    R = 256  # number of input chars
    L = 4096  # number of codewords = 2^12
    W = 12    # codeword width

    @staticmethod
    def compress(input_str):
        """Compress input string using LZW algorithm"""
        st = {chr(i): i for i in range(LZW.R)}
        code = LZW.R + 1  # R is codeword for EOF
        output = []
        
        while input_str:
            # Find longest prefix match
            s = ''
            for i in range(1, len(input_str)+1):
                if input_str[:i] in st:
                    s = input_str[:i]
                else:
                    break
            
            # Write s's encoding
            output.append(st[s])
            
            # Add new code to symbol table if possible
            t = len(s)
            if t < len(input_str) and code < LZW.L:
                st[input_str[:t+1]] = code
                code += 1
            
            # Move past s in input
            input_str = input_str[t:]
        
        output.append(LZW.R)  # Write EOF
        return output

    @staticmethod
    def expand(compressed_data):
        """Expand compressed data back to original string"""
        st = [""] * LZW.L
        for i in range(LZW.R):
            st[i] = chr(i)
        st[LZW.R] = " "  # unused lookahead for EOF
        
        val = st[compressed_data[0]]
        result = [val]
        i = LZW.R + 1
        
        for codeword in compressed_data[1:]:
            if codeword == LZW.R:
                break
            
            # Get next codeword
            if codeword < len(st):
                s = st[codeword]
            else:
                s = val + val[0]  # Handle special case
            
            result.append(s)
            
            # Add new entry to code table
            if i < LZW.L:
                st[i] = val + s[0]
                i += 1
            
            val = s
        
        return ''.join(result)

# Example usage
if __name__ == "__main__":
    # Original data
    original_data = "TOBEORNOTTOBEORTOBEORNOT"
    print("Original data:", original_data)
    print("Original size (bytes):", len(original_data))
    

    # Compress
    #compressed = LZW.compress(original_data)
    #print("Compressed codes:", compressed)

    # Compress the data
    compressed = compress(original_data)
    print("\nCompressed codes:", compressed)
    print("Compressed size (assuming 16-bit codes):", len(compressed) * 2)

    # Decompress
    #decompressed = LZW.expand(compressed)
    #print("Decompressed:", decompressed)
    
    # Decompress the data
    decompressed = decompress(compressed)
    print("\nDecompressed data:", decompressed)
    
    # Verify correctness
    print("\nCompression successful?", original_data == decompressed)