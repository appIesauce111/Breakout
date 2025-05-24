import pygame
import time
import random
evil_projectile_timer = 0
from paddle import Paddle
from ball import Ball
from brick import Brick
from projectile import Projectile
pygame.init()
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)
score = 0
lives = 10
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")
all_sprites_list = pygame.sprite.Group()
paddle = Paddle(RED, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560


all_sprites = pygame.sprite.Group() 
#Create the ball sprite
ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195
all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(RED,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(RED,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(RED,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)
all_sprites_list.add(paddle)
all_sprites_list.add(ball)
carryOn = True
clock = pygame.time.Clock()
while carryOn:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
              carryOn = False 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)
    if keys[pygame.K_UP]:
        projectile = None
        if projectile is None or not all_sprites.has(projectile):
            projectile = Projectile(YELLOW, 10, 10)
            projectile.rect.x = paddle.rect.x + paddle.rect.width // 2 - projectile.rect.width // 2
            projectile.rect.y = paddle.rect.y - projectile.rect.height
            all_sprites_list.add(projectile)
            all_sprites.add(projectile)
    all_sprites_list.update()

    seconds_since_epoch = time.time()
    
    
    if ball.rect.x>=790:
        ball.velocity[0] = -ball.velocity[0]
        if seconds_since_epoch % 2 == 0:
            veloc += 5
        else:
            veloc = 1
        if ball.velocity[1] > 0:
            ball.velocity[1] -= veloc  
        else: 
            ball.velocity[1] += veloc
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
        if seconds_since_epoch % 2 == 0:
            veloc += 5
        else:
            veloc = 1
    if ball.rect.y>590:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives == 0:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250,300))
            pygame.display.flip()
            pygame.time.wait(3000)
            carryOn=False
    if ball.rect.y<40:
        ball.velocity[1] = -ball.velocity[1]
    if pygame.sprite.collide_mask(ball, paddle):
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[1]
      ball.bounce()

    

    for projectile in [i for i in all_sprites_list if isinstance(i, Projectile)]:
        if pygame.sprite.collide_mask(ball, projectile):
            ball.rect.y = projectile.rect.y - ball.rect.height 
            ball.velocity[1] = -abs(max(6, abs(ball.velocity[1])))  
            projectile.kill()

        
    if random.randint(1, 60) == 1: 
        evil_proj = Projectile(ORANGE, 10, 10, direction="down")
        evil_proj.rect.x = random.randint(0, size[0] - 10)
        evil_proj.rect.y = 0
        all_sprites_list.add(evil_proj)
        all_sprites.add(evil_proj)
    for evil_proj in [i for i in all_sprites_list if isinstance(i, Projectile) and getattr(i, "direction", "up") == "down"]:
        if pygame.sprite.collide_mask(paddle, evil_proj):
            lives -= 1  # Or any penalty you want
            evil_proj.kill()
        if pygame.sprite.collide_mask(ball, evil_proj):
            ball.velocity[1] = abs(max(6, abs(ball.velocity[1])))  # Bounce ball down
            evil_proj.kill()
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
      ball.bounce()
      score += 1
      brick.kill()
      if len(all_bricks)==0:
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200,300))
            pygame.display.flip()
            pygame.time.wait(3000)
            carryOn=False
    BLACK = (0,0,0)
    screen.fill(BLACK)
    # pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)
    # #Display the score and the number of lives at the top of the screen
    # font = pygame.font.Font(None, 34)
    # text = font.render("Score: " + str(score), 1, WHITE)
    # screen.blit(text, (20,10))
    # text = font.render("Lives: " + str(lives), 1, WHITE)
    # screen.blit(text, (650,10)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()