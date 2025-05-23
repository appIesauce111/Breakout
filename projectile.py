import pygame
BLACK = (0,0,0)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.velocity = [5,5]
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
    def fire(self, pixels):
        self.rect.y -= pixels
        if self.rect.x > 100:
          self.rect.x = 0
    def update(self):
        self.rect.y -= self.velocity[1]