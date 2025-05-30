import pygame
from random import randint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.original_color = color
        self.original_width = width
        self.original_height = height
        self.current_color = color
        self.current_width = width
        self.current_height = height
        
        self.flash_timer = 0
        self.flash_duration = 8  
        self.flash_expansion = 1.5  
        
        self._create_image()
        self.velocity = [randint(4,8), randint(-8,8)]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def _create_image(self):
        self.image = pygame.Surface([self.current_width, self.current_height], pygame.SRCALPHA)
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, self.current_color, (self.current_width // 2, self.current_height // 2), self.current_width // 2)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        

        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0:
                self.current_color = self.original_color
                self.current_width = self.original_width
                self.current_height = self.original_height
                old_center = self.rect.center
                self._create_image()
                self.rect = self.image.get_rect()
                self.rect.center = old_center  
                self.mask = pygame.mask.from_surface(self.image)

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
        
        self._trigger_flash()

    def _trigger_flash(self):
        self.flash_timer = self.flash_duration
        self.current_color = WHITE
        self.current_width = int(self.original_width * self.flash_expansion)
        self.current_height = int(self.original_height * self.flash_expansion)
        old_center = self.rect.center
        self._create_image()
        self.rect = self.image.get_rect()
        self.rect.center = old_center  
        self.mask = pygame.mask.from_surface(self.image)

