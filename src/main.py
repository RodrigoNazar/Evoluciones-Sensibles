import _thread as th
from machine import Pin, PWM
from hcsr04 import HCSR04
from stream import Stream


# TO DO
RANDOM = True

# Hiperparámetros
TIME = .05
stream = Stream()
sensor = HCSR04(trigger_pin=26, echo_pin=25)
leds = [PWM(Pin(i), freq=20000, duty=0) for i in [13, 12, 14, 27]]


# senser_thr = th.Thread(target=senser, args=[sensor, stream])
# lighter_thr = th.Thread(target=lighter, args=[stream])

th.start_new_thread(senser, (sensor, stream))  # Senser thread
th.start_new_thread(lighter, (leds, stream))  # Light thread
