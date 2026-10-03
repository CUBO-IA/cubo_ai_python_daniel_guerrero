from .board import Board


class Game:
    def __init__(
        self,
        rows=9,
        columns=9,
        mines=10
    ):
        self.rows = rows
        self.columns = columns
        self.mines = mines

        self.board = None

        self.game_over = False
        self.won = False

        self.new_game()

    def new_game(self):
        self.board = Board(
            rows=self.rows,
            columns=self.columns,
            mines=self.mines
        )

        self.game_over = False
        self.won = False

    def reveal(self, row, column):
        if self.game_over:
            return {
                "result": "game_over",
                "cells": []
            }

        cell = self.board.cells[row][column]

        if cell.is_flagged:
            return {
                "result": "flagged",
                "cells": []
            }

        revealed_cells = self.board.reveal(
            row,
            column
        )

        # Si la casilla descubierta es una mina
        if cell.has_mine:
            self.game_over = True

            self.board.reveal_all_mines()

            return {
                "result": "lost",
                "cells": revealed_cells
            }

        # Comprobar victoria
        if (
            self.board.count_revealed_safe_cells()
            == self.board.total_safe_cells()
        ):
            self.game_over = True
            self.won = True

            return {
                "result": "won",
                "cells": revealed_cells
            }

        return {
            "result": "revealed",
            "cells": revealed_cells
        }

    def toggle_flag(self, row, column):
        if self.game_over:
            return False

        return self.board.toggle_flag(
            row,
            column
        )

    def get_cell(self, row, column):
        return self.board.cells[row][column]

    def get_remaining_mines(self):
        return (
            self.mines
            - self.board.count_flags()
        )
