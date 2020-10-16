
import threading as th
import time

start = time.perf_counter()


def do_something(seconds=1):
    print(f'\nSleeping {seconds} second(s)...')
    time.sleep(seconds)
    print(f'Done Sleeping {seconds}')


threads = []

for i in range(10):
    t = th.Thread(target=do_something, args=[i])
    t.start()  # Empieza la ejecución del thread

    threads.append(t)

for thread in threads:
    thread.join()


finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')
