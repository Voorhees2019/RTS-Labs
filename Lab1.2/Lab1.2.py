import random
import matplotlib.pyplot as plt
import numpy as np
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


x = generate_random_signal(n, w, N)
y = generate_random_signal(n, w, N)
mx = get_expected_value(x)
my = get_expected_value(y)
print(f'Mx = {mx}')
print(f'My = {my}')
# dx = get_variance(x, mx)
# dy = get_variance(y, my)
# print(f'Dx = {dx}')
# print(f'Dy = {dy}')
draw(x, 'first_random_signal.png', 'first random signal')
draw(y, 'second_random_signal.png', 'second random signal')

start_time = timeit.default_timer()
draw(get_correlation(x, mx), 'colleration_function_for_X.png', 'colleration function for X')
trx = timeit.default_timer() - start_time
print(f'Time of calculating Rxx : {trx} seconds')

start_time = timeit.default_timer()
draw(get_correlation(x, mx, y, my), 'colleration_function_for_both_X&Y.png', 'colleration function for both X and Y')
trxy = timeit.default_timer() - start_time
print(f'Time of calculating Rxy : {trxy} seconds')


with open('calculation.txt', 'w+') as file:
    file.write(f'Time of calculating Rxx: {trx} seconds\n'
               f'Time of calculating Rxy: {trxy} seconds\n')

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
            file_ids.write(main.insert_file_in_folder('colleration_function_for_X.png',
                                                      'colleration_function_for_X.png', 'image/png',
                                                      '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')
            file_ids.write(main.insert_file_in_folder('colleration_function_for_both_X&Y.png',
                                                      'colleration_function_for_both_X&Y.png', 'image/png',
                                                      '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')
            file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
                                                      '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')

    else:
        file_ids.write(main.insert_file_in_folder('colleration_function_for_X.png',
                                                  'colleration_function_for_X.png', 'image/png',
                                                  '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')
        file_ids.write(main.insert_file_in_folder('colleration_function_for_both_X&Y.png',
                                                  'colleration_function_for_both_X&Y.png', 'image/png',
                                                  '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')
        file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
                                                  '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')


