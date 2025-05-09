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

    for i, name in enumerate(characters):
        img = pygame.image.load(f"images/{name}_circle_border.png").convert_alpha()
        img = pygame.transform.smoothscale(img, (120, 120))
        icons[name] = img
        positions[name] = (100 + i * 170, 250)

    # Background
    background = pygame.image.load(os.path.join('images', 'cloud.png')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Confirm button
    confirm_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 180, 200, 55)

    # State
    selected_character = None
    fade_out = False
    fade_alpha = 0
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))

    def handle_click(name):
        nonlocal selected_character
        selected_character = name

    def draw():
        screen.blit(background, (0, 0))

        # Title
        title_surf = font_title.render("CHOOSE YOUR CHARACTER", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))

        # Draw icons and names
        for name in characters:
            x, y = positions[name]
            icon = icons[name].copy()
            icon.set_alpha(180 if selected_character and name != selected_character else 255)
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

        # Confirm button
        if selected_character:
            pygame.draw.rect(screen, WHITE, confirm_rect, border_radius=8)
            confirm_txt = font_button.render("CONFIRM", True, BLACK)
            
        else:
            pygame.draw.rect(screen, GRAY, confirm_rect, border_radius=8)
            confirm_txt = font_button.render("CONFIRM", True, (100, 100, 100))

        screen.blit(confirm_txt, (confirm_rect.x + 20, confirm_rect.y + 10))

        # Fade effect
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
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not fade_out:
                mx, my = pygame.mouse.get_pos()
                for name in characters:
                    x, y = positions[name]
                    if pygame.Rect(x, y, 120, 120).collidepoint(mx, my):
                        handle_click(name)

                if confirm_rect.collidepoint(mx, my) and selected_character:
                    # Save selected character
                    with open("player_character.json", "w") as f:
                        json.dump({"player": selected_character}, f)
                    fade_out = True


        if fade_out:
            fade_alpha += 5
            if fade_alpha >= 255:
                running = False

        clock.tick(60)

    pygame.quit()
   
    # Trigger the bedroom scene directly
    if selected_character == "Tina":
        from Tina_day.bedroom_scenario_TS import bedroom_scenario_TS
        bedroom_scenario_TS()
    elif selected_character == "Anja":
        from Anja_day.bedroom_scenario_A import bedroom_scenario_A
        bedroom_scenario_A()
    elif selected_character == "Sanja":
        from Sanja_day.bedroom_scenario_S import bedroom_scenario_S
        bedroom_scenario_S()
    elif selected_character == "Marta":
        from Marta_day.bedroom_scenario_M import bedroom_scenario_M
        bedroom_scenario_M()
    elif selected_character == "Eva":
        from Eva_day.bedroom_scenario_E import bedroom_scenario_E
    bedroom_scenario_E()
