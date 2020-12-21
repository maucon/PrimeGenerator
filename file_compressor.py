from os import remove

import numpy as np


def compress_prime_file(filepath, step_size, calculation_offset):
    with open(filepath + '.prime', 'r') as file:
        primes = np.array(list(map(int, file.readlines())))

    grouped, index, step = [], 0, 1
    while step * step_size <= calculation_offset:
        last_prime, stepper, group = 0, step * step_size, []
        while index < len(primes) and primes[index] < stepper:
            group.append(str(primes[index] - (step - 1) * step_size if len(group) == 0
                             else (primes[index] - last_prime) // 2))
            last_prime = primes[index]
            index += 1
        grouped.append(' '.join(group))
        step += 1

    with open(filepath + '.cprime', 'w+') as file:
        file.write('\n'.join(grouped))

    remove(filepath + '.prime')


def read_compressed_prime_file(filepath, step_size):
    primes = []
    line_count = 0
    with open(filepath + '.cprime', 'r') as file:
        for line in file.readlines():
            line = line.split(' ')
            primes.append(int(line[0]) + line_count * step_size)
            for index in range(1, len(line)):
                inc = int(line[index])
                inc = inc * 2 if inc != 0 else 1  # can only happen in first file first line because of the number 2
                primes.append(primes[-1] + inc)
            line_count += 1
    return np.array(primes)
