import pygame
BLACK = (0,0,0)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, color, width, height, direction="up"):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.direction = direction
        self.velocity = 5
    def fire(self, pixels):
        self.rect.y -= pixels
        if self.rect.x > 100:
          self.rect.x = 0
    def update(self):
        if self.direction == "up":
            self.rect.y -= self.velocity
        else:  # "down"
            self.rect.y += self.velocity
        # Remove if off screen
        if self.rect.y < 0 or self.rect.y > 600:
            self.kill()