magic = "metahider".encode()
import zlib

def xor_encrypt_decrypt(data, key):
    key_length = len(key)
    key_as_int = list(key)
    data_as_int = list(data)
    result = bytearray()
    
    for i in range(len(data_as_int)):
        result.append(data_as_int[i] ^ key_as_int[i % key_length])
    
    return result
