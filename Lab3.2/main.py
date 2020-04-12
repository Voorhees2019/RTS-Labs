from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel
import timeit

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
            learning_rate, deadline, iterations_number = 0, 0, 0

        first, second = train_perceptron(learning_rate, deadline, iterations_number)
        self.w1.text, self.w2.text = str(first), str(second)


class MyApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MyApp().run()
