import pygame
import sys
import time

# Initialize Pygame
pygame.init()



# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("UACS Diaries - Loading")

# Load background image
background = pygame.image.load("resourses\background_loadingScreen.png")
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
diamond_y_base = height // 2 - 140
diamond_float = 0
diamond_direction = 1  # 1 = moving down, -1 = moving up

# Main loading loop
loading = True
while loading:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    # Update floating
    diamond_float += diamond_direction * 0.5
    if diamond_float > 10 or diamond_float < -10:
        diamond_direction *= -1

    # Draw simple diamond shape
    diamond_x = width // 2
    diamond_y = diamond_y_base + diamond_float
    diamond_points = [
        (diamond_x, diamond_y - 40),
        (diamond_x + 30, diamond_y),
        (diamond_x, diamond_y + 40),
        (diamond_x - 30, diamond_y)
    ]
    pygame.draw.polygon(screen, PASTEL_PINK, diamond_points)

    # Loading text
    text = font.render("Loading...", True, BLACK)
    screen.blit(text, (width//2 - text.get_width()//2, height//2 - 50))

    # Draw loading bar background
    pygame.draw.rect(screen, BLACK, (150, height//2 + 20, 500, 40), 2)

    # Draw loading bar progress (in pastel pink)
    pygame.draw.rect(screen, PASTEL_PINK, (152, height//2 + 22, 5 * progress - 4, 36))

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

    screen.fill(WHITE)

    # Redraw diamond (still, no floating)
    diamond_x = width // 2
    diamond_y = diamond_y_base
    diamond_points = [
        (diamond_x, diamond_y - 40),
        (diamond_x + 30, diamond_y),
        (diamond_x, diamond_y + 40),
        (diamond_x - 30, diamond_y)
    ]
    pygame.draw.polygon(screen, PASTEL_PINK, diamond_points)

    # Redraw "Press any key" text
    continue_text = font.render("Press any key to continue...", True, BLACK)
    screen.blit(continue_text, (width//2 - continue_text.get_width()//2, height//2 - 20))

    pygame.display.update()
    clock.tick(60)

# After pressing key
pygame.quit()
