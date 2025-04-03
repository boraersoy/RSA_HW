import sympy
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def choose_encryptor(phi):
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            return e
    raise ValueError(f"No valid 'e' found. phi: {phi}")

def mod_inverse_euclidean(e, phi):
    m0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_rsa_keys(bit_size):
    low = 2**(bit_size - 1)
    high = 2**bit_size
    p = sympy.randprime(3 if low < 3 else low, high)
    q = sympy.randprime(3 if low < 3 else low, high)
    N = p * q
    phi = (p - 1) * (q - 1)
    e = choose_encryptor(phi)
    d = mod_inverse_euclidean(e, phi)
    return (N, e), (N, d), (p, q)

def encrypt(message, e, N):
    m = int.from_bytes(message.encode(), 'big')
    if m >= N:
        raise ValueError(f"Message is too large for this modulus. m: {m}, N: {N}")
    return pow(m, e, N)

def decrypt(c, d, N):
    m = pow(c, d, N)
    try:
        return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
    except UnicodeDecodeError:
        return f"Decryption failed. Raw number: {m}"

if "__main__" == __name__:
    bit_sizes = [2, 4, 8, 16, 32]
    message = "ab"

    for bit_size in bit_sizes:
        print(f"\n{bit_size}-bit RSA Key Generation:")
        public_key, private_key, primes = generate_rsa_keys(bit_size)
        N, e = public_key
        _, d = private_key

        try:
            print(f"Original: {message}")
            c = encrypt(message, e, N)
            print(f"Encrypted: {c}")
            decrypted_message = decrypt(c, d, N)
            print(f"Decrypted: {decrypted_message}")
        except ValueError as err:
            print(f"Error: {err}")

        print(f"Public Key: {public_key}")
        print(f"Private Key: {private_key}")
        print(f"Primes: p={primes[0]}, q={primes[1]}")
