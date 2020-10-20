
import json


def matrix_save(matrix, name, beautify=False):
    '''
    beautify = True on develop
    '''

    # Script for larger dimension matrix saving
    dim = 0
    aux = matrix

    while isinstance(aux, list):
        if aux:
            aux = aux[0]
            dim += 1

    with open(name, 'w') as file:
        if beautify:
            file.write('[\n')
            for row in matrix:
                file.write(json.dumps(row))
                file.write(',\n')
            file.write(']')

        else:
            file.write(json.dumps(matrix, indent=2))


def matrix_read(path):

    with open(path, 'r') as file:
        data = json.load(file)

    return data


def leds_left(done_leds, n_leds=100):
    leds = [i for i in range(1, n_leds + 1)]

    for i in done_leds:
        leds.remove(i)

    print(leds)
