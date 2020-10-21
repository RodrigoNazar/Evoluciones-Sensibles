import time
import random


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


def lighter(grid, sensor_stream, debug=False):
    prev_median = 200

    while 1:
        dist = sensor_stream.get_median()
        vel = dist - prev_median

        if debug:
            print('\nEl sensor_stream es', sensor_stream)
            print('La distancia sensada es', dist)
            print('La velocidad del objeto es:', vel)

        # Logic of the light system

        # Podría ser sólo un if que reaccione frente a la velocidad
        # Y calcula parámetros en función de la distancia
        if dist > 60 and vel < 5:
            random_blink(grid, period=.3, intensity=.40)

        elif dist < 60 and vel < 5:
            random_blink(grid, period=.15, intensity=.80)

        elif 5 < vel and vel < 15:
            center_wave(grid, period=.15, intensity=.80)

        elif -5 > vel and vel > -15:
            reverse_center_wave(grid, period=.15, intensity=.80)

        # Data for the computation of the velocity
        prev_median = dist


def center_wave(grid, period, intensity):
    progression = grid.radial_progression

    for leds in progression:
        new_state = []

        for led in leds:
            color = int(255 * intensity)
            led_object = (led, color, color, color)
            new_state.append(led_object)

        grid.set_state_elements_by_num(new_state)
        grid.state_transition(period)


def reverse_center_wave(grid, period, intensity):
    progression = grid.radial_progression
    progression.reverse()

    for leds in progression:
        new_state = []

        for led in leds:
            color = int(255 * intensity)
            led_object = (led, color, color, color)
            new_state.append(led_object)

        grid.set_state_elements_by_num(new_state)
        grid.state_transition(period)


def random_blink(grid, period, intensity, prob=.5):

    new_state = grid.last_state().copy()

    # Led deletion phase
    for led in grid.last_state():
        # With a probability of prob, we turn off the led
        if random.randint(0, 10) / 10 < prob:
            new_state.remove(led)

    # Led incorporation phase
    new_leds = [i[0] for i in new_state]
    n_new_leds = random.randint(0, 2)

    for i in range(n_new_leds):
        new_led = random.randint(1, 100)

        if new_led not in new_leds:
            color = int(255 * intensity)
            led_object = (new_led, color, color, color)
            new_state.append(led_object)

    grid.set_state_elements_by_num(new_state)
    grid.state_transition(period)
