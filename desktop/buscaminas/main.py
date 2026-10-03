import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.ui import MinesweeperWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("Buscaminas")
    app.setApplicationDisplayName("Buscaminas")
    app.setDesktopFileName("buscaminas")

    icon_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets",
        "icon.png"
    )

    app.setWindowIcon(
        QIcon(icon_path)
    )

    window = MinesweeperWindow(
        rows=9,
        columns=9,
        mines=10
    )

    window.setWindowIcon(
        QIcon(icon_path)
    )

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
