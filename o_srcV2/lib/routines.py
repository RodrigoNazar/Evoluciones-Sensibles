import time
import random
from utils import state_transition


def senser(sensor, sensor_stream, w_time=.1):
    '''
    Distance sensor thread routine
    '''
    while 1:
        # We get the value from the sensor
        new_val = sensor.distance_cm()
        # Append it to the stream
        sensor_stream.append(new_val)
        # Wait some time
        time.sleep(w_time)


def lighter(grid_state, strip, sensor_stream, debug=False):
    prev_dist = 150
    wave_debounce = True

    # We start cycling
    while 1:
        dist = sensor_stream.get_mean()  # Distance of the object
        vel = dist - prev_dist  # Velocity of the object

        prev_state = {
            'pattern': rand_blink_by_iter,  # The pattern that was excecuting
            'state': grid_state,  # The state of the grid
            'goal_state': None,  # The goal state
            'iteration': None,  # The number of the previous iteration
            'goal_iter': None,  # The number of final iteration
            'intensity': None,  # The % of the maximum intensity
            'period': None,  # The sleep period of each iteration
            'other_info': None  # Gap for any other kind of info
        }

        # Logic of the light system

        # Podría ser sólo un if que reaccione frente a la velocidad
        # Y calcula parámetros en función de la distancia
        if abs(vel) <= 50:
            # period = dist * .5 / 300
            prev_state['pattern'] = rand_blink_by_iter

        elif 50 < vel and not wave_debounce:
            # print('Center wave1: dist', dist, 'vel', vel)
            prev_state['pattern'] = reverse_center_wave_by_it
            # wave_debounce = True
            # sensor_stream.clean()

        elif -50 > vel and not wave_debounce:
            # print('Center wave2: dist', dist, 'vel', vel)
            prev_state['pattern'] = center_wave_by_it
            # wave_debounce = True
            # sensor_stream.clean()

        # We call the pattern iteration function
        prev_state = prev_state['pattern'](prev_state)

        # Data for the computation of the velocity
        prev_dist = dist

        # The debounce routine
        if wave_debounce and len(sensor_stream) > 6:
            sensor_stream.clean()
            wave_debounce = False

        # Prints for debuging
        if debug:
            print('\nEl sensor_stream es', sensor_stream)
            print('La distancia sensada es', dist)
            print('La velocidad del objeto es:', vel)


def center_wave_by_it(state_object):
    ''' **************** This is a guide method **************
    '''
    # Steps of the wave pattern
    NUM_OF_IT = len(state_object['state'].kwargs['radial_progression'])

    # Current step of the pattern
    goal_iter = state_object['goal_iter']

    # We update the goal number of steps
    if (goal_iter is None) or (goal_iter != NUM_OF_IT):
        state_object['goal_iter'] = NUM_OF_IT

    grid_state = state_object['state']
    progression = grid_state.kwargs.get('radial_progression')

    color = int(255 * intensity)

    for leds in progression:
        new_state = [(led, color, color, color) for led in leds]

        grid_state.append(new_state)
        state_transition(grid_state, strip, period=period, iterations=1)


def reverse_center_wave_by_it(state_object):
    ''' ****************************** Need to be updated
    '''
    progression = grid_state.kwargs.get('radial_progression')
    progression.reverse()

    color = int(255 * intensity)

    for leds in progression:
        new_state = [(led, color, color, color) for led in leds]

        grid_state.append(new_state)
        state_transition(grid_state, strip, period=period, iterations=1)


def rand_blink_by_iter(state_object, prob=.5):
    ''' ****************************** Need to be updated
    '''

    new_state = grid_state.last_state().copy()

    # Led deletion phase
    for led in grid_state.last_state():
        # With a probability of prob, we turn off the led
        if random.randint(0, 10) / 10 < prob:
            new_state = [i for i in new_state if i[0] != led[0]]

    # Led incorporation phase
    n_new_leds = random.randint(0, 4)

    for i in range(n_new_leds):
        new_led = random.randint(1, 100)

        if new_led not in [i[0] for i in new_state]:
            color = int(255 * intensity)
            led_object = (new_led, color, color, color)
            new_state.append(led_object)

    grid_state.append(new_state)
    state_transition(grid_state, strip, period=period, iterations=8)
