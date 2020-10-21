
from lib.utils import matrix_save, matrix_read, leds_left
from lib.data_structures import Grid, Stream
import json

import sys


def get_size(obj, seen=None):
    """Recursively finds size of objects
    from https://goshippo.com/blog/measure-real-size-any-python-object/
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def matrix_save_test():

    test = [[i for i in range(10)] for _ in range(10)]

    matrix_save(test, 'Grid.txt')

    with open('Grid.txt', 'r') as file:
        a = json.load(file)

    print(a, type(a), len(a))


def leds_left_here():

    DONE_LEDS = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87]

    leds_left(DONE_LEDS)


def grid_test(path, debug=False):
    grid = matrix_read(path)

    grid = Grid(grid, strip=[i for i in range(1, 101)])

    print('progression')

    print(grid.radial_progression)

    if debug:

        print(len(grid.state), len(grid.state[0]))

        print(grid.get_state_element(30, 4))
        print(grid.get_state_element(*grid.center))
        print(grid.pos_hash[2])
        print(grid.shape())

        print('progression')

        print(grid.radial_progression)

        for i in grid.state:
            print(type(i))

        # setter and getter of elements and values in strip
        print('antes', grid.get_state_element_by_pos(30, 4))
        print('stream', grid.states)

        # LED 98
        print('LED 98')
        print('seteando...', grid.set_state_element_by_pos(30, 4, (255, 255, 255)))
        print('despues', grid.get_state_element_by_pos(30, 4))
        print('stream', grid.states)

        # LED 39
        print('LED 39')
        print('seteando...', grid.set_state_element_by_pos(26, 39, (255, 255, 255)))
        print('despues', grid.get_state_element_by_pos(26, 39))
        print('stream', grid.states)

        # LED 39 -- again
        print('LED 39 -- again')
        print('seteando...', grid.set_state_element_by_num(39, (0, 230, 120)))
        print('despues', grid.get_state_element_by_pos(26, 39))
        print('stream', grid.states)

        # LED 21
        print('LED 21')
        print('seteando...', grid.set_state_element_by_num(21, (0, 230, 120)))
        print('despues', grid.get_state_element_by_num(21))
        print('stream', grid.states)

        # Annother test
        # Changes
        changes = ((i, 1, 2, 3) for i in range(1, 4))
        print('Changes 1')
        print('stream antes', grid.states)
        print('seteando...', grid.set_state_elements_by_num(changes))
        print('stream', grid.states)

        changes = ((i, 20, 20, 3) for i in range(1, 15))
        print('Changes 2')
        print('seteando...', grid.set_state_elements_by_num(changes))
        print('stream', grid.states)

        print('grid object size', get_size(grid))


def stream_test():
    data = [i for i in range(16)]

    stream = Stream()

    for i in data:
        stream.append(i)

    print(stream)
    print(stream[3])


if __name__ == '__main__':
    # matrix_save_test()
    # leds_left_here()
    grid_test('grid/Grid.txt')
    # stream_test()
