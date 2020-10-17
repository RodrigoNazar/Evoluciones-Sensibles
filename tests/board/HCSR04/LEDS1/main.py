from machine import Pin, PWM
import time
import math

# pwm0 = PWM(Pin(0))      # create PWM object from a pin
# pwm0.freq()             # get current frequency
# pwm0.freq(1000)         # set frequency
# pwm0.duty()             # get current duty cycle
# pwm0.duty(200)          # set duty cycle
# pwm0.deinit()           # turn off PWM on the pin
#
# pwm2 = PWM(Pin(2), freq=20000, duty=512)  # create and configure in one go

pins = [Pin(i) for i in [13, 12, 14, 27]]

pwms = [PWM(i, freq=20000, duty=512) for i in pins]

for i in range(20):
    for pwm in pwms:
        pwm.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))

        time.sleep(.050)
