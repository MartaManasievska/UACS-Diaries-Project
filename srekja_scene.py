import pygame
import sys
import os

def run_srekja_scene():
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Srekja Scene")
    clock = pygame.time.Clock()

    # Fonts
    custom_font_path = 'Tagesschrift-Regular.ttf'
    font_title = pygame.font.Font(custom_font_path, 48)
    font_name = pygame.font.Font(custom_font_path, 28)
    font_button = pygame.font.Font(custom_font_path, 32)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    HIGHLIGHT = (255, 255, 255)

    # Characters and layout
    characters = ["Tina", "Anja", "Sanja", "Marta", "Eva"]
    icons = {}
    positions = {}

    for i, name in enumerate(characters):
        img = pygame.image.load(f"images/{name}_circle_border.png").convert_alpha()
        img = pygame.transform.smoothscale(img, (120, 120))
        icons[name] = img
        positions[name] = (100 + i * 170, 520)  # Adjust Y for below the table

    # Background
    background = pygame.image.load(os.path.join('images', 'srekja_scenario.png')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Main loop
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0, 0))

        # Draw icons
        for name in characters:
            screen.blit(icons[name], positions[name])

        # Title
        title_surface = font_title.render("Srekja Café Meetup", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        pygame.display.flip()

    pygame.quit()

# Run the scene
run_srekja_scene()
