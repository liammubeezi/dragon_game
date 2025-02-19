import pygame
#from subprocess import call
import os
from random import randint
pygame.font.init()
import sys
import hard
import inter
import easy
pygame.mixer.init()
WIDTH, HEIGHT = 1500, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAIN MENU")

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
HIGHLIGHT = (0, 255, 255)


font = pygame.font.Font(None, 60)
menu_title = "THIS IS THE DRAGON GAME"
menu_instructions = "Select an option using the arrow keys, Press Enter to select level"

menu_options = ["BEGINNER","INTERMEDIATE", "PRO", "Quit"]
selected_option = 0
loading_sound = pygame.mixer.Sound("dragon_assets/dragon-shout-roar-98277.mp3")

background_image = pygame.image.load(os.path.join('dragon_assets', 'back1.png'))  
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def draw_menu():
   
    screen.blit(background_image, (0, 0))

    title_surface = font.render(menu_title, True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_surface, title_rect)

    
    instruction_surface = font.render(menu_instructions, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, 140))
    screen.blit(instruction_surface, instruction_rect)

    for i, option in enumerate(menu_options):
        color = HIGHLIGHT if i == selected_option else WHITE
        text_surface = font.render(option, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 200 + i * 80))
        screen.blit(text_surface, text_rect)

def main_menu():
    global selected_option
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1 ) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1 ) % len(menu_options)
                elif event.key == pygame.K_RETURN  or event.type==pygame.MOUSEBUTTONDOWN:
                    if selected_option == 0:  
                        print("EASY...")
                        screen.fill(GREEN)
                        text = font.render("game loading...", True, WHITE)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        screen.fill(GREEN)
                        text = font.render("Use WASD for movement, use 'F' to shoot, press 'esc.' for main menu", True, WHITE)
                        sub = font.render("Your goal: kill 25 cows.", True, WHITE)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 40))
                        pygame.display.flip()
                        pygame.time.wait(5000)
                        loading_sound.play()
                        easy.main()
                        running = False 
                    elif selected_option == 1:  
                        print("INTERMEDIATE...")
                        screen.fill(GREEN)
                        text = font.render("game loading...", True, WHITE)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        screen.fill(GREEN)
                        text = font.render("Use WASD for movement, use 'F' to shoot, press 'esc.' for main menu", True, WHITE)
                        below =font.render("The cows are learning to fear you, you're going to have to up your game!", True, WHITE)
                        sub = font.render("Your Goal, Kill 20 cows.", True, WHITE)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                        screen.blit(below, (WIDTH // 2 - below.get_width() // 2, HEIGHT // 2 + 40))
                        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 80))
                        pygame.display.flip()
                        pygame.time.wait(5000)
                        loading_sound.play()
                        inter.new()
                        running = False 
                    elif selected_option == 2:  
                        print("hard...")
                        screen.fill(GREEN)
                        text = font.render("game loading...", True, WHITE)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        screen.fill(GREEN)
                        text = font.render("Use WASD for movement, use 'F' to shoot, press 'esc.' for main menu", True, WHITE)
                        below = font.render("You are now so scary, the cows run from miles away!", True, WHITE)
                        sub = font.render("Your Goal, Kill 15 cows.", True, WHITE)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                        screen.blit(below, (WIDTH // 2 - below.get_width() // 2, HEIGHT // 2 + 40))
                        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 80))
                        pygame.display.flip()
                        pygame.time.wait(5000)
                        loading_sound.play()
                        hard.new()
                        running = False 
                    elif selected_option == 3: 
                        pygame.quit()
                        sys.exit()
                    
                    
                           

        draw_menu()


        pygame.display.flip()


if __name__ == "__main__":
    main_menu()