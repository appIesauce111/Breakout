#Import the pygame library and initialise the game engine
import pygame
import time
#Let's import the Paddle Class & the Ball Class
from paddle import Paddle
from ball import Ball
from brick import Brick
from projectile import Projectile
pygame.init()
# Define some colors
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)
score = 0
lives = 10
# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
#Create the Paddle
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
# Add the paddle and the ball to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)
# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
    #Moving the paddle when the use uses the arrow keys
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
    # --- Game logic should go here
    all_sprites_list.update()
    #Check if the ball is bouncing against any of the 4 walls:

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
            ball.rect.y -= ball.velocity[1]
            ball.bounce()
            if ball.velocity[1] < 0:
                ball.velocity[1] = -abs(max(6, abs(ball.velocity[1])))
            else:
                ball.velocity[1] = abs(max(6, abs(ball.velocity[1])))
            projectile.kill()
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