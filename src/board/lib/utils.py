

def matrix_read(path):
    with open(path, 'r') as file:
        data = []
        for line in file:
            if line != '[\n' and line != ']\n' and line != '\n':
                row = ''.join(line.split(','))
                row = row.split(' ')
                row = row[1:-2]
                row = [int(i) for i in row
                       if i != '' and i != '[' and i != ']']
                data.append(row)
    return data
