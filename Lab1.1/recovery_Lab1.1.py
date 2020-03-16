import random
import matplotlib.pyplot as plt
import numpy as np
import timeit
import os
from Google_Drive_API import main

n = 6
w = 1700
N = 1024
wp = np.linspace(0, w, n)
# print(wp)
t = np.linspace(0, N-1, N)
# print(t)
matrix = [[0 for j in range(N)] for i in range(len(wp))]

for i in range(len(wp)):
    A = random.randint(0, 100)
    phi = random.randint(1, 360)
    for j in range(len(matrix[i])):
        matrix[i][j] = A*np.sin(np.deg2rad(wp[i]*j+phi))

# print('--------------------------')
# for i in matrix:
#     print(i)
# print('--------------------------')
# lst = [A*np.sin(np.deg2rad(w*t+phi)) for t in range(0, N)]
# print(lst)
av_sin = []
for j in range(len(matrix[0])):
    s = 0
    for i in range(len(matrix)):
        s += matrix[i][j]
    av_sin.append(s)
    # print(s, end=' | ')
print()

plt.figure(1)
plt.subplot(211)
plt.plot(t, av_sin)
plt.subplot(212)
plt.axis([0, 100, min(av_sin), max(av_sin)])
plt.plot(t, av_sin)
plt.savefig('Lab1_1.png')
plt.show()

start_time = timeit.default_timer()
expected_value = sum(av_sin)/N
tm = timeit.default_timer() - start_time
print(f'Time of calculating the expected value: {tm} seconds')
print(f'Expected value = {expected_value}')
start_time = timeit.default_timer()
variance = sum(list(map(lambda x: ((x - expected_value) ** 2)/(N - 1), av_sin)))
td = timeit.default_timer() - start_time
print(f'Time of calculating the variance: {td} seconds')
print(f'Variance = {variance}')
# s = 0
# for i in range(len(av_sin)):
#     s += ((av_sin[i] - expected_value) ** 2)/(N-1)
# print(s)
with open('calculation.txt', 'w+') as file:
    file.write(f'An expected value = {expected_value}\n'
               f'The variance = {variance}\n'
               f'Time of calculating the expected value: {tm} seconds\n'
               f'Time of calculating the variance: {td} seconds\n')

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
            file_ids.write(main.insert_file_in_folder('Lab1_1.png', 'Lab1_1.png', 'image/png',
                                                      '1teH5nCBvd3rDFmqwcPEeyRxFs0XH_Tc0') + '\n')
            file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
                                                      '1teH5nCBvd3rDFmqwcPEeyRxFs0XH_Tc0') + '\n')
    else:
        file_ids.write(main.insert_file_in_folder('Lab1_1.png', 'Lab1_1.png', 'image/png',
                                                  '1teH5nCBvd3rDFmqwcPEeyRxFs0XH_Tc0') + '\n')
        file_ids.write(main.insert_file_in_folder('calculation.txt', 'calculation.txt', 'text/plain',
                                                  '1teH5nCBvd3rDFmqwcPEeyRxFs0XH_Tc0') + '\n')



