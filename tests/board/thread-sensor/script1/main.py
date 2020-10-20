import _thread as th
import time
from machine import Pin, PWM
from hcsr04 import HCSR04


class Stream:
    def __init__(self, data=[], l_max=9):
        self.data = data
        self.l_max = l_max

    def append(self, val):  # Agrega valores al stream, que tiene largo máximo
        if len(self) >= self.l_max:
            self.data = self.data[1:]

            self.data.append(val)
        else:
            self.data.append(val)

    def clean(self):  # Limpia el stram
        self.data = []

    def get_mean(self):  # Retorna la media de los datos
        if len(self) > 0:
            return sum(self.data) / len(self)
        else:
            return 0

    def get_median(self):  # Retorna la media de los datos
        if len(self) > 0:
            sorted_data = sorted(self.data)
            return sorted_data[len(self) // 2]
        else:
            return 0

    def __len__(self):  # Retorna el largo
        return len(self.data)

    def __repr__(self):  # Retorna la lista
        return str(self.data)


def senser(sensor, stream):
    while 1:
        new_val = sensor.distance_cm()  # Obtiene el valor del sensor
        stream.append(new_val)

        # print(f'\tMido en el sensor {new_val} cm...')
        time.sleep(TIME)


def lighter(leds, stream, n_leds=100, debug=False):
    # prev_mean = 50
    prev_median = 50

    base_duty = 512

    while 1:
        # actual_mean = stream.get_mean()
        actual_median = stream.get_median()

        # vel_mean = actual_mean - prev_mean
        vel_median = actual_median - prev_median

        print('\nEl stream es', stream)
        # print(f'La media sensada es {actual_mean}')
        print('La mediana 'alejo'sensada es', actual_median)  # N // 2 muestras para el trigger
        # print(f'La velocidad del objeto en media es: {vel_mean}')
        print('La velocidad del objeto en mediana es:', vel_median)

        # if vel_median > -20 and actual_median > 30:
        #     print('Se acercó el objeto rápidamente, pero está lejos')

        # if abs(actual_median) > 0:


        for i in range(2):
            leds[i].duty(base_duty - int(abs(actual_median))*10)

        # for i in range(2, 4):
        #     leds[i].duty(base_duty - int(abs(vel_median))*14)

        # prev_mean = actual_mean
        prev_median = actual_median

        time.sleep(TIME)


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
