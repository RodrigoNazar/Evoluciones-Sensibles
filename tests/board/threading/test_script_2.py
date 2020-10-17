
import threading as th
import time
import random


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


def senser(stream):
    while 1:
        new_val = random.randint(0, 30)  # Obtiene el valor del sensor
        stream.append(new_val)

        print(f'\tMido en el sensor {new_val} cm...')
        time.sleep(TIME)


def lighter(stream):
    # prev_mean = 50
    prev_median = 50

    while 1:
        # actual_mean = stream.get_mean()
        actual_median = stream.get_median()

        # vel_mean = actual_mean - prev_mean
        vel_median = actual_median - prev_median

        print(f'\nEl stream es {stream}')
        # print(f'La media sensada es {actual_mean}')
        print(f'La mediana sensada es {actual_median}')  # N // 2 muestras para el trigger
        # print(f'La velocidad del objeto en media es: {vel_mean}')
        print(f'La velocidad del objeto en mediana es: {vel_median}')

        if vel_median > -20 and actual_median > 30:
            print('Se acercó el objeto rápidamente, pero está lejos')



        # prev_mean = actual_mean
        prev_median = actual_median

        time.sleep(TIME*.8)


# TO DO
RANDOM = True
SENSED_STREAM = [100, 80, 60, 40, 10, 1]

# Hiperparámetros
TIME = .5
stream = Stream()


senser_thr = th.Thread(target=senser, args=[stream])
lighter_thr = th.Thread(target=lighter, args=[stream])

senser_thr.start()
lighter_thr.start()
