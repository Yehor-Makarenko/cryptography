import math

# Constants
T = [int(2**32 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
s = [
    7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
]

# Round funcs
F = lambda x, y, z: (x & y) | (~x & z)
G = lambda x, y, z: (x & z) | (y & ~z)
H = lambda x, y, z: x ^ y ^ z
I = lambda x, y, z: y ^ (x | ~z)

rotate_left = lambda x, n: (x << n | x >> (32 - n)) & 0xFFFFFFFF

# Initialize variables
a0 = 0x67452301
b0 = 0xEFCDAB89
c0 = 0x98BADCFE
d0 = 0x10325476

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='little')

def int_to_bytes(n, length):
    return n.to_bytes(length, byteorder='little')

# Pre-processing
def md5_padding(message):
    message = bytearray(message)
    orig_len_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message.append(0x80)
    
    while len(message) % 64 != 56:
        message.append(0)
    
    message += orig_len_bits.to_bytes(8, byteorder='little')
    return message

# md5 func
def md5(message):
    message = md5_padding(message)
    
    A, B, C, D = a0, b0, c0, d0
    
    # Process the message in successive 512-bit chunks
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        M = [bytes_to_int(chunk[j:j+4]) for j in range(0, 64, 4)]
        
        AA, BB, CC, DD = A, B, C, D
        
        # Main loop
        for j in range(64):
            if 0 <= j <= 15:
                F_val = F(B, C, D)
                g = j
            elif 16 <= j <= 31:
                F_val = G(B, C, D)
                g = (5 * j + 1) % 16
            elif 32 <= j <= 47:
                F_val = H(B, C, D)
                g = (3 * j + 5) % 16
            elif 48 <= j <= 63:
                F_val = I(B, C, D)
                g = (7 * j) % 16
            
            temp = (A + F_val + T[j] + M[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + rotate_left(temp, s[j])) & 0xFFFFFFFF
        
        # Add this chunk's hash to result so far
        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF
    
    # Result
    result = int_to_bytes(A, 4) + int_to_bytes(B, 4) + int_to_bytes(C, 4) + int_to_bytes(D, 4)
    return result.hex()


message = "The quick brown fox jumps over the lazy dog"
hash_result = md5(message.encode())
print(f"MD5 хеш: {hash_result}")