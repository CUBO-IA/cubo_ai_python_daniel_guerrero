# game/collision.py


def check_wall_collision(position, grid_width, grid_height):
    """
    Comprueba si una posición está fuera
    de los límites del tablero.
    """

    x, y = position

    return (
        x < 0
        or x >= grid_width
        or y < 0
        or y >= grid_height
    )


def check_self_collision(snake):
    """
    Comprueba si la cabeza de la serpiente
    está chocando con su propio cuerpo.
    """

    return snake.head in snake.body[1:]


def check_food_collision(snake, food):
    """
    Comprueba si la cabeza de la serpiente
    está encima de la comida.
    """

    return snake.head == food.position
