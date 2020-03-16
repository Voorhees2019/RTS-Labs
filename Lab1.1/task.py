import random
import matplotlib.pyplot as plt
import numpy as np
import timeit
# from Google_Drive_API import main

N = 500
dx_lst = []
while N < 1501:
    n = 6
    w = 1700
    # N = 1024
    wp = np.linspace(0, w, n)
    t = np.linspace(0, N - 1, N)
    x = [0 for _ in range(N)]

    for i in range(len(wp)):
        A = random.uniform(0, 1)
        phi = random.uniform(0, 1)
        for j in range(N):
            x[j] += A * np.sin(wp[i] * j + phi)

    # plt.figure(1)
    # plt.subplot(211)
    # plt.plot(t, x)
    # plt.subplot(212)
    # plt.axis([0, 100, min(x), max(x)])
    # plt.plot(t, x)
    # plt.savefig('Lab1_1.png')
    # plt.show()
    mx = 0
    for i in range(N):
        mx += x[i]
    mx /= N
    dx = 0
    for i in range(N):
        dx += ((x[i] - mx) ** 2)
    dx /= N - 1
    dx_lst.append(dx)
    N += 1
print(dx_lst)
plt.plot([i for i in range(500, 1501)], dx_lst)
plt.show()
