from random import choice, randint
from typing import Optional

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTION_LIST = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс задающий начальное состояние обьектов."""

    def __init__(self,
                 body_color=None,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                 ):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Метод отрисовки объектов на игровом поле."""
        pass

    def draw_rect(self):
        """Метод возвращает заданную прямоугольную область"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        return rect


class Apple(GameObject):
    """Класс яблока.
    Определяет позицию яблока на игровом поле и отрисыввыет его.
    """

    def __init__(self, body_color=APPLE_COLOR):
        self.position = self.randomize_position()
        self.body_color = body_color
        self.length = 1

    def randomize_position(self) -> tuple[int, int]:
        """Метод возвращает случайные координаты яблока на игровом поле."""
        horizontal_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        vertical_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (horizontal_position, vertical_position)
        return self.position

    def draw(self, surface=screen) -> None:
        """Метод отрисовывает яблоко на игровом поле."""
        super().draw_rect()
        pygame.draw.rect(surface, self.body_color, super().draw_rect())
        pygame.draw.rect(surface, BORDER_COLOR, super().draw_rect(), 1)


class Snake(GameObject):
    """Класс змейки.
    Определяет размер, направление движения,
    """

    def __init__(self):
        self.reset()

    def reset(self, surface=screen, length=1, body_color=SNAKE_COLOR) -> None:
        """Метод стирает змейку, возвращает ее в начальное состояние и
        задает направление движения случайным образом.
        """
        rect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = length
        self.direction = choice(DIRECTION_LIST)
        self.body_color = body_color
        self.positions = [self.position]
        self.next_direction = None
        self.last: Optional[tuple] = None

    def update_direction(self) -> None:
        """Метод обновления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод отвечает за движение змейки - добаляет новую
        ячейку змейки в зависимости от направления движения и стирает
        последнюю. Вызывает метод reset при столкновении с собой.
        """
        horizontal_coord, vertical_coord = self.get_head_position()
        movement = GRID_SIZE if (self.direction
                                 in [RIGHT, DOWN]) else - GRID_SIZE
        if self.direction in [DOWN, UP]:
            vertical_coord += movement
        else:
            horizontal_coord += movement
        horizontal_coord %= SCREEN_WIDTH
        vertical_coord %= SCREEN_HEIGHT
        new_head_positions = (horizontal_coord, vertical_coord)
        if new_head_positions in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head_positions)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface=screen) -> None:
        """Метод отрисовывает змейку."""
        for self.position in self.positions[:-1]:
            super().draw_rect()
            pygame.draw.rect(surface, self.body_color, super().draw_rect())
            pygame.draw.rect(surface, BORDER_COLOR, super().draw_rect(), 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Метод возвращающает позицию головы змейки."""
        return self.positions[0]


def handle_keys(game_object) -> None:
    """Функция обрабатывает действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция в которой определяется логика игры."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        # ...
        handle_keys(game_object=snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
