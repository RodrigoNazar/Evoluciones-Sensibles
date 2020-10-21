import threading as th
# from machine import Pin
# from lib.hcsr04 import HCSR04
from lib.data_structures import Stream, Grid
from lib.utils import matrix_read
from lib.routines import senser, lighter
# import neopixel


# Hyperparameters
GRID_PATH = './grid/Grid.txt'
N_LEDS = 100  # Number of leds of the strip
STRIP_PIN = 4  # Pin D4
TRIGGER_PIN = 26  # Pin D26
ECHO_PIN = 25  # Pin D25


# NeoPixel Strip object
# strip = neopixel.NeoPixel(Pin(STRIP_PIN), N_LEDS)

false_strip = [i for i in range(1, N_LEDS + 1)]

# Grid Object
grid = matrix_read(GRID_PATH)
grid = Grid(grid, strip=false_strip)

# Movement Sensor
sensor_stream = Stream()
# sensor = HCSR04(trigger_pin=TRIGGER_PIN, echo_pin=ECHO_PIN)


# Starting the routines in threads
th.start_new_thread(senser, (sensor, sensor_stream))  # Senser thread
th.start_new_thread(lighter, (grid, sensor_stream))  # Light thread
