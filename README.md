## CompressionAlgorithm_Python_Flask
It takes Decompressed words as input and return a Compressed file as output by Calling encode(). 
When it is given Compressed words file as input, it calls decode() and returns decompressed file of words.

## Logic:
The algorithm works on the principle of encoding words by:

1. Finding the prefix that exactly exists in the previous word.

2. Counting it's length

3. Writing the length and then the remaining word.

4. The file is decoded on the basis of this prefix length.
