import random
import matplotlib.pyplot as plt
import numpy as np
import timeit

n = 6
w = 1700
N = 10240


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


def draw(x: list, filename: str, title: str):
    t = np.linspace(0, N-1, N)
    plt.figure(1)
    sub = plt.subplot(211)
    sub.set_title(title)
    if len(x) != len(t):
        plt.plot(t[:len(t)//2], x)
    else:
        plt.plot(t, x)
    plt.subplot(212)
    plt.axis([0, 100, min(x), max(x)])
    if len(x) != len(t):
        plt.plot(t[:len(t) // 2], x)
    else:
        plt.plot(t, x)
    plt.savefig(filename)
    plt.show()


def get_expected_value(x: list):
    expected_value = 0
    for i in range(N):
        expected_value += x[i]
    return expected_value/N


def get_variance(x: list, expected_value: float):
    variance = 0
    for i in range(N):
        variance += ((x[i] - expected_value) ** 2)
    return variance/(N-1)


def get_correlation(x: list, mx: float, y: list=None, my: float=None):
    correlation = [0 for _ in range(int(N/2))]
    if y:
        for i in range(int(N/2)):
            for j in range(int(N/2)):
                correlation[i] += (x[i] - mx)*(y[i+j] - my)/(N-1)
    else:
        for i in range(int(N/2)):
            for j in range(int(N/2)):
                correlation[i] += (x[i] - mx)*(x[i+j] - mx)/(N-1)
    return correlation


start_time = timeit.default_timer()
x = generate_random_signal(n, w, N)
y = generate_random_signal(n, w, N)
mx = get_expected_value(x)
my = get_expected_value(y)
get_correlation(x, mx, y, my)
tx = timeit.default_timer() - start_time
print(f'Time of calculating Rxy : {tx} seconds')

start_time = timeit.default_timer()
z = generate_random_signal(n, w, N)
mz = get_expected_value(z)
get_correlation(z, mz, z, mz)
tz = timeit.default_timer() - start_time
print(f'Time of calculating Rzz : {tz} seconds')
