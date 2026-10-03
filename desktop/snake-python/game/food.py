# game/food.py

import random


class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.position = (0, 0)

    def spawn(self, occupied_positions):
        """
        Genera una nueva posición para la comida.

        La comida nunca aparecerá encima
        de la serpiente.
        """

        available_positions = []

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                position = (x, y)

                if position not in occupied_positions:
                    available_positions.append(position)

        if not available_positions:
            return False

        self.position = random.choice(available_positions)

        return True
