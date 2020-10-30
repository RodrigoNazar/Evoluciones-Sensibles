
from lib.utils import matrix_read
from lib.data_structures import Grid, Stream
import random


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


def states_test():
    data = [[i for i in range(random.randint(1, 5))] for i in range(16)]

    radial_progression = [[i for i in range(random.randint(1, 5))]
                          for _ in range(6)]

    kwargs = {
        'radial_progression': radial_progression
    }
    # We use a Stream of states instead of a grid object
    grid_states = Stream(data=[], l_max=2, kwargs=kwargs)

    print('kwargs', grid_states.kwargs)

    for i in data:
        grid_states.append(i)

    print(grid_states)
    print(grid_states[1])


def radial_progression_merging():

    radial_progression = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                          [10, 11, 12], [13, 14, 15]]

    radial_progression = ((i, i+j) for i, j in zip(radial_progression, radial_progression[1:]))

    final_radial_progression = []
    for elems in radial_progression:
        final_radial_progression.append(elems[0])
        final_radial_progression.append(elems[1])

    print(final_radial_progression)


def state_transition_test(states):
    new_state = states.last_state()
    new_state_leds_on = [i[0] for i in new_state]

    if len(states) >= 2:
        previous_state = states[-2]
    else:
        previous_state = []
    prev_state_leds_on = [i[0] for i in previous_state]

    # Leds that turn off
    leds_turned_off = [i for i in prev_state_leds_on
                       if i not in new_state_leds_on]
    leds_turned_off = [i for i in previous_state if i[0] in leds_turned_off]

    # Leds that turn on
    leds_turned_on = [i for i in new_state_leds_on
                      if i not in prev_state_leds_on]
    leds_turned_on = [i for i in new_state if i[0] in leds_turned_on]

    print('leds_turned_off', [i[0] for i in leds_turned_off])
    print('leds_turned_on', [i[0] for i in leds_turned_on])


def light_test():
    radial_progression = [
        [1, 7, 8, 6, 9, 3, 2, 11, 24, 23, 12],
        [1, 7, 8, 6, 9, 3, 2, 11, 24, 23, 12, 10, 25, 22, 21, 5, 4, 15, 26, 50,
         14, 13],
        [10, 25, 22, 21, 5, 4, 15, 26, 50, 14, 13],
        [10, 25, 22, 21, 5, 4, 15, 26, 50, 14, 13, 30, 27, 20, 19, 16, 28, 29,
         49, 44, 17, 35, 34, 33, 32, 31],
        [30, 27, 20, 19, 16, 28, 29, 49, 44, 17, 35, 34, 33, 32, 31],
        [30, 27, 20, 19, 16, 28, 29, 49, 44, 17, 35, 34, 33, 32, 31, 43, 18, 36,
         51, 48, 45, 40, 52, 42, 41, 37],
        [43, 18, 36, 51, 48, 45, 40, 52, 42, 41, 37],
        [43, 18, 36, 51, 48, 45, 40, 52, 42, 41, 37, 47, 46, 39, 61, 57, 55, 53,
         94, 92, 83, 68],
        [47, 46, 39, 61, 57, 55, 53, 94, 92, 83, 68],
        [47, 46, 39, 61, 57, 55, 53, 94, 92, 83, 68, 58, 56, 54, 93, 38, 66, 64,
         60, 59, 84, 71, 67, 65],
        [58, 56, 54, 93, 38, 66, 64, 60, 59, 84, 71, 67, 65],
        [58, 56, 54, 93, 38, 66, 64, 60, 59, 84, 71, 67, 65, 95, 90, 82, 72, 70,
         69, 62, 99, 91, 89, 79, 73, 63],
        [95, 90, 82, 72, 70, 69, 62, 99, 91, 89, 79, 73, 63],
        [95, 90, 82, 72, 70, 69, 62, 99, 91, 89, 79, 73, 63, 100, 97, 88, 85,
         78, 71, 98, 96, 81, 80, 86, 75]
    ]

    kwargs = {
        'radial_progression': radial_progression
    }
    # We use a Stream of states instead of a grid object
    grid_states = Stream(data=[], l_max=2, kwargs=kwargs)

    for it in radial_progression:
        color = 255
        new_state = [(led, color, color, color) for led in it]
        grid_states.append(new_state)

        print('\nit', it)

        state_transition_test(grid_states)

        input()


if __name__ == '__main__':
    # grid_test('grid/Grid.txt')
    # stream_test()
    # states_test()
    # radial_progression_merging()
    light_test()
