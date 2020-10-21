

class Grid:
    def __init__(self, grid, strip, center=(23, 27)):
        # Physical devices
        self.grid = grid  # 2d matrix representation of the grid
        self.strip = strip  # LED strip object from NeoPixel
        self.center = center  # Position of the sensor

        # Software data structures
        self.LEDS_on = []  # LEDS that are on, tuples form: (n_led, r, g, b)
        # State stream of led on
        self.states = Stream(data=[self.LEDS_on], l_max=3)
        # Hash table: n_led -> position AND position -> n_led
        self.hash_n_pos, self.hash_pos_n = self.gen_pos_hash()
        self.radial_progression = self.gen_radial_progression()

        # Free memory
        del self.grid

    def remove_LED(self, n_led):
        # We delete it from the LEDS on
        self.LEDS_on = [led for led in self.LEDS_on if led[0] != n_led]

        self.set_state_element(*pos, (0, 0, 0))

    def clear_LEDS(self):
        for led in self.LEDS_on:
            self.LEDS_on.remove(led)

    def gen_state_grid(self):
        '''
        Generates a matrix representation of the actual grid state
        '''

        state = self.states[-1]

        for row in self.grid:
            state_row = []
            for elem in row:
                if elem != 0:
                    state_row.append(
                        {
                            'n': elem,
                            'color': (0, 0, 0)
                        }
                    )
                else:
                    state_row.append(0)
            state.append(state_row)
        return state

    def gen_pos_hash(self):
        hash_n_pos, hash_pos_n = {}, {}

        for i_row, row in enumerate(self.grid):
            for i_col, elem in enumerate(row):
                if elem != 0:
                    hash_n_pos[elem] = (i_col, i_row)
                    hash_pos_n[(i_col, i_row)] = elem
        return hash_n_pos, hash_pos_n

    def get_state_element(self, coord_x, coord_y):
        return self.states[-1][coord_y][coord_x]

    def set_state_element(self, coord_x, coord_y, color):
        '''
        Cambiar a que utilice los elementos de la lista de leds prendidos
        '''
        state = self.states[-1].copy()  # get the last state

        hash = state[coord_y][coord_x]  # Getting the led object

        # We overwrite the color
        if isinstance(hash, dict):
            state[coord_y][coord_x]['color'] = color

            # If the color is != than none
            if color != (0, 0, 0):
                self.LEDS_on.append((state[coord_y][coord_x]['n'], *color))

            # If we turn off the led, we delete it
            else:
                self.remove_LED(state[coord_y][coord_x]['n'])

            self.states.append(state)

    def gen_radial_progression(self):
        '''
        from
        https://www.geeksforgeeks.org/print-a-given-matrix-in-spiral-form/
        '''
        m, n = self.shape()
        k = 0
        le = 0

        radial_items = []

        while (k < m and le < n):
            items = []
            # Print the first row from
            # the remaining rows
            for i in range(le, n):
                if self.grid[k][i] != 0:
                    items.append(self.grid[k][i])
            k += 1

            for i in range(k, m):
                if self.grid[i][n - 1] != 0:
                    items.append(self.grid[i][n - 1])
            n -= 1

            # Print the last row from
            # the remaining rows
            if (k < m):
                for i in range(n - 1, (le - 1), -1):
                    if self.grid[m - 1][i] != 0:
                        items.append(self.grid[m - 1][i])

                m -= 1

            # Print the first column from
            # the remaining columns
            if (le < n):
                for i in range(m - 1, k - 1, -1):
                    if self.grid[i][le] != 0:
                        items.append(self.grid[i][le])

                le += 1

            if items:
                radial_items.append(items)

        return radial_items

    def shape(self):
        return (len(self.grid), len(self.grid[0]))


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

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):  # Retorna el largo
        return len(self.data)

    def __repr__(self):  # Retorna la lista
        return str(self.data)
