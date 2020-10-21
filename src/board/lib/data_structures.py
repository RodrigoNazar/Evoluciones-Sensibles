info = '''
data estructures module
'''


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.state = self.gen_state_grid()

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

    # Returns a list of the equal radial leds
    def radial_progression(self):
        pass
