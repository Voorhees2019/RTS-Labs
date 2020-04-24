from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel
import timeit
import random
import math

Config.set('kivy', 'keyboard_mode', 'systemanddock')
# Window.size = (320, 480)


def is_prime(n):
    a = 2
    while n % a != 0:
        a += 1
    return a == n


def is_square(x):
    return (int(x ** 0.5)) ** 2 == x


def factorize_Ferma(n):
    if n <= 1:
        return None, None, 'Error: the number must be > 1'

    if n % 2 == 0:
        return None, None, 'Error: the number must be odd'

    if is_prime(n):
        return 1, n, 'The number is prime'

    if is_square(n):
        return int(n ** 0.5), int(n ** 0.5), 'SUCCESSFULLY'

    x = int(n ** 0.5) + 1

    while not is_square(x * x - n):
        x += 1

    y = int((x * x - n) ** 0.5)
    a, b = x - y, x + y
    return a, b, 'SUCCESSFULLY'


def predict(dot, weights, P):
    s = 0
    for i in range(len(dot)):
        s += weights[i] * dot[i]
    return 1 if s > P else 0


def train_perceptron(learning_rate, deadline, iterations):
    P = 4
    data = [(0, 6), (1, 5), (3, 3), (2, 4)]
    n = len(data[0])
    weights = [0.001, -0.004]
    outputs = [0, 0, 0, 1]
    start_time = timeit.default_timer()
    for _ in range(iterations):
        total_error = 0
        for i in range(len(outputs)):
            prediction = predict(data[i], weights, P)
            err = outputs[i] - prediction
            total_error += err
            for j in range(n):
                delta = learning_rate * data[i][j] * err
                weights[j] += delta
        if total_error == 0 or timeit.default_timer() - start_time > deadline:
            break
    return weights[0], weights[1]


def get_roots_genetic(a, b, c, d, y, mutate_chance=0.1):
    num_pop = 4
    population = [[random.randint(0, int(y / 4)) for i in range(4)] for j in range(num_pop)]
    chance = mutate_chance
    counter = 0
    roots = [i[0] * a + i[1] * b + i[2] * c + i[3] * d for i in population]
    while y not in roots:
        deltas = [1 / abs(i - y) for i in roots]
        chances = [i / sum(deltas) for i in deltas]
        for i in range(int(num_pop / 2)):
            tmp = random.uniform(0, 1)
            if tmp < chances[0]:
                par1 = population[0]
            elif tmp < chances[0] + chances[1]:
                par1 = population[1]
            elif tmp < chances[0] + chances[1] + chances[2]:
                par1 = population[2]
            else:
                par1 = population[3]

            par2 = par1
            while par2 == par1:
                tmp2 = random.uniform(0, 1)
                if tmp2 < chances[0]:
                    par2 = population[0]
                elif tmp2 < chances[0] + chances[1]:
                    par2 = population[1]
                elif tmp2 < chances[0] + chances[1] + chances[2]:
                    par2 = population[2]
                else:
                    par2 = population[3]

            gene = random.randint(0, 3)
            par1[gene], par2[gene] = par2[gene], par1[gene]
            for j in range(4):
                tmp = random.uniform(0, 1)
                if tmp < chance:
                    par1[j] += random.choice([-1, 1])
                tmp = random.uniform(0, 1)
                if tmp < chance:
                    par2[j] += random.choice([-1, 1])
            population[2 * i] = par1
            population[2 * i + 1] = par2
        roots = [j[0] * a + j[1] * b + j[2] * c + j[3] * d for j in population]
        counter += 1
    return population[roots.index(y)], counter


class Container(TabbedPanel):

    def calculate1(self):
        try:
            inp_number = int(self.text_input.text)
            a, b, c = factorize_Ferma(inp_number)
            self.first_number.text, self.second_number.text, self.factorization_state.text = str(a), str(b), c
        except:
            inp_number = 0
            self.factorization_state.text = 'Incorrect input'

    def calculate2(self):
        try:
            learning_rate, deadline, iterations_number = float(self.learning_rate.text), int(self.deadline.text), int(
                self.iterations_number.text)
        except:
            learning_rate, deadline, iterations_number = 0.001, 5, 10000

        first, second = train_perceptron(learning_rate, deadline, iterations_number)
        self.w1.text, self.w2.text = str(first), str(second)

    def calculate3(self):
        try:
            a_val, b_val, c_val, d_val, y_val = int(self.a_val.text), int(self.b_val.text), int(self.c_val.text),\
                                                int(self.d_val.text), int(self.y_val.text)
        except:
            a_val, b_val, c_val, d_val, y_val = 1, 1, 1, 1, 8

        roots = get_roots_genetic(a_val, b_val, c_val, d_val, y_val)[0]
        self.roots.text = str(roots)

        iterations = []
        experiments = 10
        mutate_chances = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
        for i in mutate_chances:
            steps = 0
            for j in range(experiments):
                steps += get_roots_genetic(a_val, b_val, c_val, d_val, y_val, i)[1]
            iterations.append(math.ceil(steps / experiments))
        ind = iterations.index(min(iterations))
        best_chance = mutate_chances[ind]
        self.mutate_chance.text = str(best_chance)


class MyApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MyApp().run()
