from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .game import Game


class CellButton(QPushButton):
    left_clicked = Signal(int, int)
    right_clicked = Signal(int, int)

    def __init__(self, row, column):
        super().__init__()

        self.row = row
        self.column = column

        self.setFixedSize(42, 42)

        self.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_clicked.emit(
                self.row,
                self.column
            )

            event.accept()
            return

        if event.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit(
                self.row,
                self.column
            )

            event.accept()
            return

        super().mousePressEvent(event)


class MinesweeperWindow(QMainWindow):
    def __init__(
        self,
        rows=9,
        columns=9,
        mines=10
    ):
        super().__init__()

        self.rows = rows
        self.columns = columns
        self.mines = mines

        self.game = Game(
            rows=rows,
            columns=columns,
            mines=mines
        )

        self.elapsed_seconds = 0

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_timer
        )

        self.setWindowTitle(
            "Buscaminas"
        )

        self.setMinimumWidth(450)

        self.create_ui()

        self.update_board_ui()

    def create_ui(self):
        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        main_layout.setSpacing(10)

        # ---------------------------------
        # PANEL SUPERIOR
        # ---------------------------------

        top_layout = QHBoxLayout()

        self.mines_label = QLabel(
            "Minas: 10"
        )

        self.mines_label.setFont(
            QFont(
                "Sans",
                12,
                QFont.Weight.Bold
            )
        )

        self.timer_label = QLabel(
            "Tiempo: 00:00"
        )

        self.timer_label.setFont(
            QFont(
                "Sans",
                12,
                QFont.Weight.Bold
            )
        )

        self.new_game_button = QPushButton(
            "Nueva partida"
        )

        self.new_game_button.clicked.connect(
            self.new_game
        )

        top_layout.addWidget(
            self.mines_label
        )

        top_layout.addStretch()

        top_layout.addWidget(
            self.timer_label
        )

        top_layout.addStretch()

        top_layout.addWidget(
            self.new_game_button
        )

        main_layout.addLayout(
            top_layout
        )

        # ---------------------------------
        # MENSAJE
        # ---------------------------------

        self.status_label = QLabel(
            "Haz click en una casilla para comenzar"
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label.setFont(
            QFont(
                "Sans",
                11
            )
        )

        main_layout.addWidget(
            self.status_label
        )

        # ---------------------------------
        # TABLERO
        # ---------------------------------

        board_container = QWidget()

        self.board_layout = QGridLayout(
            board_container
        )

        self.board_layout.setSpacing(2)

        self.buttons = []

        for row in range(self.rows):

            button_row = []

            for column in range(self.columns):

                button = CellButton(
                    row,
                    column
                )

                # Conectar click izquierdo
                button.left_clicked.connect(
                    self.handle_left_click
                )

                # Conectar click derecho
                button.right_clicked.connect(
                    self.handle_right_click
                )

                button_row.append(
                    button
                )

                self.board_layout.addWidget(
                    button,
                    row,
                    column
                )

            self.buttons.append(
                button_row
            )

        main_layout.addWidget(
            board_container,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

    def handle_left_click(
        self,
        row,
        column
    ):
        if self.game.game_over:
            return

        if not self.timer.isActive():
            self.timer.start(1000)

        result = self.game.reveal(
            row,
            column
        )

        result_type = result["result"]

        if result_type == "lost":

            self.status_label.setText(
                "💥 ¡Has perdido!"
            )

            self.timer.stop()

        elif result_type == "won":

            self.status_label.setText(
                "🎉 ¡Has ganado!"
            )

            self.timer.stop()

        elif result_type == "flagged":
            return

        self.update_board_ui()

    def handle_right_click(
        self,
        row,
        column
    ):
        if self.game.game_over:
            return

        if not self.timer.isActive():
            self.timer.start(1000)

        self.game.toggle_flag(
            row,
            column
        )

        self.update_board_ui()

    def update_board_ui(self):
        for row in range(self.rows):

            for column in range(self.columns):

                button = self.buttons[
                    row
                ][
                    column
                ]

                cell = self.game.get_cell(
                    row,
                    column
                )

                # ---------------------------------
                # CASILLA MARCADA
                # ---------------------------------

                if (
                    cell.is_flagged
                    and not cell.is_revealed
                ):

                    button.setText(
                        "🚩"
                    )

                    button.setStyleSheet(
                        """
                        QPushButton {
                            background-color: #3b4252;
                            color: #bf616a;
                            border: 1px solid #4c566a;
                            font-size: 20px;
                            font-weight: bold;
                        }

                        QPushButton:hover {
                            background-color: #434c5e;
                        }
                        """
                    )

                    continue

                # ---------------------------------
                # CASILLA NO DESCUBIERTA
                # ---------------------------------

                if not cell.is_revealed:

                    button.setText("")

                    button.setStyleSheet(
                        """
                        QPushButton {
                            background-color: #3b4252;
                            border: 1px solid #4c566a;
                            border-radius: 3px;
                        }

                        QPushButton:hover {
                            background-color: #434c5e;
                        }

                        QPushButton:pressed {
                            background-color: #2e3440;
                        }
                        """
                    )

                    continue

                # ---------------------------------
                # MINA
                # ---------------------------------

                if cell.has_mine:

                    button.setText(
                        "💣"
                    )

                    button.setStyleSheet(
                        """
                        QPushButton {
                            background-color: #bf616a;
                            border: 1px solid #d08770;
                            font-size: 18px;
                        }
                        """
                    )

                    continue

                # ---------------------------------
                # CASILLA DESCUBIERTA
                # ---------------------------------

                number = cell.adjacent_mines

                button.setText(
                    str(number)
                    if number > 0
                    else ""
                )

                color = self.get_number_color(
                    number
                )

                button.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: #2e3440;
                        border: 1px solid #4c566a;
                        color: {color};
                        font-size: 16px;
                        font-weight: bold;
                    }}
                    """
                )

        self.mines_label.setText(
            f"Minas: {self.game.get_remaining_mines()}"
        )

    def get_number_color(
        self,
        number
    ):
        colors = {
            1: "#88c0d0",
            2: "#a3be8c",
            3: "#bf616a",
            4: "#b48ead",
            5: "#d08770",
            6: "#8fbcbb",
            7: "#eceff4",
            8: "#d8dee9",
        }

        return colors.get(
            number,
            "#eceff4"
        )

    def update_timer(self):
        self.elapsed_seconds += 1

        minutes = (
            self.elapsed_seconds // 60
        )

        seconds = (
            self.elapsed_seconds % 60
        )

        self.timer_label.setText(
            f"Tiempo: {minutes:02d}:{seconds:02d}"
        )

    def new_game(self):
        self.timer.stop()

        self.elapsed_seconds = 0

        self.timer_label.setText(
            "Tiempo: 00:00"
        )

        self.status_label.setText(
            "Haz click en una casilla para comenzar"
        )

        self.game.new_game()

        self.update_board_ui()
