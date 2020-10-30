
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
        self.states = Stream(data=[self.LEDS_on], l_max=2)
        # Hash table: n_led -> position AND position -> n_led
        self.hash_n_pos, self.hash_pos_n = self.gen_hashes()
        self.radial_progression = self.gen_radial_progression()

        # Free memory
        del self.grid

        # Clear the strip
        self.clear_strip()

    def last_state(self):
        return self.states[-1].copy()

    def clear_strip(self):
        '''
        * Made in a hurry
        '''
        for led in range(1, 100):
            self.strip[led] = (0, 0, 0)
            self.strip.write()

    def remove_LED(self, n_led):
        '''
        Remove the led from the leds_on structure and update the state
        '''
        # We delete it from the LEDS on
        self.LEDS_on = [led for led in self.LEDS_on if led[0] != n_led]

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

        # Lastly we append the new state
        self.states.append(new_state)

    def set_state_elements_by_num(self, elems):
        '''
        Change the state of multiple led by the position in the grid
        elems must be an iterable object and its elements must be of the form:
            (n_led, r, g, b)
        '''
        # Lastly we append the new state
        self.states.append(elems)

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

        # Optimize the progression
        op_radial_items = []
        current = []
        for item in radial_items:
            current += item
            if len(current) > 10:
                op_radial_items.append(current)
                current = []

        return op_radial_items

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
        prev_leds_on = [i[0] for i in previous_state]

        # Leds that turn off
        leds_turned_off = [i for i in prev_leds_on if i not in actual_leds_on]
        leds_turned_off = [i for i in previous_state if i[0] in leds_turned_off]

        # Leds that turn on
        leds_turned_on = [i for i in actual_leds_on if i not in prev_leds_on]
        leds_turned_on = [i for i in actual_state if i[0] in leds_turned_on]

        for it in range(iterations):
            for led in leds_turned_on:
                n_led = led[0]
                r, g, b = led[1:]
                r = int(r * it / iterations)
                g = int(g * it / iterations)
                b = int(b * it / iterations)

                r = r if r <= 255 else 255
                g = g if g <= 255 else 255
                b = b if b <= 255 else 255

                if n_led <= 99:
                    self.strip[n_led] = (r, g, b)

            for led in leds_turned_off:
                n_led = led[0]
                r, g, b = led[1:]
                r = int(r * (iterations - it) / iterations)
                g = int(g * (iterations - it) / iterations)
                b = int(b * (iterations - it) / iterations)

                r = r if r <= 255 else 255
                g = g if g <= 255 else 255
                b = b if b <= 255 else 255

                if n_led <= 99:
                    self.strip[n_led] = (r, g, b)

            time.sleep(period / iterations)

            self.strip.write()

        # We make sure that all the leds turn off
        for led in leds_turned_off:
            n_led = led[0]

            if n_led <= 99:
                self.strip[n_led] = (0, 0, 0)
                self.strip.write()

    def shape(self):
        return (len(self.grid), len(self.grid[0]))


class Stream:
    def __init__(self, data=[], l_max=9, kwargs={}):
        self.data = data
        self.l_max = l_max
        self.kwargs = kwargs

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

    def last_state(self):
        return self.data[-1]

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):  # Retorna el largo
        return len(self.data)

    def __repr__(self):  # Retorna la lista
        return str(self.data)
