# MECE 603 - Assignment 4
# Nargiz Azat ID No: 202443650


import heapq
from collections import Counter

# part 1 where we will get a frequency of each character
def freq_by_char(file):
    with open(file, 'r') as file:
        text = file.read()
    freq = Counter(text.strip())
    return freq

# subpart b, to get a fixed length for characters
def fixed_length(freq):
    # get a number of unique characters
    count = len(freq)
    # to get how many bits are needed for char
    bits_per_char = (count - 1).bit_length() # "-1" because the numeration starts with 0
    codes = {}
    # goes through all chars and gives binary code
    for i, char in enumerate(sorted(freq.keys())):
        codes[char] = format(i, f'0{bits_per_char}b')
    return codes

# part 2 && subpart d:
# nodes implemented in a huffman tree
class HuffmanNode:
    def __init__(self, char=None, freq=0): # initialization of the node
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other): # defining the order of nodes according to freq
        return self.freq < other.freq

# Implementing pseudocode
def huffman_tree(freq):
    # q = c
    queue = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(queue) # sort the nodes by their freq
    # for i from 1 to n-1
    while len(queue) > 1:
        # get the two nodes with the smallest freq
        x = heapq.heappop(queue)
        y = heapq.heappop(queue)

        # get the new node z with the freq x+y
        z = HuffmanNode(freq = x.freq + y.freq)
        # x && y become its children
        z.left = x
        z.right = y

        heapq.heappush(queue, z)
    return queue[0] # after the loop there will be only one node which is the root

# now generate new codes according to their order in the tree
def generate_huffman_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

# to find a size of the file after compression
def calculate_size(freq, codes): # the function will use freq and their Haffman codes
    # the length of the code for each char * their freq, then all of them will be summarized
    return sum(len(codes[char]) * freq for char, freq in freq.items()) # freq.items() => gives (char, freq)

def main(file):
    # part 1
    print(" All the characters from the input.txt by their frequency: ")
    frequencies = freq_by_char(file)
    for char, freq in sorted(frequencies.items()):
        print(f"'{char}': {freq}", end = " ")

    # subpart a
    # then we need to summarize all frequencies together and mult by 8 to get the total number of bits
    actual_size = sum(frequencies.values()) * 8
    print(f"\n Actual number of bits needed to save the file : {actual_size} bits")

    # subpart b
    # using the func fixed_length
    print(" All the characters with their fixed-length codes: ")
    fixed = fixed_length(frequencies)
    for char, code in fixed.items():
        print(f"    '{char}': {code}", end=" ")

    # subpart c
    # the size of the compressed file with fixed-length
    fixed_size = calculate_size(frequencies, fixed)
    print(f"\n The size of the new compressed file with fixed-length coding: {fixed_size} bits")

    # subpart d
    print("\n All the characters with their variable-length codes:")
    root = huffman_tree(frequencies)
    variable = generate_huffman_codes(root)
    for char, code in variable.items():
        print(f"    '{char}': {code}", end = " ")

    # subpart e
    # the size of the compressed file with variable-length + using the same func as for fixed
    variable_size = calculate_size(frequencies, variable)
    print(f"\n The size of the new compressed file with variable-length coding: {variable_size} бит")

main('input.txt')