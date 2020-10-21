import time


def senser(sensor, sensor_stream, w_time=.1):
    '''
    Distance sensor thread routine
    '''
    while 1:
        # We get the value from the sensor
        new_val = sensor.distance_cm()
        # Append it to the stream
        sensor_stream.append(new_val)
        # Wait some time
        time.sleep(w_time)


def lighter(grid, sensor_stream, debug=False):
    prev_median = 200

    while 1:
        dist_median = sensor_stream.get_median()
        vel_median = dist_median - prev_median

        if debug:
            print('\nEl sensor_stream es', sensor_stream)
            print('La mediana sensada es', dist_median)
            print('La velocidad del objeto en mediana es:', vel_median)

        prev_median = dist_median
