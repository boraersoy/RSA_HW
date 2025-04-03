import time
import math
import matplotlib.pyplot as plt
from statistics import mean
from RSA_hw import generate_rsa_keys, encrypt, decrypt, mod_inverse_euclidean

def brute_force_rsa(N, e, encrypted_message):
    start_time = time.perf_counter() 
    for p in range(2, int(math.sqrt(N)) + 1):
        if N % p == 0:
            q = N // p
            phi = (p - 1) * (q - 1)
            try:
                d = mod_inverse_euclidean(e, phi)
                decrypted = decrypt(encrypted_message, d, N)
                return True, time.perf_counter() - start_time 
            except:
                continue
    return False, time.perf_counter() - start_time

def measure_brute_force_time(bit_size, num_runs=5):
    message = "ab"
    times = []
    
    for _ in range(num_runs):
        public_key, private_key, _ = generate_rsa_keys(bit_size)
        N, e = public_key
        encrypted = encrypt(message, e, N)
        success, elapsed_time = brute_force_rsa(N, e, encrypted)
        if success:
            times.append(elapsed_time)
    
    return mean(times) if times else None

def main():
    bit_sizes = [2, 4, 8, 16, 32]  # Added larger bit sizes
    times = []
    successful_sizes = []

    print("System Specifications:")
    print("- CPU: Apple M2 Pro")
    print("- RAM: 16GB")
    print("\nMeasuring brute force times...")

    for bit_size in bit_sizes:
        print(f"\nTesting {bit_size}-bit RSA...")
        avg_time = None
        try:
            avg_time = measure_brute_force_time(bit_size)
        except ValueError as err:
            print(err)
            print("Continuing to next bit size")
            
        if avg_time is not None:
            times.append(avg_time)
            successful_sizes.append(bit_size)
            print(f"Average time: {avg_time:.6f} seconds")
        else:
            print(f"Brute force took too long or failed for {bit_size}-bit key")

    plt.figure(figsize=(10, 6))
    plt.plot(successful_sizes, times, 'bo-')
    plt.xlabel('Key Size (bits)')
    plt.ylabel('Time (seconds)')
    plt.title('RSA Brute Force Time vs Key Size\nSystem: M2 Pro, 16GB RAM')
    plt.grid(True)
    plt.yscale('log')
    plt.savefig('rsa_brute_force_times.png')
    plt.close()

    print("\nPlot saved as 'rsa_brute_force_times.png'")

if __name__ == "__main__":
    main()
