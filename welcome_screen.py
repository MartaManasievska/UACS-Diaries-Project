import pygame
import sys
from selection_screen import run_selection_screen
import os

# Initialize Pygame
pygame.init()

# Load diamond image
diamond_img = pygame.image.load(os.path.join('images', 'diamond.png'))
diamond_img = pygame.transform.scale(diamond_img, (110, 140))  # adjust size if needed




# Set up display
width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("UACS Diaries - Loading")

# Load background image
background = pygame.image.load(os.path.join('images', 'background_loadingScreen.jpg'))
background = pygame.transform.scale(background, (width, height))  # Make sure it fits screen


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PASTEL_PINK = (255, 182, 193)  # Soft pink color

# Fonts
font = pygame.font.Font("Tagesschrift-Regular.ttf", 40)


# Clock
clock = pygame.time.Clock()

# Loading variables
progress = 0
loading_speed = 1

# Diamond variables (simple up and down floating)
diamond_y_base = height // 2 - 200
diamond_float = 0
diamond_direction = 1  # 1 = moving down, -1 = moving up

# Main loading loop
loading = True
while loading:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    # Update floating
    diamond_float += diamond_direction * 0.5
    if diamond_float > 10 or diamond_float < -10:
        diamond_direction *= -1

    # Draw simple diamond shape
    diamond_x = width // 2 - diamond_img.get_width() // 2
    diamond_y = diamond_y_base + diamond_float  # or just diamond_y_base when it's not floating
    screen.blit(diamond_img, (diamond_x, diamond_y))


    # Loading text
    text = font.render("Loading...", True, BLACK)
    screen.blit(text, (width//2 - text.get_width()//2, height//2 - 50))

    # Draw loading bar background
    pygame.draw.rect(screen, BLACK, (230, height//2 + 20, 500, 40), 2)

    # Draw loading bar progress (in pastel pink)
    pygame.draw.rect(screen, PASTEL_PINK, (232, height//2 + 22, 5 * progress - 4, 36))

    # Update progress
    progress += loading_speed
    if progress > 100:
        loading = False

    pygame.display.update()
    clock.tick(60)

# After loading is done - "Press any key to continue"
waiting_for_key = True
while waiting_for_key:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            waiting_for_key = False

    screen.blit(background, (0, 0))

 


   # Floating effect
    diamond_float += diamond_direction * 0.5
    if diamond_float > 10 or diamond_float < -10:
        diamond_direction *= -1

    diamond_x = width // 2 - diamond_img.get_width() // 2
    diamond_y = diamond_y_base + diamond_float
    screen.blit(diamond_img, (diamond_x, diamond_y))


    # Redraw "Press any key" text
    continue_text = font.render("Press any key to continue...", True, BLACK)
    screen.blit(continue_text, (width//2 - continue_text.get_width()//2, height//2 - 20))

    pygame.display.update()
    clock.tick(60)

# FLIP ROTATION EFFECT
original = screen.copy()

for angle in range(0, 361, 10):
    rotated = pygame.transform.rotozoom(original, angle, 1)
    rect = rotated.get_rect(center=(width // 2, height // 2))
    screen.fill((0, 0, 0))
    screen.blit(rotated, rect.topleft)
    pygame.display.update()
    pygame.time.delay(10)

# FADE TO BLACK EFFECT
fade_surface = pygame.Surface((width, height))
fade_surface.fill((0, 0, 0))

for alpha in range(0, 256, 10):
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))
    pygame.display.update()
    pygame.time.delay(20)

# Move to the next screen
run_selection_screen()

  

