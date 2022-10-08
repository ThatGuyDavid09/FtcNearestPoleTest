import pygame

from BaseSprite import BaseSprite


class SpecialRect(BaseSprite):
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    def __init__(self, rect, mode):
        super().__init__()
        self.rect = pygame.Rect(*rect)
        self.mode = mode

    def draw(self, surface):
        pygame.draw.rect(surface, self.BLUE, self.rect, self.mode)
