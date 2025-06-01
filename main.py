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
GREEN = (0, 255, 0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)
score = 0
lives = 10
levelcomp = None
bg = (800, 600)
def play_level(bg, pwidth, phigh, bbg, brickrs, brickcs, wall1, wall2, wall3):
    screen = pygame.display.set_mode(bg)
    all = pygame.sprite.Group()
    allbs = pygame.sprite.Group()
    paddle = Paddle(RED, pwidth, phigh)
    paddle.rect.x = bg[0] // 2 - pwidth // 2
    paddle.rect.y = bg[1] - 40
    ball = Ball(WHITE, bbg, bbg)
    ball.rect.x = bg[0] // 2 - bbg // 2
    ball.rect.y = bg[1] // 2
    all.add(paddle)
    all.add(ball)
    greenies = random.sample(range(brickcs), 2)
    for row in range(brickrs):
        greenies = random.sample(range(brickcs), 2) 
        for i in range(brickcs):
            if i in greenies: 
                brick = Brick(GREEN, 80, 30)
                brick.is_slow_brick = True
                brick.hits_left = 3
            else:
                brick = Brick(RED, 80, 30)
                brick.is_slow_brick = False
            brick.rect.x = 60 + i * 95
            brick.rect.y = 60 + row * 45
            all.add(brick)
            allbs.add(brick)

    slowon = False
    slowtime = 0
    carryOn = True
    clock = pygame.time.Clock()
    paddle2 = None
    score = 0
    lives = 10

    while carryOn:
        clock.tick(60 if bg == (800, 600) else 120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    projectile = Projectile(YELLOW, 50, 10)
                    projectile.rect.x = paddle.rect.x + paddle.rect.width // 2 - projectile.rect.width // 2
                    projectile.rect.y = paddle.rect.y - projectile.rect.height
                    all.add(projectile)
                if event.key == pygame.K_2 and paddle2 is None:
                    paddle2 = Paddle(LIGHTBLUE, 100, 10)
                    paddle2.rect.x = 350
                    paddle2.rect.y = 530
                    all.add(paddle2)
                if event.key == pygame.K_w and paddle2 is not None:
                    projectile = Projectile(YELLOW, 50, 10)
                    projectile.rect.x = paddle2.rect.x + paddle2.rect.width // 2 - projectile.rect.width // 2
                    projectile.rect.y = paddle2.rect.y - projectile.rect.height
                    all.add(projectile)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft(5)
        if keys[pygame.K_RIGHT]:
            paddle.moveRight(5)
        if paddle2 is not None and paddle2 in all:
            if keys[pygame.K_a]:
                paddle2.moveLeft(5)
            if keys[pygame.K_d]:
                paddle2.moveRight(5)
        all.update()

        if slowon:
            if ball.velocity[1] > 0:
                ball.velocity[1] = max(1, ball.velocity[1] - 0.05)  
            if time.time() > slowtime:
                slowon = False

        seconds_since_epoch = time.time()
        
        
        if ball.rect.x>=wall1:
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
        if ball.rect.y>wall2:
            ball.velocity[1] = -ball.velocity[1]
            lives -= 1
            if lives == 0:
                font = pygame.font.Font(None, 74)
                text = font.render("GAME OVER", 1, WHITE)
                screen.blit(text, (250,300))
                pygame.display.flip()
                pygame.time.wait(3000)
                carryOn=False
        if ball.rect.y<wall3:
            ball.velocity[1] = -ball.velocity[1]
        if pygame.sprite.collide_mask(ball, paddle):
            ball.rect.x -= ball.velocity[0]
            ball.rect.y -= ball.velocity[1]
            ball.bounce()
        if paddle2 is not None and paddle2 in all:
            if pygame.sprite.collide_mask(ball, paddle2):
                ball.rect.x -= ball.velocity[0]
                ball.rect.y -= ball.velocity[1]
                ball.bounce()
        

        

        for projectile in [i for i in all if isinstance(i, Projectile)]:
            if pygame.sprite.collide_mask(ball, projectile):
                ball.rect.y = projectile.rect.y - ball.rect.height 
                ball.velocity[1] = -abs(max(6, abs(ball.velocity[1])))  
                projectile.kill()

            
        if random.randint(1, 60) == 1: 
            evil_proj = Projectile(ORANGE, 10, 10, direction="down")
            evil_proj.rect.x = random.randint(0, bg[0] - 10)
            evil_proj.rect.y = 0
            all.add(evil_proj)
        for evil_proj in [i for i in all if isinstance(i, Projectile) and getattr(i, "direction", "up") == "down"]:
            if pygame.sprite.collide_mask(paddle, evil_proj):
                lives -= 1 
                evil_proj.kill()
            if pygame.sprite.collide_mask(ball, evil_proj):
                ball.velocity[1] = abs(max(6, abs(ball.velocity[1]))) 
                evil_proj.kill()
        brick_collision_list = pygame.sprite.spritecollide(ball,allbs,False)
        for brick in brick_collision_list:
            ball.bounce()
            score += 1
            if hasattr(brick, "is_slow_brick") and brick.is_slow_brick:
                if not hasattr(brick, "hits_left"):
                    brick.hits_left = 3 
                brick.hits_left -= 1
                if brick.hits_left <= 0:
                    slowon = True
                    slowtime = time.time() + 5
                    brick.kill()
                else:
                    if brick.hits_left == 2:
                        brick.image.fill((100, 200, 100))  
                    elif brick.hits_left == 1:
                        brick.image.fill((200, 255, 200)) 
            else:
                brick.kill()


        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        all.draw(screen)
        pygame.display.flip()


        if len(allbs) == 0:
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200, 300))
            pygame.display.flip()
            pygame.time.wait(2000)
            return True

        if lives == 0:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250, 300))
            pygame.display.flip()
            pygame.time.wait(3000)
            return "game_over"



result = play_level((800, 600), 100, 10, 10, 3, 8, 790, 590, 40)
if result == True:
    play_level((1200, 900), 150, 15, 15, 3, 12, 1600, 590, 60)
