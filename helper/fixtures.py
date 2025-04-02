import collections
import random
import string
from functools import update_wrapper


def repeat_function(n: int):
    """Функция работает как декоратор, выполняет функцию рекурсивного повторения N раз
    Args:
        n - передаем обычно число, например - 20
    Returns:
        На выходе получаем повтор N раз указанный в агументах
    """

    def repeat_function_inner(f):
        update_wrapper(repeat_function_inner, f)

        def inner(*args, **kwargs):
            for i in range(n):
                f(*args, **kwargs)

        return inner

    return repeat_function_inner


def generate_random_string(length):
    """Функция генерирует рандомный набор букв для нейминга в создании продукта внутри РК
    Args:
        На вход принимается число int - например 10
    Returns:
        На выходе получим строку str из рандомного набора букв
    """
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return 'R' + rand_string


"""Класс для обработки увеличения счетчиков для динамических локаторов"""
Deck = collections.namedtuple('Card', ['testid', 'num'])


# TODO: доделать класс
class IDDeck:
    nums = [str(n) for n in range(0, 21)]
    testids = 'тут будет дата тест атрибут'.split()

    def __init__(self):
        self._ids = [
            Deck(testid, num) for num in self.nums for testid in self.testids
        ]

    def __len__(self):
        return len(self._ids)

    def __getitem__(self, position):
        return self._ids[position]
