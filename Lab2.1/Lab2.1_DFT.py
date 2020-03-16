import random
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


def draw(x: list, filename: str, canvas_title: str):
    t = np.linspace(0, N-1, N)
    plt.figure(1)
    sub = plt.subplot(111)
    sub.set_title(canvas_title)
    plt.plot(t, x)
    plt.savefig(filename)
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


x = generate_random_signal(n, w, N)
start_time = timeit.default_timer()
Fp = get_DFT_func(x)
print(f'Time of calculating Fp: {timeit.default_timer() - start_time}')
draw(Fp, 'F(p).png', 'F(p)')


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
                                                      '1CI01IUqxgmwT3Vgb3XYwVq4Mp-q3EgxG') + '\n')
            # file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
            #                                           '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')

    else:
        file_ids.write(main.insert_file_in_folder('F(p).png',
                                                  'F(p).png', 'image/png',
                                                  '1CI01IUqxgmwT3Vgb3XYwVq4Mp-q3EgxG') + '\n')
        # file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
        #                                           '1bNyCESOlyaXhH-dyopEWHbKikCtLwzB-') + '\n')


