from glob import glob
from time import time

import numpy as np

from prime_generator import calculate_sieve, get_primes

start = max(map(lambda path: int(path.split('-')[1].split('.')[0]), glob('data/*.txt')))
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
