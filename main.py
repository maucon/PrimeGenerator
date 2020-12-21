from time import time

from numba import cuda, njit
import numpy as np


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


start = 41000000000  # todo automate
offset = 1000000000

print('Loading primes...')
loading_primes_time = time()
small_primes = np.delete(np.loadtxt('data/0-1000000000.txt', delimiter='\n', dtype=np.int32), 0)
print('INIT VALUES:', time() - loading_primes_time, end='\n\n')

for calc_round in range(1, 101):
    print('ROUND ', calc_round)
    print('--------------------------------')
    sieve = np.zeros(offset, dtype=np.bool)

    start_time = time()
    part_time = start_time

    calculate_sieve[256, 64](start, offset, sieve, small_primes)
    print('CALC PRIMES:', time() - part_time)

    part_time = time()
    final_primes = get_primes(start, sieve)
    print('READ PRIMES:', time() - part_time)

    part_time = time()
    with open('data/%s-%s.txt' % (start, start + offset), 'w+') as file:
        file.write('\n'.join(map(str, final_primes)))  # maybe chunk it to reduce ram spikes
    print('SAVING TXT :', time() - part_time)

    print('--------------------------------')
    print('ROUND TIME :', time() - start_time, end='\n\n')

    start += offset
