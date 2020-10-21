
from lib.utils import matrix_read
from lib.data_structures import Grid, Stream

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


def grid_test(path, debug=False):
    grid = matrix_read(path)

    grid = Grid(grid, strip=[i for i in range(1, 101)])

    if debug:

        print(len(grid.state), len(grid.state[0]))

        print(grid.get_state_element(30, 4))
        print(grid.get_state_element(*grid.center))
        print(grid.pos_hash[2])
        print(grid.shape())

        print('progression')

        grid.gen_radial_progression()

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

    print('grid object size', get_size(grid))


def stream_test():
    data = [i for i in range(16)]

    stream = Stream()

    for i in data:
        stream.append(i)

    print(stream)
    print(stream[3])


if __name__ == '__main__':
    grid_test('grid/Grid.txt')
    # stream_test()
