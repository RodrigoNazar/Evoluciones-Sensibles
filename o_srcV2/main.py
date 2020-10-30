import _thread as th
from machine import Pin
from lib.hcsr04 import HCSR04
from lib.data_structures import Stream, Grid
from lib.utils import matrix_read, clear_strip
from lib.routines import senser, lighter
import neopixel


def main():
    print('\nSetting up the system...')

    # Hyperparameters
    GRID_PATH = './grid/Grid.txt'
    N_LEDS = 100  # Number of leds of the strip
    STRIP_PIN = 4  # Pin D4
    TRIGGER_PIN = 26  # Pin D26
    ECHO_PIN = 25  # Pin D25

    # NeoPixel Strip object
    strip = neopixel.NeoPixel(Pin(STRIP_PIN), N_LEDS)
    clear_strip(strip, N_LEDS)
    print('\nStrip ready!')

    # Grid Object
    grid = matrix_read(GRID_PATH)
    grid = Grid(grid, strip=strip)

    # We use the grid to compute the radial progression
    radial_progression = grid.radial_progression.copy()
    kwargs = {
        'radial_progression': radial_progression
    }
    # We use a Stream of states instead of a grid object
    grid_state = Stream(data=[], l_max=1, kwargs=kwargs)

    # Finally we delete the grid object
    del grid
    print('Grid ready!')

    # Movement Sensor
    sensor_stream = Stream(l_max=7)
    sensor = HCSR04(trigger_pin=TRIGGER_PIN, echo_pin=ECHO_PIN)
    print('Sensor ready!')

    print('\nStarting the routines threads...')
    # Starting the routines in threads
    # Senser thread
    th.start_new_thread(senser, (sensor, sensor_stream))
    # Light thread
    th.start_new_thread(lighter, (grid_state, strip, sensor_stream))
    print('Threads ready!')

# ***********************+ DELETE
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
