
from lib.utils import matrix_read
from lib.data_structures import Grid, Stream


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
