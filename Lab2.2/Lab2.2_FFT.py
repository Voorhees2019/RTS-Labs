import random
from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np
import math
import timeit
from Google_Drive_API import main

n = 6
w = 1700
N = 1024


def generate_random_signal(n, w, N):
    """The function that generate a random signal and returns a list of xpoints."""
    wp = np.linspace(0, w, n)
    x = [0 for _ in range(N)]
    for i in range(len(wp)):
        A = random.uniform(0, 1)
        phi = random.uniform(0, 1)
        for j in range(N):
            x[j] += A*np.sin(wp[i]*j+phi)
    return x


def draw(x: list, y: list, filename: str, canvas_title1: str, canvas_title2: str):
    t = np.linspace(0, N-1, N)
    plt.figure(1)
    sub = plt.subplot(211)
    sub.set_title(canvas_title1)
    plt.plot(t, x)
    sub2 = plt.subplot(212)
    sub2.set_title(canvas_title2)
    plt.plot(t, y)
    plt.savefig(filename)
    plt.show()


def get_DFT_func(x: list) -> List:
    Freal = [0]*N
    Fimage = [0]*N
    for p in range(N):
        for k in range(N):
            Freal[p] += x[k] * np.cos(2*np.pi/N*p*k)
            Fimage[p] += x[k] * np.sin(2*np.pi/N*p*k)
    Fp = [math.sqrt(r ** 2 + i ** 2) for (r, i) in zip(Freal, Fimage)]

    return Fp


def get_FFT_func(x: list) -> List:
    freal11 = [0 for i in range(int(N / 2))]
    freal12 = [0 for i in range(int(N / 2))]
    freal1 = [0 for i in range(N)]
    fimage11 = [0 for i in range(int(N / 2))]
    fimage12 = [0 for i in range(int(N / 2))]
    fimage1 = [0 for i in range(N)]
    f1 = [0 for i in range(N)]
    for p in range(int(N / 2)):
        for m in range(int(N / 2)):
            freal11[p] += x[2 * m + 1] * np.cos(4 * np.pi / N * p * m)
            fimage11[p] += x[2 * m + 1] * np.sin(4 * np.pi / N * p * m)
            freal12[p] += x[2 * m] * np.cos(4 * np.pi / N * p * m)
            fimage12[p] += x[2 * m] * np.sin(4 * np.pi / N * p * m)
        freal1[p] = freal12[p] + freal11[p] * np.cos(2 * np.pi / N * p) - fimage11[p] * np.sin(
            2 * np.pi / N * p)
        fimage1[p] = fimage12[p] + fimage11[p] * np.cos(2 * np.pi / N * p) + freal11[p] * np.sin(
            2 * np.pi / N * p)
        freal1[p + int(N / 2)] = freal12[p] - (
                    freal11[p] * np.cos(2 * np.pi / N * p) - fimage11[p] * np.sin(2 * np.pi / N * p))
        fimage1[p + int(N / 2)] = fimage12[p] - (
                    fimage11[p] * np.cos(2 * np.pi / N * p) + freal11[p] * np.sin(2 * np.pi / N * p))
        f1[p] = (freal1[p] ** 2 + fimage1[p] ** 2) ** 0.5
        f1[p + int(N / 2)] = (freal1[p + int(N / 2)] ** 2 + fimage1[p + int(N / 2)] ** 2) ** 0.5
    return f1


x = generate_random_signal(n, w, N)
start_time = timeit.default_timer()
fp = get_DFT_func(x)
print(f'Time of calculating DFT function: {timeit.default_timer() - start_time}')
start_time = timeit.default_timer()
fp2 = get_FFT_func(x)
print(f'Time of calculating FFT function: {timeit.default_timer() - start_time}')
print(f'x: {x}')
print(f'Fp: {fp}')
print(f'Fp2: {fp2}')
draw(fp, fp2, 'F(p).png', 'DFT', 'FFT')


# with open('calculation.txt', 'w+') as file:
#     file.write(f'Time of calculating Rxx: {trx} seconds\n'
#                f'Time of calculating Rxy: {trxy} seconds\n')

with open('file_ids.txt', 'r+') as file_ids:
    lines = file_ids.readlines()
    # check if the file is not empty
    if lines:
        file_ids.seek(0)
        lines = list(map(lambda x: x.strip(), lines))
        for i in range(len(lines)):
            main.delete_file(lines[i])
        # main.delete_file(f'{file_ids.readline()}')
        with open('file_ids.txt', 'r+') as file_ids:
            file_ids.write(main.insert_file_in_folder('F(p).png',
                                                      'F(p).png', 'image/png',
                                                      '1C5_WOktf4-RrdE8AL_3DAmixWRSxiQL8') + '\n')
            # file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
            #                                           '') + '\n')

    else:
        file_ids.write(main.insert_file_in_folder('F(p).png',
                                                  'F(p).png', 'image/png',
                                                  '1C5_WOktf4-RrdE8AL_3DAmixWRSxiQL8') + '\n')
        # file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
        #                                           '') + '\n')


