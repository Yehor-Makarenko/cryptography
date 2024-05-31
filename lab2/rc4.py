# Key Scheduling Algorithm (KSA)
def ksa(key):    
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

# Pseudo-Random Generation Algorithm (PRGA) 
def prga(S):    
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

# RC4 algorithm 
def rc4(key, data):        
    key = bytearray(key.encode())
    S = ksa(key)
    keystream = prga(S)
    return bytearray([c ^ next(keystream) for c in data])

key = "hh3g4h5g34hg345v3k2"
data = "The quick brown fox jumps over the lazy dog".encode()
encrypted_data = rc4(key, data)
print("Encrypted data:", encrypted_data)

decrypted_data = rc4(key, encrypted_data)
print("Decrypted data:", decrypted_data.decode())
