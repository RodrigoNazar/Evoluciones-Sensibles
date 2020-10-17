from hcsr04 import HCSR04
import time

sensor = HCSR04(trigger_pin=26, echo_pin=25)


while 1:
    distance = sensor.distance_cm()

    print('Distance:', distance, 'cm')

    time.sleep(.3)
