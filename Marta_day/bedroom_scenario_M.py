import pygame
import sys
import os
from Marta_day.car_scenarioM import run_car_scenario_M


def bedroom_scenario_M():
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Marta's Bedroom")
    clock = pygame.time.Clock()

    # Load assets
    background = pygame.image.load(os.path.join('Marta_day', 'images_marta', 'bedroom_M.png')).convert()
    background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

    marta_image = pygame.image.load(os.path.join('Marta_day', 'images_marta', 'character_bedroom_M.png')).convert_alpha()
    marta_image = pygame.transform.smoothscale(marta_image, (400, 600))
    marta_position = (WIDTH // 2 + 30, HEIGHT - 600)

    icon_img = pygame.image.load(os.path.join('images', 'Marta_circle_border.png')).convert_alpha()
    icon_img = pygame.transform.smoothscale(icon_img, (80, 80))
    icon_position = (WIDTH - 100, HEIGHT - 120)

    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 28)

    dialogue_lines = [
        "Ughh,my bed is soo warm. Should I snooze and sleep longer, walk my dog, or have some tea?",
        "Breakfast or no breakfast? Maybe I can grab something while walking the dog. Should I have breakfast at home, grab food on the walk, or skip breakfast?",
        "Alright, now how should I get to uni? Should I drive to university, take the bus, or carpool with colleagues?" 
    ]

    choices_sets = [
        ["Snooze and sleep", "Walk my dog", "Have some tea"],
        ["Breakfast at home", "Grab food outside", "Skip breakfast"],
        ["Drive to Uni", "Take the bus", "carpool with colleagues"] 
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
            (label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
    
    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(marta_image, marta_position)

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
                                    choice_text = "A little more sleep won’t hurt…"
                                elif food_option == 1:
                                    choice_text = "Fresh air will be good for both of us!"
                                elif food_option == 2:
                                    choice_text = "A warm cup of tea sounds perfect to start the day calmly."
                                dialogue_lines.insert(3, choice_text)
                                current_line = 3

                            elif current_choice_set == 1:
                                current_choice_set = 2

                            elif current_choice_set == 2:
                                selected_outfit = idx
                                if selected_outfit == 0:
                                    choice_text = "Eating at home is healthier, let's do that."
                                elif selected_outfit == 1:
                                    choice_text = "I’m in a rush — I’ll just grab something quick on the way."
                                elif selected_outfit == 2:
                                    choice_text = "Not really hungry right now. I’ll skip breakfast and maybe snack later."
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

    # After fade, continue to car scene
    run_car_scenario_M()
