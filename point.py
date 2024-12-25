import pygame
import math
from settings import *

class Point:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.selected = False

    def draw(self, screen):
        color = BLUE if self.selected else BLACK
        pygame.draw.circle(screen, color, (self.x, self.y), RADIUS)
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, True, WHITE) 
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)
