
from utils.utils import matrix_save, matrix_read, leds_left
from utils.data_structures import Grid
import json
import numpy as np


def matrix_save_test():

    test = [[i for i in range(10)] for _ in range(10)]

    matrix_save(test, 'Grid.txt')

    with open('Grid.txt', 'r') as file:
        a = json.load(file)

    print(a, type(a), len(a))


def matrix_read_test():
    a = matrix_read('Grid.txt')
    a = np.array(a)
    print(a, type(a), a.shape)


def leds_left_here():

    DONE_LEDS = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87]

    leds_left(DONE_LEDS)


def grid_test():
    grid = matrix_read('Grid.txt')

    grid = Grid(grid)

    print(len(grid.state), len(grid.state[0]))

    print(grid.get_state_element(30, 4))
    print(grid.get_state_element(*grid.center))
    print(grid.pos_hash[2])
    print(grid.shape())

    print('progression')

    grid.gen_radial_progression()

    # for i in grid.state:
    #     print(type(i))


if __name__ == '__main__':
    # matrix_save_test()
    # matrix_read_test()
    # leds_left_here()
    grid_test()
