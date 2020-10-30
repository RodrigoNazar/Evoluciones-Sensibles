
import time


def matrix_read(path):
    with open(path, 'r') as file:
        data = []
        for line in file:
            if line != '[\n' and line != ']\n' and line != '\n':
                row = ''.join(line.split(','))
                row = row.split(' ')
                row = row[1:-2]
                row = [int(i) for i in row
                       if i != '' and i != '[' and i != ']']
                data.append(row)
    return data


def state_transition(states, strip, period=0, iterations=10):
    '''
    Transition from the previous to the new grid state in $period seconds
    '''
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

    for it in range(iterations):
        for led in leds_turned_on:
            n_led = led[0]
            r, g, b = led[1:]
            r = int(r * it / iterations)
            g = int(g * it / iterations)
            b = int(b * it / iterations)

            r = r if r <= 255 else 255
            g = g if g <= 255 else 255
            b = b if b <= 255 else 255

            if n_led <= 99:
                strip[n_led] = (r, g, b)

        for led in leds_turned_off:
            n_led = led[0]
            r, g, b = led[1:]
            r = int(r * (iterations - it) / iterations)
            g = int(g * (iterations - it) / iterations)
            b = int(b * (iterations - it) / iterations)

            r = r if r <= 255 else 255
            g = g if g <= 255 else 255
            b = b if b <= 255 else 255

            if n_led <= 99:
                strip[n_led] = (r, g, b)

        strip.write()
        time.sleep(period / iterations)

    # We make sure that all the leds turn off
    for led in leds_turned_off:
        n_led = led[0]

        if n_led <= 99:
            strip[n_led] = (0, 0, 0)
            strip.write()
