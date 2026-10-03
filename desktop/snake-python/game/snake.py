# game/snake.py


class Snake:
    def __init__(self):
        self.body = [
            (10, 8),
            (9, 8),
            (8, 8),
        ]

        self.direction = (1, 0)
        self.next_direction = (1, 0)

    @property
    def head(self):
        return self.body[0]

    def change_direction(self, direction):
        """
        Cambia la dirección de movimiento.

        Evita que la serpiente pueda girar
        directamente en sentido contrario.
        """

        dx, dy = direction
        current_dx, current_dy = self.direction

        # Evitar movimiento directamente contrario
        if dx == -current_dx and dy == -current_dy:
            return

        self.next_direction = direction

    def move(self, grow=False):
        """
        Mueve la serpiente una celda.
        """

        self.direction = self.next_direction

        head_x, head_y = self.head
        dx, dy = self.direction

        new_head = (
            head_x + dx,
            head_y + dy,
        )

        self.body.insert(0, new_head)

        if not grow:
            self.body.pop()

    def grow(self):
        """
        Actualmente el crecimiento se controla
        desde move(grow=True).

        Este método queda preparado para
        futuras mejoras.
        """

        self.move(grow=True)

    def occupies(self, position):
        """
        Comprueba si la serpiente ocupa
        una determinada posición.
        """

        return position in self.body
