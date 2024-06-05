import math
from sympy import randprime, gcd, mod_inverse
import os
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_prime_number(length=1024):
    return randprime(2**(length - 1), 2**length)

def generate_rsa_keys(length=1024):
    p1 = generate_prime_number(length)
    p2 = generate_prime_number(length)
    N = p1 * p2
    phi = (p1 - 1) * (p2 - 1)

    e = 65537
    if gcd(e, phi) != 1:
        for i in range(2, phi):
            if gcd(i, phi) == 1:
                e = i
                break

    d = mod_inverse(e, phi)

    public_key = (e, N)
    private_key = (d, N)

    return public_key, private_key

def convert_to_pem(public_key, private_key):
    e, N = public_key
    d, _ = private_key
    
    public_key_pem = RSA.construct((N, e)).export_key()
    
    private_key_pem = RSA.construct((N, e, d)).export_key()
    
    return public_key_pem, private_key_pem

def ecb_encrypt(data, public_key, block_size):
    e, N = public_key
    encrypted_blocks = []

    for i in range(0, len(data), block_size):
        block = int.from_bytes(data[i:i+block_size], byteorder='big')
        encrypted_block = pow(block, e, N)
        encrypted_blocks.append(encrypted_block)

    return encrypted_blocks

def ecb_decrypt(encrypted_blocks, private_key, block_size):
    d, N = private_key
    decrypted_data = bytearray()

    for block in encrypted_blocks:
        decrypted_block = pow(block, d, N)
        decrypted_data.extend(decrypted_block.to_bytes(block_size, byteorder='big'))

    return decrypted_data

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def cbc_encrypt(data, public_key, block_size, prev_block):
    e, N = public_key
    encrypted_blocks = []
    previous_block = prev_block

    padding_len = (block_size-11) - len(data) % (block_size-11)
    data = data + bytes([padding_len] * padding_len)

    for i in range(0, len(data), block_size - 11):
        block = data[i:i + block_size - 11]
        block = int.from_bytes(xor_bytes(block, previous_block), byteorder='big')
        encrypted_block = pow(block, e, N)
        encrypted_block_bytes = encrypted_block.to_bytes((N.bit_length() + 7) // 8, byteorder='big')
        encrypted_blocks.append(encrypted_block_bytes)
        previous_block = encrypted_block_bytes

    return b''.join(encrypted_blocks)

def cbc_decrypt(encrypted_data, private_key, block_size, prev_block):
    d, N = private_key
    decrypted_data = bytearray()
    previous_block = prev_block

    for i in range(0, len(encrypted_data), (N.bit_length() + 7) // 8):
        block = encrypted_data[i:i + (N.bit_length() + 7) // 8]
        encrypted_block = int.from_bytes(block, byteorder='big')
        decrypted_block = pow(encrypted_block, d, N)
        decrypted_block_bytes = decrypted_block.to_bytes(block_size - 11, byteorder='big')
        decrypted_data.extend(xor_bytes(decrypted_block_bytes, previous_block))
        previous_block = block

    padding_len = decrypted_data[-1]
    return decrypted_data[:-padding_len]

def library_encrypt(data, public_key):
    e, N = public_key
    rsa_key = RSA.construct((N, e))
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def library_decrypt(encrypted_data, public_key, private_key):
    e, N = public_key
    d, N = private_key
    rsa_key = RSA.construct((N, e, d))
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data