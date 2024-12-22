import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scorebar Example")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TR = (0, 0, 0, 0)

# Fonts
font = pygame.font.Font(None, 20)

# Initialize score
score = 0

# Function to display the scorebar
def draw_scorebar(score):
    text = font.render(f"Score: {score}", True, WHITE)  # Score text
    screen.blit(text, (10, 10)) # Display score at the top-left corner
    for event in pygame.event.get():
        if event.type == pygame.K_SPACE:
            score =+ 1
            pygame.display.update()
    
    if score == 10:
            text = font.render(f"YOU WIN!!!!", True, WHITE)  # Score text
            screen.blit(text, (400, 300))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()


    


# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Background color for game area

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Example score increment when a key is pressed
        elif event.type == pygame.KEYDOWN:
            score += 1

    # Draw the scorebar
    draw_scorebar(score)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
