import pygame
import os
from random import randint
import sys
import level
WIDTH, HEIGHT = 1500, 800
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First, Game!")


FPS = 60

VEL = 8
FIRE_VEL = 40
TARGET_VEL = 3

WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0) 
BLUE = (0, 0, 225)
ORANGE = (255, 165, 0)
TR = (0, 0, 0, 0)

DRAG_VERT = 50
DRAG_HORI = 50
DRAG_HEI = 40
DRAG_WID = 40

DRAG_TAIL_WID = 100
DRAG_TAIL_HEI = 150
DRAG_TAIL_HORI = DRAG_HORI + 11
DRAG_TAIL_VERT = DRAG_VERT - DRAG_TAIL_HEI

TARGET_WID, TARGET_HEI = 60, 60

TARGET_HIT = pygame.USEREVENT + 1
DRAGON_HIT = pygame.USEREVENT + 2

BACK = pygame.image.load(os.path.join('dragon_assets', 'back_lvl3.png'))
BACK = pygame.transform.scale(BACK, (WIDTH, HEIGHT))

TARGET = pygame.image.load(os.path.join('dragon_assets', 'target.png'))
TARGET = pygame.transform.scale(TARGET, (TARGET_WID, TARGET_HEI))

text_font = pygame.font.SysFont("Helvetica", 100)
font = pygame.font.Font(None, 30)
boundary = "You Lose"
win = "Victory!"
fire_sound = pygame.mixer.Sound("dragon_assets/Grenade+1.mp3")
collide_sound=pygame.mixer.Sound("dragon_assets/Gun+Silencer.mp3")

def new():
    dragon = pygame.Rect(DRAG_HORI, DRAG_VERT, DRAG_WID, DRAG_HEI)
    dragon_tail = pygame.Rect(DRAG_TAIL_HORI, DRAG_TAIL_VERT, DRAG_TAIL_WID, DRAG_TAIL_HEI)
    rotation = 0
    score = 0
    dragon_fire = []
    target_spawn = []
    repeat = ['down']
    
    
    
    clock = pygame.time.Clock()
    run = True
    
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #quit event
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fire_sound.play()
                    if rotation == 270:
                        fire = pygame.Rect(dragon.x, dragon.y + DRAG_HEI//2, 30, 10)    #fix fire launch origin
                        dragon_fire.append(('left', fire))
                    if rotation == 90:
                        fire = pygame.Rect(dragon.x + DRAG_WID, dragon.y + DRAG_HEI//2, 30, 10)
                        dragon_fire.append(('right', fire))
                    if rotation == 180:
                        fire = pygame.Rect(dragon.x + DRAG_WID//2, dragon.y, 10, 30)
                        dragon_fire.append(('up', fire))
                    if rotation == 0:
                        fire = pygame.Rect(dragon.x + DRAG_WID//2, dragon.y + DRAG_HEI, 10, 30)
                        dragon_fire.append(('down', fire))
                if event.key == pygame.K_ESCAPE:
                      level.main_menu() 
            TARGET_SPAWN_X = randint(0, WIDTH - TARGET_WID - 1)
            TARGET_SPAWN_Y = randint(0, HEIGHT - TARGET_HEI - 1)
            target = pygame.Rect(TARGET_SPAWN_X, TARGET_SPAWN_Y, 60, 60)
            trigger = randint(0, 100)
            if trigger < int(20) and len(target_spawn) < 12:
                target_spawn.append(target) 
            if event.type == TARGET_HIT:
                target_spawn.remove(target)                                 #<-------------------------add new target
        
        for target in target_spawn[:]:
            if target.colliderect(dragon):
                pygame.event.post(pygame.event.Event(DRAGON_HIT))
        
        if event.type == DRAGON_HIT:
            collide_sound.play()
            draw_text(boundary, text_font, BLACK, 220, 150)
            pygame.display.update()
            pygame.time.delay(2000)
            level.main_menu()
        
        if repeat[-1] == 'left' in repeat and dragon.x - VEL > 0:
            dragon.x -= VEL 
            dragon_tail.x -= VEL
        elif repeat[-1] == 'right' in repeat and dragon.x + 50 + VEL < WIDTH:
            dragon.x += VEL
            dragon_tail.x += VEL
        elif repeat[-1] == 'up' in repeat and dragon.y - VEL > 0:
            dragon.y -= VEL
            dragon_tail.y -= VEL
        elif repeat[-1] == 'down' in repeat  and dragon.y + DRAG_HEI + VEL < HEIGHT:
            dragon.y += VEL
            dragon_tail.y += VEL
            
        if dragon.x <= 2:
            collide_sound.play()
            draw_text(boundary, text_font, BLACK, 220, 150)
            pygame.display.update()
            pygame.time.delay(2000)
            level.main_menu()
            break

        elif dragon.x >= WIDTH - 20 - DRAG_HEI:
            collide_sound.play()
            draw_text(boundary, text_font, BLACK, 220, 150)
            pygame.display.update()
            pygame.time.delay(2000)
            level.main_menu()
            break 
    
        elif dragon.y <= 2:
            collide_sound.play()
            draw_text(boundary, text_font, BLACK, 220, 150)
            pygame.display.update()
            pygame.time.delay(2000)
            level.main_menu()
            break

        elif dragon.y >= HEIGHT - 4 - DRAG_HEI:
            collide_sound.play()
            draw_text(boundary, text_font, BLACK, 220, 150)
            pygame.display.update()
            pygame.time.delay(2000)
            level.main_menu() 
            break

        handle_target(target_spawn, dragon)    
        keys_pressed = pygame.key.get_pressed()
        rotation = handle_dragon_move(keys_pressed, rotation, repeat)
        score = handle_fire(dragon_fire, target_spawn, score)
        update_tail_postion(rotation, dragon_tail, dragon)
        draw_window(dragon, rotation, dragon_fire, target, target_spawn, dragon_tail, score)
        draw_scorebar(score)
    new()


def draw_window(dragon, rotation, dragon_fire, target, target_spawn, dragon_tail, score):
    DRAGON = pygame.image.load(os.path.join('dragon_assets', 'dragon_head.png'))
    DRAGON = pygame.transform.rotate(pygame.transform.scale(DRAGON, (DRAG_WID, DRAG_HEI)), rotation)

    DRAGON_TAIL = pygame.image.load(os.path.join('dragon_assets', 'body.png'))
    DRAGON_TAIL = pygame.transform.rotate(pygame.transform.scale(DRAGON_TAIL, (DRAG_TAIL_WID, DRAG_TAIL_HEI)), rotation + int(180))
    DRAGON_TAIL.set_colorkey((225, 225, 225))
    
    FIRE = pygame.image.load(os.path.join('dragon_assets', 'fire.png'))
    FIRE = pygame.transform.rotate(pygame.transform.scale(FIRE, (30, 50)), rotation)
    
    WIN.blit(BACK, (0, 0))
    text = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(text, (20, 20))
    for _, fire in dragon_fire:
        WIN.blit(FIRE, (fire.x, fire.y))
    for target in target_spawn:
        WIN.blit(TARGET, (target.x, target.y))
    WIN.blit(DRAGON, (dragon.x, dragon.y))
    WIN.blit(DRAGON_TAIL, (dragon_tail.x, dragon_tail.y))

    pygame.display.update()

def draw_scorebar(score):
    if score == 15:
        draw_text(win, text_font, BLUE, 220, 150)
        pygame.display.update()
        pygame.time.delay(2000)
        level.main_menu()

def handle_dragon_move(keys_pressed, rotation, repeat):                                  
    if keys_pressed[pygame.K_a]: #left
       repeat.append('left')
       if 'right' in repeat: 
           repeat.remove('right')
       if 'up' in repeat:
            repeat.remove('up')
       if 'down' in repeat:
            repeat.remove('down')
       return 270
    elif keys_pressed[pygame.K_d]: #right
        repeat.append('right')
        if 'left' in repeat: 
           repeat.remove('left')
        if 'up' in repeat:
            repeat.remove('up')
        if 'down' in repeat:
            repeat.remove('down')
        return 90
    elif keys_pressed[pygame.K_w]: #up
        repeat.append('up')
        if 'right' in repeat: 
           repeat.remove('right')
        if 'left' in repeat:
            repeat.remove('left')
        if 'down' in repeat:
            repeat.remove('down')
        return 180
    elif keys_pressed[pygame.K_s]:
         repeat.append('down')
         if 'right' in repeat: 
           repeat.remove('right')
         if 'up' in repeat:
            repeat.remove('up')
         if 'left' in repeat:
            repeat.remove('left')
         return 0
    return rotation



def update_tail_postion(rotation, dragon_tail, dragon):
    if rotation == 270:
        dragon_tail.x = dragon.x + DRAG_HEI
        dragon_tail.y = dragon.y - 30
    elif rotation == 90:
        dragon_tail.x = dragon.x - DRAG_TAIL_HEI
        dragon_tail.y = dragon.y - 30
    elif rotation == 180:
        dragon_tail.x = dragon.x - 30
        dragon_tail.y = dragon.y + DRAG_HEI
    elif rotation == 0:
        dragon_tail.x = dragon.x - 30
        dragon_tail.y = dragon.y - DRAG_TAIL_HEI



def handle_fire(dragon_fire, target_spawn, score):
    for direction, fire in dragon_fire[:]: 
        if direction == 'left':
            fire.x -= FIRE_VEL
        elif direction == 'right':
            fire.x += FIRE_VEL
        elif direction == 'up':
            fire.y -= FIRE_VEL
        elif direction == 'down':
            fire.y += FIRE_VEL

        if fire.x < 0 or fire.x > WIDTH or fire.y < 0 or fire.y > HEIGHT:
            dragon_fire.remove((direction, fire))
            continue

        for target in target_spawn[:]:
            if fire.colliderect(target):
                target_spawn.remove(target) 
                dragon_fire.remove((direction, fire)) 
                score += 1  
                break  
    return score



def handle_target(target_spawn, dragon):
    for target in target_spawn[:]:  
        if dragon.x - int(120) < target.x < dragon.x and target.x - 2 - TARGET_VEL > DRAG_HEI:
                target.x -= TARGET_VEL #left
        elif dragon.x < target.x < dragon.x + int(120) and target.x + TARGET_WID + TARGET_VEL < WIDTH - DRAG_HEI:    
                target.x += TARGET_VEL #right
        elif dragon.y - int(120) < target.y < dragon.y and target.y - 2 - TARGET_VEL > DRAG_HEI:    
                target.y -= TARGET_VEL #up
        elif dragon.y < target.y < dragon.y + int(120) and target.y + TARGET_HEI + TARGET_VEL < HEIGHT - DRAG_HEI:    
                target.y += TARGET_VEL #down


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  winner = font.render(text, True, text_col)
  WIN.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - 150//2))
  WIN.blit(winner, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - 150//2))
    

if __name__ == "__main__":
    new()

