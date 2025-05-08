import pygame
import sys
import os

def run_walking_scenario():
    # Initialize
    pygame.init()
    width, height = 1000, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tina - Music Walk")
    clock = pygame.time.Clock() 

    # Load background
    background = pygame.image.load(os.path.join('Tina_day', 'images_tina', 'walking_scene.png')).convert()
    background = pygame.transform.smoothscale(background, (width, height))

    # Button setup
    button_font = pygame.font.SysFont('Arial', 28, bold=True)
    button_text = button_font.render("Next Scene", True, (255, 255, 255))
    button_color = (120, 60, 20)  # Dark orange-brown
    button_rect = pygame.Rect(width - 180, height - 70, 160, 50)  # Position + Size



    # # Optional: Load and play background music
    # pygame.mixer.music.load(os.path.join('Tina_day', 'audio', 'lofi_walk.mp3'))
    # pygame.mixer.music.play(-1)  # Loop indefinitely

    # Tina position
    tina_x = -250  # Start off-screen
    tina_y = height - 500
    tina_speed = 2

    # Fade-out setup
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    fade_alpha = 0
    fade_out = False

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Draw button
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_pos)

        hover_color = (51, 24, 0)  
        current_color = hover_color if is_hovered else button_color

        pygame.draw.rect(screen, current_color, button_rect, border_radius=12)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))



        tina_x += tina_speed

        # Once Tina exits the screen, start fade-out
        if tina_x > width:
            fade_out = True

        if fade_out:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha += 3
            if fade_alpha >= 255:
                pygame.time.delay(500)
                running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Next Scene clicked!")  # Or trigger scene transition here
                    running = False

            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(60)


