import random
import string


def generate_random_letters(length_value: int):
    """ Генерация случайных букв латинского алфавита"""
    letters_array = string.ascii_lowercase
    finish_array = []
    i = 0
    while i < length_value:
        position = random.choice(range(26))
        finish_array.append(letters_array[position])
        i += 1
    result_string = ''.join(str(x) for x in finish_array)
    return result_string
