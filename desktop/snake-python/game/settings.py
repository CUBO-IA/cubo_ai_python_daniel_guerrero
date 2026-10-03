# game/settings.py


# =========================
# VENTANA
# =========================

CELL_SIZE = 32

GRID_WIDTH = 25
GRID_HEIGHT = 18

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

WINDOW_TITLE = "Snake"


# =========================
# JUEGO
# =========================

FPS = 60

SNAKE_MOVE_DELAY = 120  # milisegundos


# =========================
# COLORES
# =========================

BACKGROUND_COLOR = (20, 20, 20)

GRID_COLOR = (35, 35, 35)

SNAKE_COLOR = (80, 200, 120)

SNAKE_HEAD_COLOR = (110, 230, 150)

FOOD_COLOR = (220, 70, 70)
