from numba import cuda, njit


@cuda.jit
def calculate_sieve(start, offset, sieve, primes):
    index = (cuda.blockIdx.x * cuda.blockDim.x) + cuda.threadIdx.x
    if index > len(primes) - 1:
        return
    prime = primes[index]
    if prime ** 2 > start + offset:
        return
    start_offset = prime - start % prime
    if start_offset % 2 == 0:
        start_offset += prime
    for n in range(start_offset, offset, prime * 2):
        sieve[n] = 1


@njit
def get_primes(offset, sieve):
    primes = []
    for i in range(1, len(sieve), 2):
        if not sieve[i]:
            primes.append(i + offset)
    return primes
