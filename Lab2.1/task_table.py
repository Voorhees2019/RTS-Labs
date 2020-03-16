import random
import matplotlib.pyplot as plt
import numpy as np
import math
import timeit

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


def draw(x: list, canvas_title: str):
    t = np.linspace(0, N-1, N)
    plt.figure(1)
    sub = plt.subplot(111)
    sub.set_title(canvas_title)
    plt.plot(t, x)
    plt.show()


def get_DFT_func(x: list):
    Freal = [0]*N
    Fimage = [0]*N
    for p in range(N):
        for k in range(N):
            Freal[p] += x[k] * np.cos(2*np.pi/N*p*k)
            Fimage[p] += x[k] * np.sin(2*np.pi/N*p*k)
    Fp = [math.sqrt(r ** 2 + i ** 2) for (r, i) in zip(Freal, Fimage)]
    return Fp


def get_DFT_with_w_table(p: int, k: int) -> list:
    w_table_real = [[None for _ in range(k)] for _ in range(p)]
    w_table_image = [[None for _ in range(k)] for _ in range(p)]
    Fp2_real = [0] * 1024
    Fp2_image = [0] * 1024
    for i in range(p):
        for j in range(k):
            w_table_real[i][j] = np.cos(2*np.pi/N*i*j)
            w_table_image[i][j] = np.sin(2*np.pi/N*i*j)

    for i in range(len(w_table_real)):
        for j in range(len(w_table_real[i])):
            Fp2_real[i] += x[j] * w_table_real[i][j]
            Fp2_image[i] += x[j] * w_table_image[i][j]

    Fp2 = [math.sqrt(r ** 2 + i ** 2) for (r, i) in zip(Fp2_real, Fp2_image)]
    return Fp2


x = generate_random_signal(n, w, N)
start_time = timeit.default_timer()
Fp = get_DFT_func(x)
print(f'Time of calculating Fp: {timeit.default_timer() - start_time}')
start_time = timeit.default_timer()
Fp2 = get_DFT_with_w_table(N, N)
print(f'Time of calculating Fp2: {timeit.default_timer() - start_time}')
draw(Fp, 'F(p)')
draw(Fp2, 'F2(p)')

