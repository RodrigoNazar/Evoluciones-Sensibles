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


def lighter(grid_states, strip, sensor_stream, debug=False):
    prev_dist = 150
    first_loop = True
    while 1:
        dist = sensor_stream.get_mean()
        vel = dist - prev_dist

        if debug:
            print('\nEl sensor_stream es', sensor_stream)
            print('La distancia sensada es', dist)
            print('La velocidad del objeto es:', vel)

        # Logic of the light system

        # Podría ser sólo un if que reaccione frente a la velocidad
        # Y calcula parámetros en función de la distancia
        if abs(vel) <= 50:
            # period = dist * .5 / 300
            random_blink(grid_states, strip, period=.1, intensity=.5)

        elif 50 < vel and not first_loop:
            # print('Center wave1: dist', dist, 'vel', vel)
            reverse_center_wave(grid_states, strip, period=.0, intensity=.80)

        # elif -5 > vel and vel > -15:
        elif -50 > vel and not first_loop:
            # print('Center wave2: dist', dist, 'vel', vel)
            center_wave(grid_states, strip, period=.0, intensity=.80)

        # Data for the computation of the velocity
        prev_dist = dist
        if first_loop and len(sensor_stream) == sensor_stream.l_max:
            first_loop = False


def center_wave(grid_states, strip, period, intensity):
    progression = grid_states.kwargs.get('radial_progression')

    color = int(255 * intensity)

    for leds in progression:
        new_state = [(led, color, color, color) for led in leds]

        grid_states.append(new_state)
        state_transition(grid_states, strip, period=period, iterations=1)


def reverse_center_wave(grid_states, strip, period, intensity):
    progression = grid_states.kwargs.get('radial_progression')
    progression.reverse()

    color = int(255 * intensity)

    for leds in progression:
        new_state = [(led, color, color, color) for led in leds]

        grid_states.append(new_state)
        state_transition(grid_states, strip, period=period, iterations=1)


def random_blink(grid_states, strip, period, intensity, prob=.5):

    new_state = grid_states.last_state().copy()

    # new_state = []

    # Led deletion phase
    for led in grid_states.last_state():
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

    grid_states.append(new_state)
    state_transition(grid_states, strip, period=period, iterations=5)
