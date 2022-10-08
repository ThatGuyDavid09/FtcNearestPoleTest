import pygame


class Robot(pygame.sprite.Sprite):
    """
    This class represents our user controlled character.
    """

    def __init__(self, pos, image, speed=100, *groups):
        super(Robot, self).__init__(*groups)
        self.speed = speed  # px/seg
        self.max_speed = 600
        self.acc = 85  # px/s^2
        self.dec = 150
        self.angle = 90
        self.source_image = pygame.transform.rotozoom(image, 0, prepare.SCALE_FACTOR)
        self.image = pygame.transform.rotate(self.source_image, self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.hit_rect = self.rect.inflate(-20, -20)
        self.hit_rect.center = self.rect.center
        self.pos = list(pos)
        self.dx = 0.0
        self.dy = 0.0

    def update(self, keys, bounding, obstacles, dt):
        """
        Updates the players position based on currently held keys.
        """
        for key in prepare.DIRECT_DICT:
            if keys[key]:
                self.dx = prepare.DIRECT_DICT[key][0] * math.cos(self.angle * GRAD)
                self.dy = prepare.DIRECT_DICT[key][1] * math.sin(self.angle * GRAD)
                Smoke(self.rect.center, -self.dy, -self.dx, self.gfx_group)

        if any((keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_e], keys[pygame.K_q])):
            if self.speed < self.max_speed:
                self.speed += self.acc * dt
        else:
            if self.speed > 100:
                self.speed -= self.dec * dt
            else:
                self.dx = 0.0
                self.dy = 0.0

        self.pos[0] += self.dx * self.speed * dt
        self.pos[1] += self.dy * self.speed * dt
        self.rect.center = self.pos

        rotate_factor = 0
        if keys[pygame.K_LEFT]:
            rotate_factor += 1
        if keys[pygame.K_RIGHT]:
            rotate_factor -= 1

        if rotate_factor != 0:
            self.angle += rotate_factor
            self.image = pygame.transform.rotate(self.source_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.centerx = round(self.pos[0], 0)
            self.rect.centery = round(self.pos[1], 0)

        self.wrap_in_screen(bounding)
        self.check_collisions(obstacles)

    def check_collisions(self, obstacles):
        collision = pygame.sprite.spritecollideany(self, obstacles,
                                                   collided=tools.hit_rect_collision)
        if collision:
            for _ in range(50):
                RedFragment(self.pos, self.gfx_group)
            self.kill()

    def wrap_in_screen(self, bounding):
        buffer = 50
        if self.rect.centerx < bounding.left - buffer:
            self.rect.centerx = bounding.right + buffer
        elif self.rect.centerx > bounding.right + buffer:
            self.rect.centerx = bounding.left - buffer
        elif self.rect.centery < bounding.top - buffer:
            self.rect.centery = bounding.bottom + buffer
        elif self.rect.centery > bounding.bottom + buffer:
            self.rect.centery = bounding.top - buffer

        self.hit_rect.center = self.rect.center
        self.pos = list(self.rect.center)

    def draw(self, surface):
        """
        Basic draw function. (not  used if drawing via groups)
        """
        surface.blit(self.image, self.rect)
