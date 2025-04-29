import pygame
import sys
import os
from choose_character_screen import run_character_selection  # Make sure this matches the function name!

# Initialize Pygame
pygame.init()

def run_selection_screen():
    # Set up display
    width, height = 1000, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("UACS Diaries - Selection Screen")

    # Load background image
    background = pygame.image.load(os.path.join('images', 'background_loadingScreen.jpg'))
    background = pygame.transform.scale(background, (width, height))

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PASTEL_PINK = (255, 182, 193)
    PASTEL_PINK_HOVER = (255, 200, 210)

    # Fonts
    font_title = pygame.font.Font("Tagesschrift-Regular.ttf", 64)
    font_button = pygame.font.Font("Tagesschrift-Regular.ttf", 40)

    # Button setup
    button_width = 500
    button_height = 70
    start_btn_rect = pygame.Rect(width//2 - button_width//2, 250, button_width, button_height)
    exit_btn_rect = pygame.Rect(width//2 - button_width//2, 350, button_width, button_height)

    def draw_button(rect, text, mouse_pos):
        color = PASTEL_PINK_HOVER if rect.collidepoint(mouse_pos) else PASTEL_PINK
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=15)
        label = font_button.render(text, True, BLACK)
        screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

    # Main loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_rect.collidepoint(event.pos):
                    print("Start New Game clicked")
                    run_character_selection()  # Call the character selection function
                if exit_btn_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(background, (0, 0))

        # Draw title
        title = font_title.render("UACS Diaries", True, PASTEL_PINK)
        screen.blit(title, (width//2 - title.get_width()//2, 100))

        # Draw buttons
        draw_button(start_btn_rect, "Start New Game", mouse_pos)
        draw_button(exit_btn_rect, "Exit", mouse_pos)

        pygame.display.update()

# Only run this screen when executing the script directly
if __name__ == "__main__":
    run_selection_screen()
