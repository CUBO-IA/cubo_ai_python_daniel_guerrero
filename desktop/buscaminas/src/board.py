import random

from .cell import Cell


class Board:
    def __init__(self, rows=9, columns=9, mines=10):
        self.rows = rows
        self.columns = columns
        self.mines = mines

        self.cells = [
            [Cell() for _ in range(columns)]
            for _ in range(rows)
        ]

        self.generate_mines()
        self.calculate_numbers()

    def generate_mines(self):
        total_cells = self.rows * self.columns

        mine_positions = random.sample(
            range(total_cells),
            self.mines
        )

        for position in mine_positions:
            row = position // self.columns
            column = position % self.columns

            self.cells[row][column].has_mine = True

    def get_neighbors(self, row, column):
        neighbors = []

        for row_offset in (-1, 0, 1):
            for column_offset in (-1, 0, 1):

                # No contar la propia casilla
                if row_offset == 0 and column_offset == 0:
                    continue

                neighbor_row = row + row_offset
                neighbor_column = column + column_offset

                # Comprobar límites
                if not (
                    0 <= neighbor_row < self.rows
                    and 0 <= neighbor_column < self.columns
                ):
                    continue

                neighbors.append(
                    (neighbor_row, neighbor_column)
                )

        return neighbors

    def calculate_numbers(self):
        for row in range(self.rows):
            for column in range(self.columns):

                cell = self.cells[row][column]

                # Las minas no necesitan número
                if cell.has_mine:
                    continue

                mine_count = 0

                for neighbor_row, neighbor_column in self.get_neighbors(
                    row,
                    column
                ):
                    neighbor = self.cells[
                        neighbor_row
                    ][
                        neighbor_column
                    ]

                    if neighbor.has_mine:
                        mine_count += 1

                cell.adjacent_mines = mine_count

    def reveal(self, row, column):
        cell = self.cells[row][column]

        if cell.is_revealed:
            return []

        if cell.is_flagged:
            return []

        revealed_cells = []

        self._reveal_recursive(
            row,
            column,
            revealed_cells
        )

        return revealed_cells

    def _reveal_recursive(
        self,
        row,
        column,
        revealed_cells
    ):
        # Comprobar límites
        if not (
            0 <= row < self.rows
            and 0 <= column < self.columns
        ):
            return

        cell = self.cells[row][column]

        # No descubrir casillas ya descubiertas
        if cell.is_revealed:
            return

        # No descubrir casillas marcadas
        if cell.is_flagged:
            return

        cell.is_revealed = True

        revealed_cells.append(
            (row, column)
        )

        # Si hay mina, terminar
        if cell.has_mine:
            return

        # Si tiene minas alrededor, no expandir
        if cell.adjacent_mines > 0:
            return

        # Si tiene 0 minas alrededor,
        # descubrir automáticamente vecinos
        for neighbor_row, neighbor_column in self.get_neighbors(
            row,
            column
        ):
            neighbor = self.cells[
                neighbor_row
            ][
                neighbor_column
            ]

            if neighbor.has_mine:
                continue

            self._reveal_recursive(
                neighbor_row,
                neighbor_column,
                revealed_cells
            )

    def toggle_flag(self, row, column):
        cell = self.cells[row][column]

        if cell.is_revealed:
            return False

        cell.is_flagged = not cell.is_flagged

        return cell.is_flagged

    def reveal_all_mines(self):
        for row in range(self.rows):
            for column in range(self.columns):

                cell = self.cells[row][column]

                if cell.has_mine:
                    cell.is_revealed = True

    def count_flags(self):
        count = 0

        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].is_flagged:
                    count += 1

        return count

    def count_revealed_safe_cells(self):
        count = 0

        for row in range(self.rows):
            for column in range(self.columns):

                cell = self.cells[row][column]

                if cell.is_revealed and not cell.has_mine:
                    count += 1

        return count

    def total_safe_cells(self):
        return (
            self.rows * self.columns
            - self.mines
        )
