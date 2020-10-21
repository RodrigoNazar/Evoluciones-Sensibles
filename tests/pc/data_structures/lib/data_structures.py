
import time


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
        self.hash_n_pos, self.hash_pos_n = self.gen_hashes()
        self.radial_progression = self.gen_radial_progression()

        # Free memory
        del self.grid

    def last_state(self):
        return self.states[-1]

    def remove_LED(self, n_led):
        '''
        Remove the led from the leds_on structure and update the state
        '''
        # We delete it from the LEDS on
        self.LEDS_on = [led for led in self.LEDS_on if led[0] != n_led]

        # We clear the led color if its valid
        pos = self.hash_n_pos.get(n_led)
        if pos:
            self.set_state_element_by_pos(pos[0], pos[1], (0, 0, 0))

    def clear_LEDS(self):
        '''
        Clears all leds colors
        '''
        for led in self.LEDS_on:
            self.remove_LED(led[0])

    def gen_state_grid(self):
        '''
        ** UNFINISHED
        *  LOW PRIORITY
        Generates a matrix representation of the actual grid state

        Todo: Match the real color
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

    def gen_hashes(self):
        '''
        Creates the following hash tables:
            - n_led -> position
            - position -> n_led
        '''
        hash_n_pos, hash_pos_n = {}, {}

        for i_row, row in enumerate(self.grid):
            for i_col, elem in enumerate(row):
                if elem != 0:
                    hash_n_pos[elem] = (i_col, i_row)
                    hash_pos_n[(i_col, i_row)] = elem
        return hash_n_pos, hash_pos_n

    def get_state_element_by_pos(self, coord_x, coord_y):
        '''
        Get the state of the a led by the position in the grid
        '''
        n_led = self.hash_pos_n.get((coord_x, coord_y))  # Getting the n_led
        if n_led is None:
            return
        state = [elem for elem in self.states[-1] if elem[0] == n_led]
        if state:
            return state[0]

    def get_state_element_by_num(self, n_led):
        '''
        Get the state of the a led by its number
        '''
        state = [elem for elem in self.states[-1] if elem[0] == n_led]
        if state:
            return state[0]

    def set_state_element_by_pos(self, coord_x, coord_y, color):
        '''
        Change the state of the a led by the position in the grid
        '''
        n_led = self.hash_pos_n.get((coord_x, coord_y))  # Getting the n_led

        if n_led is None:
            return

        # We search if the led was on
        state = [elem for elem in self.states[-1] if elem[0] == n_led]

        # If its on, we overwrite the color
        if state:
            new_state = self.states[-1].copy()

            for indx, elem in enumerate(new_state):
                if n_led == elem[0]:
                    new_state[indx] = (n_led, color[0], color[1], color[2])

        # If the led was off, we turn it on
        else:
            new_state = self.states[-1].copy()
            led_object = (n_led, color[0], color[1], color[2])

            if color != (0, 0, 0):
                new_state.append(led_object)

            else:
                self.remove_LED(led_object)

        # We modify the color of the strip
        self.strip[n_led] = color

        # Lastly we append the new state
        self.states.append(new_state)

    def set_state_element_by_num(self, n_led, color):
        '''
        Change the state of the a led by its number
        '''

        # We search if the led was on
        state = [elem for elem in self.states[-1] if elem[0] == n_led]

        # If its on, we overwrite the color
        if state:
            new_state = self.states[-1].copy()

            for indx, elem in enumerate(new_state):
                if n_led == elem[0]:
                    new_state[indx] = (n_led, color[0], color[1], color[2])

        # If the led was off, we turn it on
        else:
            new_state = self.states[-1].copy()
            led_object = (n_led, color[0], color[1], color[2])

            if color != (0, 0, 0):
                new_state.append(led_object)

            else:
                self.remove_LED(led_object)

        # We modify the color of the strip
        self.strip[n_led] = color

        # Lastly we append the new state
        self.states.append(new_state)

    def set_state_elements_by_num(self, elems):
        '''
        Change the state of multiple led by the position in the grid
        elems must be an iterable object and its elements must be of the form:
            (n_led, r, g, b)
        '''
        # We create a new state
        new_state = self.states[-1].copy()

        for new_elem in elems:

            n_led = new_elem[0]
            color = new_elem[1:]

            # We search if the led was on
            state = [i for i in new_state if i[0] == n_led]

            # If its on, we overwrite the color
            if state:
                for indx, elem in enumerate(new_state):
                    if n_led == elem[0]:
                        new_state[indx] = new_elem

            # If the led was off, we turn it on
            else:
                if color != (0, 0, 0):
                    new_state.append(new_elem)

                else:
                    self.remove_LED(new_elem)

            # We modify the color of the strip
            self.strip[n_led] = color

        # Lastly we append the new state
        self.states.append(new_state)

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

        radial_items.reverse()
        return radial_items

    def state_transition(self, period, iterations=10):
        '''
        Transition from the previous to the actual grid state in $period seconds
        '''
        actual_state = self.last_state()
        actual_leds_on = [i[0] for i in actual_state]

        if len(self.states) >= 2:
            previous_state = self.states[-2]
        else:
            previous_state = []
        leds_turned_off = [i for i in previous_state
                           if i[0] not in actual_leds_on]

        for it in range(iterations):
            for led in actual_state:
                n_led = led[0]
                r, g, b = led[1:]
                r = r * it / iterations
                g = g * it / iterations
                b = b * it / iterations

                self.strip[n_led] = (r, g, b)

            for led in leds_turned_off:
                n_led = led[0]
                r, g, b = led[1:]
                r = r * (iterations - it) / iterations
                g = g * (iterations - it) / iterations
                b = b * (iterations - it) / iterations

                self.strip[n_led] = (r, g, b)

            time.sleep(period / iterations)

            self.strip.write()

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
