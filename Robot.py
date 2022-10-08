import math

import numpy as np
import pygame

from BaseSprite import BaseSprite


class Robot(pygame.sprite.Sprite):
    GREEN = (0, 255, 0)

    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 100
        self.rotation = 0

        self.movex = 0
        self.movey = 0
        self.moverot = 0

        self.width = 80
        self.height = 80

        self.image = pygame.image.load("robot.png")
        self.image = pygame.transform.scale(self.image, (80, 80))

    def control_move(self, x, y):
        self.movex += x
        self.movey += y

    def control_rot(self, rot):
        self.moverot += rot

    def draw(self, screen):
        screen.blit(*self.rot_center(self.image, self.rotation, self.x, self.y))

    def rot_center(self, image, angle, x, y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

        return rotated_image, new_rect

    def update(self):
        self.x += self.movex
        self.y += self.movey
        self.rotation += self.moverot

    def get_pos(self):
        return self.x, self.y

    def get_normal_vector(self):
        vector = [self.x + math.cos(math.radians(self.rotation)), self.y + math.sin(math.radians(self.rotation))]
        norm = np.linalg.norm(vector)
        return vector / norm
