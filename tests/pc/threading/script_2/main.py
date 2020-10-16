
import threading as th
import time

start = time.perf_counter()


def do_something(t=1):
    print(f'\nSleeping {t} second...')
    time.sleep(t)
    print('Done Sleeping')


t1 = th.Thread(target=do_something)
t2 = th.Thread(target=do_something)

t1.start()  # Empieza la ejecución del thread
t2.start()

t1.join()  # Hay que esperar a que termine el thread para seguir
t2.join()

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')
