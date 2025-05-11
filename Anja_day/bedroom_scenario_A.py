import pygame
import sys
import os
from Anja_day.car_scenarioA import run_car_scenario_A  # Make sure this exists

def bedroom_scenario_A():
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Anja's Bedroom")
    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join('Anja_day', 'images_anja', 'bedroom_A.png')).convert()
    background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

    anja_image = pygame.image.load(os.path.join('Anja_day', 'images_anja', 'character_bedroom_A.png')).convert_alpha()
    anja_image = pygame.transform.smoothscale(anja_image, (400, 600))
    anja_position = (WIDTH // 2 + 90, HEIGHT - 600)

    icon_img = pygame.image.load(os.path.join('images', 'Anja_circle_border.png')).convert_alpha()
    icon_img = pygame.transform.smoothscale(icon_img, (80, 80))
    icon_position = (WIDTH - 100, HEIGHT - 120)

    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 28)

    dialogue_lines = [
        "It’s way too early for real decisions. I feel like I barely slept. Should I eatbreakfast now, drink coffee, or snooze for 15 more minutes?",
        "Let me see... my phone’s buzzing already. But maybe I should be productive and start the day positively. Should I check my phone notifications, write in my journal, or listen to music while getting ready?",
        "Traffic is going to be a nightmare, but public transport sucks too. Should I go to university by car, by bus, or carpool with colleagues?",



    ]

    choices_sets = [
        ["Eat Breakfast", "Drink Coffee, "Snooze for 15 minutes"],
        ["Check phone notification", "Write in journal", "Listen to music"],
        ["Go by car", "Go by bus", "Carpool with colleagues"] 
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
        screen.blit(anja_image, anja_position)

        if show_choices:
            draw_choices()
        else:
            draw_dialogue_box()

        if fade_out:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha += 5
            if fade_alpha >= 255:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_choices:
                    for idx, rect in enumerate(choice_rects):
                        if rect.collidepoint(event.pos):
                            show_choices = False
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False

                            if current_choice_set == 0:
                                current_choice_set = 1
                                if idx == 0:
                                    choice_text = "Best breakfast ever!"
                                elif idx == 1:
                                    choice_text = "That will keep me awake for the day."
                                else:
                                    choice_text = "Well, I have more time I should sleep."
                                dialogue_lines.insert(3, choice_text)
                                current_line = 3

                            elif current_choice_set == 1:
                                current_choice_set = 2

                            elif current_choice_set == 2:
                                if idx == 0:
                                    choice_text = "Let's see what is going on."
                                elif idx == 1:
                                    choice_text = "Time to reflect and jot down my thoughts."
                                else:
                                    choice_text = "Music always lifts my mood and helps me focus."
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

    # Call car ride scene
    run_car_scenario_A()
    