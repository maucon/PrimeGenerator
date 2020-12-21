from glob import glob
from time import time

import numpy as np

from file_compressor import read_compressed_prime_file, save_and_compress_prime_file
from prime_generator import calculate_sieve, get_primes

loading_primes_time = time()
blocks, block_size = 256, 64
offset = 1000000000
step_size = 10000
print('Calculating start point...')
start = max(map(lambda path: int(path.split('-')[1].split('.')[0]), glob('../data/*.*prime')))
print('Loading primes...')
small_primes = read_compressed_prime_file('../data/0-1000000000', step_size)[1:]
print('INIT VALUES:', time() - loading_primes_time, end='\n\n')

for calc_round in range(1, 101):
    print('ROUND %s\n--------------------------------' % calc_round)
    start_time = time()

    part_time = start_time
    sieve = np.zeros(offset, dtype=np.bool)
    calculate_sieve[blocks, block_size](start, offset, sieve, small_primes)
    print('CALC PRIMES:', time() - part_time)

    part_time = time()
    final_primes = get_primes(start, sieve)
    print('READ PRIMES:', time() - part_time)

    part_time = time()
    # save_prime_file(start, offset, final_primes)
    save_and_compress_prime_file(start, offset, step_size, final_primes)
    print('SAVING FILE:', time() - part_time)

    print('--------------------------------\nROUND TIME : %s' % (time() - start_time), end='\n\n')
    start += offset
