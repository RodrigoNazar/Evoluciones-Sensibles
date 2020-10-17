import _thread as th
from machine import Pin, PWM
import time


def led(pin, delay):
    while True:
        time.sleep(delay)
        pin.duty(512)
        time.sleep(delay)
        pin.duty(0)


pin1 = PWM(Pin(13), freq=20000, duty=512)
pin2 = PWM(Pin(12), freq=20000, duty=512)
pin3 = PWM(Pin(14), freq=20000, duty=512)
pin4 = PWM(Pin(27), freq=20000, duty=512)


th.start_new_thread(led, (pin1, .15))
th.start_new_thread(led, (pin2, .3))
th.start_new_thread(led, (pin3, .15))
th.start_new_thread(led, (pin4, .3))

print('Threads running!')
