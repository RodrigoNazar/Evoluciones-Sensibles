import time


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
