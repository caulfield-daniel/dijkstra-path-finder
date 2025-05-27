import pygame
import math
from settings import *


class Point:
    """
    Класс, представляющий точку на экране.

    Атрибуты:
    x (int): координата x точки.
    y (int): координата y точки.
    label (str): метка точки.
    selected (bool): флаг, указывающий, выбрана ли точка.
    """

    def __init__(self, x, y, label):
        """
        Инициализирует новый экземпляр класса Point.

        Параметры:
        x (int): координата x точки.
        y (int): координата y точки.
        label (str): метка точки.
        """
        self.x = x
        self.y = y
        self.label = label
        self.selected = False

    def draw(self, screen):
        """
        Рисует точку на экране.

        Параметры:
        screen (pygame.Surface): поверхность, на которой будет нарисована точка.
        """
        color = BLUE if self.selected else BLACK
        pygame.draw.circle(screen, color, (self.x, self.y), RADIUS)
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_distance(self, other):
        """
        Возвращает расстояние между текущей точкой и другой точкой.

        Параметры:
        other (Point): другая точка.

        Возвращает:
        float: расстояние между текущей точкой и другой точкой.
        """
        return math.hypot(self.x - other.x, self.y - other.y)
