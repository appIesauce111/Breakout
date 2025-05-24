import pygame
from random import randint
BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, color, (width // 2, height // 2), width // 2)
        self.velocity = [randint(4,8),randint(-8,8)]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) 

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]
        if self.velocity[0] == 0:
            self.velocity[0] = randint(2, 4)
        else:
            self.velocity[0] += randint(-1, 1)
        if 0 < abs(self.velocity[0]) < 2:
            if self.velocity[0] > 0:
                self.velocity[0] = 2
            else:
                self.velocity[0] = -2
        if self.velocity[0] > 8:
            self.velocity[0] = 8
        if self.velocity[0] < -8:
            self.velocity[0] = -8