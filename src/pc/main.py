
from utils.utils import matrix_save, matrix_read, leds_left
import json
import numpy as np


def matrix_save_test():

    test = [[i for i in range(10)] for _ in range(10)]

    matrix_save(test, 'test.json')

    with open('test.json', 'r') as file:
        a = json.load(file)

    print(a, type(a), len(a))


def matrix_read_test():
    a = matrix_read('test.json')
    a = np.array(a)
    print(a, type(a), a.shape)


def leds_left_here():

    DONE_LEDS = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87]

    leds_left(DONE_LEDS)


if __name__ == '__main__':
    # matrix_save_test()
    matrix_read_test()
    # leds_left_here()
