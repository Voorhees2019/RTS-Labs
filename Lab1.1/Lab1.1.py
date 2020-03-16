import random
import matplotlib.pyplot as plt
import numpy as np
import timeit
from Google_Drive_API import main

n = 6
w = 1700
N = 1024
wp = np.linspace(0, w, n)
t = np.linspace(0, N-1, N)
x = [0 for _ in range(N)]

for i in range(len(wp)):
    A = random.uniform(0, 1)
    phi = random.uniform(0, 1)
    for j in range(N):
        x[j] += A*np.sin(wp[i]*j+phi)


plt.figure(1)
plt.subplot(211)
plt.plot(t, x)
plt.subplot(212)
plt.axis([0, 100, min(x), max(x)])
plt.plot(t, x)
plt.savefig('Lab1_1.png')
plt.show()

start_time = timeit.default_timer()
mx = 0
for i in range(N):
    mx += x[i]
mx /= N
tm = timeit.default_timer() - start_time
print(f'Time of calculating Mx : {tm} seconds')
print(f'Mx = {mx}')

start_time = timeit.default_timer()
dx = 0
for i in range(N):
    dx += ((x[i] - mx) ** 2)
dx /= N-1
td = timeit.default_timer() - start_time
print(f'Time of calculating Dx: {td} seconds')
print(f'Dx = {dx}')


with open('calculation.txt', 'w+') as file:
    file.write(f'An expected value = {mx}\n'
               f'The variance = {dx}\n'
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



