import pygame
from random import randint
BLACK = (0, 0, 0)
 
class Ball(pygame.sprite.Sprite):
    
    
    def __init__(self, color, width, height):
        
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [randint(4,8),randint(-8,8)]
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
          
    def bounce(self):
        self.velocity[1] = -self.velocity[1]
        if self.velocity[0] == 0:
            self.velocity[0] = randint(2, 4)
        else:
            self.velocity[0] += randint(-1, 1)
        # Prevent horizontal velocity from being too small
        if 0 < abs(self.velocity[0]) < 2:
            if self.velocity[0] > 0:
                self.velocity[0] = 2
            else:
                self.velocity[0] = -2
        if self.velocity[0] > 8:
            self.velocity[0] = 8
        if self.velocity[0] < -8:
            self.velocity[0] = -8