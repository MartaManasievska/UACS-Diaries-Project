import pygame
import sys
import os

# def run_srekja_scene():
pygame.init()

#Screen setup
WIDTH , HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Srekja Scene")
clock = pygame.time.Clock()

#Fonts 
custom_font_path = "Tagesschrift-Regular.ttf"
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
        positions[name] = (100 + i * 170, 250)

# Background
background = pygame.image.load(os.path.join('images', 'izlet.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))



# Main loop
running = True
while running:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not fade_out:
            mx, my = pygame.mouse.get_pos()
            for name in characters:
                x, y = positions[name]
                if pygame.Rect(x, y, 120, 120).collidepoint(mx, my):
                    handle_click(name)

            if confirm_rect.collidepoint(mx, my) and selected_character:
                fade_out = True

    if fade_out:
        fade_alpha += 5
        if fade_alpha >= 255:
            running = False

    clock.tick(60)

pygame.quit()