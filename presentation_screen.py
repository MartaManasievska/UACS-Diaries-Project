import pygame
import os
import sys

def run_presentation_scene():
    pygame.init()

    # Screen setup
    width, height = 1000, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Presentation")
    clock = pygame.time.Clock()

    # Load backgrounds
    background1 = pygame.image.load(os.path.join('images', 'presentation_scenario.png')).convert()
    background1 = pygame.transform.smoothscale(background1, (width, height))

    background2 = pygame.image.load(os.path.join('images', 'presentation_group.png')).convert()
    background2 = pygame.transform.smoothscale(background2, (width, height))

    # Load icons
    profV_icon = pygame.image.load(os.path.join('images', 'profV_circle_border.png')).convert_alpha()
    profV_icon = pygame.transform.smoothscale(profV_icon, (70, 70))

    profG_icon = pygame.image.load(os.path.join('images', 'profG_circle_border.png')).convert_alpha()
    profG_icon = pygame.transform.smoothscale(profG_icon, (70, 70))

    sanja_icon = pygame.image.load(os.path.join('images', 'Sanja_circle_border.png')).convert_alpha()
    sanja_icon = pygame.transform.smoothscale(sanja_icon, (70, 70))

    eva_icon = pygame.image.load(os.path.join('images', 'Eva_circle_border.png')).convert_alpha()
    eva_icon = pygame.transform.smoothscale(eva_icon, (70, 70))

    student_icon = pygame.image.load(os.path.join('images', 'Student.png')).convert_alpha()
    student_icon = pygame.transform.smoothscale(student_icon, (70, 70))

    # Fonts
    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 26)

    # Dialogue content
    professor_lines = [
        ("Prof. V", "left", "Excellent presentation from Group 2!"),
        ("Prof. G", "right", "Yes, they handled the topic really well."),
        ("Prof. V", "left", "Now, let’s invite Group 3 – ‘UACS Diaries’ – to present their project."),
        ("Prof. G", "right", "Looking forward to seeing your work!")
    ]

    girl_lines = [
        ("Sanja", "left", "Hello everyone, we’re Group 3 and our project is a game!"),
        ("Eva", "right", "Yes! We’ve designed an interactive experience that lets you play through student life at UACS."),
        ("Sanja", "left", "To show you how it works, we’d like to invite a volu..."),
        ("Student A", "left", "ME! I want to play!")
    ]

    # State variables
    current_line = 0
    displayed_text = ""
    typing_index = 0
    typing_speed = 2
    frame_count = 0
    text_complete = False
    waiting_for_click = False
    fade_out = False
    fade_alpha = 0
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    transitioned = False
    using_girl_lines = False

    def draw_dialogue_box(speaker, side):
        box_rect = pygame.Rect(50, height - 160, width - 100, 110)
        pygame.draw.rect(screen, (40, 40, 40), box_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2, border_radius=15)

        icons = {
            "Prof. V": profV_icon,
            "Prof. G": profG_icon,
            "Sanja": sanja_icon,
            "Eva": eva_icon,
            "Student A": student_icon
        }
        icon = icons.get(speaker)

        if side == "left":
            if icon:
                screen.blit(icon, (40, box_rect.y - 20))
            text_x = 150
        else:
            if icon:
                screen.blit(icon, (width - 110, box_rect.y - 12))
            text_x = 80

        # Word wrapping
        words = displayed_text.split(' ')
        lines, line = [], ""
        max_width = box_rect.width - 180
        for word in words:
            test_line = line + word + " "
            if font_dialogue.size(test_line)[0] < max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        for i, l in enumerate(lines):
            rendered = font_dialogue.render(l, True, (255, 255, 255))
            screen.blit(rendered, (text_x, box_rect.y + 40 + i * 30))

    # Main loop
    running = True
    while running:
        # Background swap
        screen.blit(background1 if not transitioned else background2, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_complete:
                    if not waiting_for_click:
                        waiting_for_click = True  # Prevent skipping during type
                    else:
                        current_line += 1
                        typing_index = 0
                        frame_count = 0
                        displayed_text = ""
                        text_complete = False
                        waiting_for_click = False

                        # Fade after professors are done
                        if not using_girl_lines and current_line >= len(professor_lines):
                            fade_out = True

                        # End scene after girls' dialogue
                        if using_girl_lines and current_line >= len(girl_lines):
                            running = False

        # Determine which set we're in
        if not transitioned and current_line < len(professor_lines):
            name, side, full_text = professor_lines[current_line]
        elif transitioned:
            if not using_girl_lines:
                using_girl_lines = True
                current_line = 0
                typing_index = 0
                displayed_text = ""
                text_complete = False
                waiting_for_click = False
            if current_line < len(girl_lines):
                name, side, full_text = girl_lines[current_line]
            else:
                full_text = ""
        else:
            full_text = ""

        # Typewriter effect
        if full_text and not text_complete:
            frame_count += 1
            if frame_count % typing_speed == 0 and typing_index < len(full_text):
                displayed_text += full_text[typing_index]
                typing_index += 1
            if typing_index == len(full_text):
                text_complete = True

        if full_text:
            draw_dialogue_box(name, side)

        # Fade to group image
        if fade_out and not transitioned:
            fade_alpha += 5
            if fade_alpha >= 255:
                fade_alpha = 255
                transitioned = True
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        pygame.display.update()
        clock.tick(60)

pygame.quit()
sys.exit()
