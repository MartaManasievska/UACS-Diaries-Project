import pygame
import sys
import os
from Sanja_day.car_scenarioS import run_car_scenario_S

def bedroom_scenario_S():
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sanja's Bedroom")
    clock = pygame.time.Clock()

    # Load assets
    background = pygame.image.load(os.path.join('Sanja_day', 'images_sanja', 'bedroom_S.png')).convert()
    background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

    Sanja_image = pygame.image.load(os.path.join('Sanja_day', 'images_sanja', 'character_bedroom_S.png')).convert_alpha()
    Sanja_image = pygame.transform.smoothscale(Sanja_image, (400, 600))
    Sanja_position = (WIDTH // 2 + 30, HEIGHT - 600)

    icon_img = pygame.image.load(os.path.join('images', 'Sanja_circle_border.png')).convert_alpha()
    icon_img = pygame.transform.smoothscale(icon_img, (80, 80))
    icon_position = (WIDTH - 100, HEIGHT - 120)

    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 28)

    dialogue_lines = [
        "How is it already morning? Ugh, that was definitely not 8 hours.",        
        "Coffee sounds so good right now... but my skincare won't do itself.",
        "I have to hurry Eva is already downstairs!"
    ]

    choices_sets = [
        ["Wake up on time", "Hit snooze", "Accidentally oversleep"],
        ["Start day with skincare", "Drink coffee", "Listen to music"]
    ]

    current_line = 0
    displayed_text = ""
    typing_index = 0
    typing_speed = 2
    frame_count = 0
    text_complete = False
    show_choices = False
    current_choice_set = 0
    choice_rects = []
    fade_out = False
    fade_alpha = 0
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    waiting_for_fade = False
    dialogue_lines.append("scene_end_marker")
    waiting_for_response = False
    next_response_text = ""


    def draw_dialogue_box():
        box_rect = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 100)
        pygame.draw.rect(screen, (0, 0, 0, 180), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3, border_radius=10)
        screen.blit(icon_img, icon_position)

        words = displayed_text.split(' ')
        lines, line = [], ""
        max_width = box_rect.width - 120
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
            screen.blit(rendered, (box_rect.x + 20, box_rect.y + 20 + i * 30))

    def draw_choices():
        nonlocal choice_rects
        choice_rects = []
        start_y = HEIGHT - 300
        mouse_pos = pygame.mouse.get_pos()

        for i, choice in enumerate(choices_sets[current_choice_set]):
            rect = pygame.Rect(WIDTH // 2 - 250, start_y + i * 60, 500, 50)
            choice_rects.append(rect)

            hover = rect.collidepoint(mouse_pos)
            color = (255, 105, 180) if hover else (255, 182, 193)

            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)

            label = font_dialogue.render(choice, True, (0, 0, 0))
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(Sanja_image, Sanja_position)

        if show_choices:
            draw_choices()
        else:
            draw_dialogue_box()

        if fade_out:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha += 5
            if fade_alpha >= 255:
                print("Transition complete. Moving to car scene.")
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if show_choices:
                    for idx, rect in enumerate(choice_rects):
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            show_choices = False
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False
                            current_choice_set += 1
                            break

                elif text_complete:
                    if current_line < len(dialogue_lines) - 1:
                        current_line += 1

                        # Check for scene end marker BEFORE typing anything
                        if dialogue_lines[current_line] == "scene_end_marker":
                            fade_out = True
                        else:
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False

                            # Always show next choice if available
                            if current_choice_set < len(choices_sets):
                                show_choices = True
                    else:
                        fade_out = True



        if not text_complete and current_line < len(dialogue_lines):
            frame_count += 1
            if frame_count % typing_speed == 0:
                typing_index += 1
                displayed_text = dialogue_lines[current_line][:typing_index]
            if typing_index == len(dialogue_lines[current_line]):
                text_complete = True

        pygame.display.update()
        clock.tick(60)


    pygame.quit()
    run_car_scenario_S()
