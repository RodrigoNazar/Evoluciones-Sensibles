
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
