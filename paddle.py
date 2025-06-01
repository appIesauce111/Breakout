import pygame
wall1 = None
BLACK = (0,0,0)
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width * 5, height])
        self.rect = self.image.get_rect()
        self.wall1 = None
    def moveLeft(self, pixels):
        self.rect.x -= (pixels *1.2)
        if self.rect.x < 0:
          self.rect.x = 0
    def moveRight(self, pixels):
        self.rect.x += (pixels * 1.2)
        if self.wall1 is not None:
            max_x = self.wall1 - self.rect.width
            if self.rect.x > max_x:
                self.rect.x = max_x