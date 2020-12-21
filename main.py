from glob import glob
from time import time

import numpy as np

from prime_generator import calculate_sieve, get_primes

loading_primes_time = time()
blocks, block_size = 256, 64
offset = 1000000000
print('Calculating start point...')
start = max(map(lambda path: int(path.split('-')[1].split('.')[0]), glob('data/*.txt')))
print('Loading primes...')
with open('data/0-1000000000.txt', 'r') as file:
    small_primes = np.array(list(map(int, file.readlines()[1:])))
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
    with open('data/%s-%s.txt' % (start, start + offset), 'w+') as file:
        file.write('\n'.join(map(str, final_primes)))  # maybe chunk it to reduce ram spikes
    print('SAVING TXT :', time() - part_time)

    print('--------------------------------\nROUND TIME : %s' % (time() - start_time), end='\n\n')
    start += offset
