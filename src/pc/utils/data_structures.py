
import math


class Grid:
    def __init__(self, grid, center=(23, 27)):
        self.grid = grid
        self.state = self.gen_state_grid()
        self.center = center
        self.pos_hash = self.gen_pos_hash()

    def gen_state_grid(self):
        state = []

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
        hash = {}

        for i_row, row in enumerate(self.grid):
            for i_col, elem in enumerate(row):
                if elem != 0:
                    hash[elem] = (i_col, i_row)
        return hash

    def get_state_element(self, coord_x, coord_y):
        return self.state[coord_y][coord_x]

    def gen_radial_progression(self):
        '''
        from
        https://www.geeksforgeeks.org/print-a-given-matrix-in-spiral-form/
        '''
        m, n = self.shape()
        k = 0
        l = 0

        radial_items = []

        while (k < m and l < n):
            items = []
            # Print the first row from
            # the remaining rows
            for i in range(l, n):
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
                for i in range(n - 1, (l - 1), -1):
                    if self.grid[m - 1][i] != 0:
                        items.append(self.grid[m - 1][i])

                m -= 1

            # Print the first column from
            # the remaining columns
            if (l < n):
                for i in range(m - 1, k - 1, -1):
                    if self.grid[i][l] != 0:
                        items.append(self.grid[i][l])

                l += 1

            if items:
                radial_items.append(items)

        return radial_items

    def shape(self):
        return (len(self.grid), len(self.grid[0]))
