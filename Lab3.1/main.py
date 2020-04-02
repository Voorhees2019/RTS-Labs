from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')
#Window.size = (320, 480)


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


class Container(GridLayout):

    def calculate(self):
        try:
            inp_number = int(self.text_input.text)
            a, b, c = factorize_Ferma(inp_number)
            self.first_number.text, self.second_number.text, self.factorization_state.text = str(a), str(b), c
        except:
            inp_number = 0
            self.factorization_state.text = 'Incorrect input'



class MyApp(App):
    def build(self):
        return Container()


if __name__ == "__main__":
    MyApp().run()
