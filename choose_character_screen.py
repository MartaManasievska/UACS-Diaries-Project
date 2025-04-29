import pygame
import sys
import os

def run_character_selection():
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Character Selection")
    clock = pygame.time.Clock()

    # Fonts
    custom_font_path = "Tagesschrift-Regular.ttf"
    font_title = pygame.font.Font(custom_font_path, 48)
    font_name = pygame.font.Font(custom_font_path, 28)
    font_button = pygame.font.Font(custom_font_path, 32)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (100, 149, 237)
    HIGHLIGHT = (255, 255, 255)

    # Characters and layout
    characters = ["Tina", "Anja", "Sanja", "Marta", "Eva"]
    icons = {}
    positions = {}
    descriptions = {
        "Tina": "Bold and fearless. Loves solving problems with style.",
        "Anja": "Cool and collected. Always ready for a challenge.",
        "Sanja": "Sweet and curious. Loves discovering new things.",
        "Marta": "Friendly and loyal. A dependable companion.",
        "Eva": "Smart and strong. A natural leader."
    }

    # Load and scale icons
    for i, name in enumerate(characters):
        img = pygame.image.load(f"images/{name}_circle_border.png").convert_alpha()
        img = pygame.transform.smoothscale(img, (120, 120))
        icons[name] = img
        positions[name] = (100 + i * 170, 250)

    # Static cloud background
    background = pygame.image.load(os.path.join('images', 'cloud.png')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Button setup
    confirm_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 180, 200, 55)

    # State
    selected_character = None
    fade_out = False
    fade_alpha = 0
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))

    def handle_click(icon_name):
        nonlocal selected_character
        selected_character = icon_name

    def draw():
        screen.blit(background, (0, 0))

        # Title
        title_surf = font_title.render("CHOOSE YOUR CHARACTER", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))

        # Draw character icons and names
        for name in characters:
            x, y = positions[name]
            icon = icons[name].copy()

            # Spotlight effect
            if selected_character and name != selected_character:
                icon.set_alpha(180)  # 70% opacity
            else:
                icon.set_alpha(255)

            screen.blit(icon, (x, y))

            if selected_character == name:
                pygame.draw.circle(screen, HIGHLIGHT, (x + 60, y + 60), 65, 5)

            label = font_name.render(name, True, BLACK)
            screen.blit(label, (x + 60 - label.get_width()//2, y + 130))

        # Description
        if selected_character:
            desc = descriptions[selected_character]
            desc_surf = font_name.render(desc, True, WHITE)
            screen.blit(desc_surf, (WIDTH//2 - desc_surf.get_width()//2, 450))

        # Confirm Button (locked until selection)
        if selected_character:
            pygame.draw.rect(screen, WHITE, confirm_rect, border_radius=8)
            confirm_txt = font_button.render("CONFIRM", True, BLACK)
        else:
            pygame.draw.rect(screen, GRAY, confirm_rect, border_radius=8)
            confirm_txt = font_button.render("CONFIRM", True, (100, 100, 100))

        screen.blit(confirm_txt, (confirm_rect.x + 20, confirm_rect.y + 10))

        # Fade transition
        if fade_out:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        pygame.display.flip()

    # Main loop
    running = True
    while running:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not fade_out:
                mx, my = pygame.mouse.get_pos()
                for name in characters:
                    x, y = positions[name]
                    icon_rect = pygame.Rect(x, y, 120, 120)
                    if icon_rect.collidepoint(mx, my):
                        handle_click(name)

                if confirm_rect.collidepoint(mx, my) and selected_character:
                    fade_out = True

        if fade_out:
            fade_alpha += 5
            if fade_alpha >= 255:
                print(f"Character selected: {selected_character}")
                running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()