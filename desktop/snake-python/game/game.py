# game/game.py

import pygame

from game.settings import (
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    FPS,
    SNAKE_MOVE_DELAY,
    BACKGROUND_COLOR,
    GRID_COLOR,
    SNAKE_COLOR,
    SNAKE_HEAD_COLOR,
    FOOD_COLOR,
)

from game.snake import Snake
from game.food import Food

from game.collision import (
    check_wall_collision,
    check_self_collision,
    check_food_collision,
)


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()

        self.running = True
        self.game_over = False

        self.snake = Snake()

        self.food = Food(
            GRID_WIDTH,
            GRID_HEIGHT,
        )

        self.food.spawn(self.snake.body)

        self.move_timer = 0

        self.score = 0

    def run(self):
        """
        Bucle principal del juego.
        """

        while self.running:
            delta_time = self.clock.tick(FPS)

            self.handle_events()

            if not self.game_over:
                self.update(delta_time)

            self.render()

        pygame.quit()

    def handle_events(self):
        """
        Procesa eventos de teclado y ventana.
        """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key)

    def handle_key(self, key):
        """
        Procesa las teclas del jugador.
        """

        if key == pygame.K_UP:
            self.snake.change_direction((0, -1))

        elif key == pygame.K_DOWN:
            self.snake.change_direction((0, 1))

        elif key == pygame.K_LEFT:
            self.snake.change_direction((-1, 0))

        elif key == pygame.K_RIGHT:
            self.snake.change_direction((1, 0))

        elif key == pygame.K_w:
            self.snake.change_direction((0, -1))

        elif key == pygame.K_s:
            self.snake.change_direction((0, 1))

        elif key == pygame.K_a:
            self.snake.change_direction((-1, 0))

        elif key == pygame.K_d:
            self.snake.change_direction((1, 0))

        elif key == pygame.K_ESCAPE:
            self.running = False

    def update(self, delta_time):
        """
        Actualiza el estado del juego.
        """

        self.move_timer += delta_time

        if self.move_timer < SNAKE_MOVE_DELAY:
            return

        self.move_timer = 0

        # Comprobamos si la próxima posición
        # contiene comida.
        head_x, head_y = self.snake.head

        dx, dy = self.snake.next_direction

        next_position = (
            head_x + dx,
            head_y + dy,
        )

        will_grow = next_position == self.food.position

        self.snake.move(grow=will_grow)

        # Colisión con las paredes
        if check_wall_collision(
            self.snake.head,
            GRID_WIDTH,
            GRID_HEIGHT,
        ):
            self.game_over = True
            return

        # Colisión consigo misma
        if check_self_collision(self.snake):
            self.game_over = True
            return

        # Comida
        if will_grow:
            self.score += 1

            self.food.spawn(self.snake.body)

    def render(self):
        """
        Dibuja el juego.
        """

        self.screen.fill(BACKGROUND_COLOR)

        self.draw_grid()
        self.draw_food()
        self.draw_snake()

        pygame.display.flip()

    def draw_grid(self):
        """
        Dibuja la cuadrícula del tablero.
        """

        for x in range(GRID_WIDTH + 1):

            pixel_x = x * CELL_SIZE

            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (pixel_x, 0),
                (pixel_x, WINDOW_HEIGHT),
            )

        for y in range(GRID_HEIGHT + 1):

            pixel_y = y * CELL_SIZE

            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (0, pixel_y),
                (WINDOW_WIDTH, pixel_y),
            )

    def draw_snake(self):
        """
        Dibuja todos los segmentos de la serpiente.
        """

        for index, position in enumerate(self.snake.body):

            x, y = position

            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )

            if index == 0:
                color = SNAKE_HEAD_COLOR
            else:
                color = SNAKE_COLOR

            pygame.draw.rect(
                self.screen,
                color,
                rect,
            )

    def draw_food(self):
        """
        Dibuja la comida.
        """

        x, y = self.food.position

        rect = pygame.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )

        pygame.draw.rect(
            self.screen,
            FOOD_COLOR,
            rect,
        )
