import pygame
import sys
import os
from Eva_day.car_scenarioE import run_car_scenarioE
 

def bedroom_scenario_E():
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Eva's Bedroom")
    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join('Eva_day', 'images_eva', 'bedroom_E.png')).convert()
    background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

    eva_image = pygame.image.load(os.path.join('Eva_day', 'images_eva', 'character_bedroom_E.png')).convert_alpha()
    eva_image = pygame.transform.smoothscale(eva_image, (400, 600))
    eva_position = (WIDTH // 2 - 20, HEIGHT - 600)

    icon_img = pygame.image.load(os.path.join('images', 'Eva_circle_border.png')).convert_alpha()
    icon_img = pygame.transform.smoothscale(icon_img, (80, 80))
    icon_position = (WIDTH - 100, HEIGHT - 120)

    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 28)

    dialogue_lines = [
        "Ugh... another Monday morning. Do I really have to get up?",
        "Maybe today's the day I'll actually be productive...",
        "Should I eat pancakes, make a healthy smoothie, or skip breakfast and play games instead?",
        "Now what should I do next?",
        "Should I text my boyfriend, do some chores, or go out with friends?",
        "Should I plan my outfit ahead of time, choose last minute, or just grab the comfiest thing I see?" 
    ]

    choices_sets = [
        ["Eat pancakes", "Make a healthy smoothie", "Skip breakfast and play games"],
        ["Text my boyfriend", "Do some chores", "Go out with friends"],
        ["Plan ahead", "Choose last minute", "Grab comfiest thing"] 
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
        choices = choices_sets[current_choice_set]
        start_y = HEIGHT - 250
        for i, choice in enumerate(choices):
            rect = pygame.Rect(WIDTH // 2 - 250, start_y + i * 70, 500, 50)
            choice_rects.append(rect)
            pygame.draw.rect(screen, (255, 182, 193), rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)
            label = font_dialogue.render(choice, True, (0, 0, 0))
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(eva_image, eva_position)

        if show_choices:
            draw_choices()
        else:
            draw_dialogue_box()

        if fade_out:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha += 5
            if fade_alpha >= 255:
                print("Transition complete. Moving to next scene.")
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_choices:
                    for idx, rect in enumerate(choice_rects):
                        if rect.collidepoint(event.pos):
                            print(f"Player picked: {choices_sets[current_choice_set][idx]}")
                            show_choices = False
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False

                            if current_choice_set == 0:
                                current_choice_set = 1
                                food_option = idx
                                if food_option == 0:
                                    choice_text = "Now that was a great breakfast!"
                                elif food_option == 1:
                                    choice_text = "That made me feel very refreshed."
                                elif food_option == 2:
                                    choice_text = "Well, that takes care of breakfast... or lack of it, haha."

                                dialogue_lines.insert(3, choice_text)
                                current_line = 3
                            elif current_choice_set == 1:
                                current_choice_set = 2
                            elif current_choice_set == 2:
                                selected_outfit = idx
                                if selected_outfit == 0:
                                    choice_text = "Eva carefully picks out a confident look and gets going."
                                elif selected_outfit == 1:
                                    choice_text = "Eva shrugs and chooses something quickly."
                                elif selected_outfit == 2:
                                    choice_text = "Eva pulls on her comfiest clothes with a smirk."
                                dialogue_lines.insert(current_line, choice_text)
                                current_line = len(dialogue_lines) - 1
                                waiting_for_fade = True

                elif text_complete:
                    if waiting_for_fade:
                        fade_out = True
                    else:
                        current_line += 1
                        if current_line < len(dialogue_lines):
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False
                            if current_line == 3 and current_choice_set == 0:
                                show_choices = True
                            if current_line == 6 and current_choice_set == 1:
                                show_choices = True
                        else:
                            show_choices = True

        if not text_complete and current_line < len(dialogue_lines):
            frame_count += 1
            if frame_count % typing_speed == 0:
                typing_index += 1
                displayed_text = dialogue_lines[current_line][:typing_index]
            if typing_index == len(dialogue_lines[current_line]):
                text_complete = True

        pygame.display.update()
        clock.tick(60)

    run_car_scenario_E()
