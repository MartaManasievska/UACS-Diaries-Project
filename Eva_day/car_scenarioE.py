import pygame
import sys
import os
import json
from srekja_scene import run_srekja_scene

def run_car_scenario_E():
    pygame.init()

    width, height = 1000, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Car Ride - Eva & Sanja")
    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join('Sanja_day', 'images_sanja', 'car_scenario_S.png')).convert()
    background = pygame.transform.smoothscale(background, (width, height))

    sanja_icon = pygame.image.load(os.path.join('images', 'Sanja_circle_border.png')).convert_alpha()
    sanja_icon = pygame.transform.smoothscale(sanja_icon, (70, 70))
    eva_icon = pygame.image.load(os.path.join('images', 'Eva_circle_border.png')).convert_alpha()
    eva_icon = pygame.transform.smoothscale(eva_icon, (70, 70))

    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 26)
    font_name = pygame.font.Font(font_path, 26)
    font_narration = pygame.font.SysFont("arial", 22, bold=False, italic=True)

    with open(os.path.join('Sanja_day', 'dialog_S&E.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)

    dialogue_lines = data["dialogue_lines"]
    choice_sets = data["choice_sets"]
    response_dialogue = data["response_dialogue"]

    current_line = 0
    displayed_text = ""
    typing_index = 0
    typing_speed = 2
    frame_count = 0
    text_complete = False
    show_choices = False
    choice_rects = []
    choice_stage = 0
    fade_out = False
    waiting_for_fade = False

    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    fade_alpha = 0

    def draw_dialogue_box(speaker):
        box_rect = pygame.Rect(50, height - 160, width - 100, 110)
        pygame.draw.rect(screen, (40, 40, 40), box_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2, border_radius=15)

        icon_y = box_rect.y - 40
        words = displayed_text.split(' ')
        lines, line = [], ""
        max_width = box_rect.width - 140
        for word in words:
            test_line = line + word + " "
            if font_dialogue.size(test_line)[0] < max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        text_x = box_rect.x + 20 if speaker == "Eva" else box_rect.x + 10
        for i, l in enumerate(lines):
            font = font_narration if speaker == "narration" else font_dialogue
            color = (200, 200, 200) if speaker == "narration" else (255, 255, 255)
            rendered = font.render(l, True, color)
            screen.blit(rendered, (text_x, box_rect.y + 40 + i * 30))

        if speaker not in ["narration"]:
            name_text = font_name.render(speaker, True, (255, 255, 255))
            name_x = box_rect.x + 90 if speaker == "Eva" else box_rect.right - font_name.size(speaker)[0] - 90
            name_y = box_rect.y - 30
            if speaker == "Eva":
                screen.blit(eva_icon, (box_rect.x + 10, icon_y))
            else:
                screen.blit(sanja_icon, (box_rect.right - 80, icon_y))
            screen.blit(name_text, (name_x, name_y))

    def draw_choices():
        nonlocal choice_rects
        choice_rects = []
        start_y = height - 300
        mouse_pos = pygame.mouse.get_pos()

        for i, choice in enumerate(choice_sets[choice_stage]):
            rect = pygame.Rect(width // 2 - 250, start_y + i * 60, 500, 50)
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

        if current_line < len(dialogue_lines):
            line_data = dialogue_lines[current_line]
            if isinstance(line_data, list) and len(line_data) == 2:
                speaker, _ = line_data
                draw_dialogue_box(speaker)
            else:
                print("⚠️ Invalid dialogue line at index", current_line, ":", line_data)
        elif show_choices:
            draw_choices()

        if fade_out:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha += 5
            if fade_alpha >= 255:
                pygame.time.delay(500)
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_choices:
                    for idx, rect in enumerate(choice_rects):
                        if rect.collidepoint(event.pos):
                            print(f"Player chose: {choice_sets[choice_stage][idx]}")
                            response_lines = response_dialogue[choice_stage * 3 + idx]
                            start_index = len(dialogue_lines)

                            for speaker, line in response_lines:
                                dialogue_lines.append([speaker, line])
                            current_line = start_index
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False
                            show_choices = False
                            choice_stage += 1
                            if choice_stage >= len(choice_sets):
                                waiting_for_fade = True
                elif text_complete:
                    current_line += 1
                    if current_line < len(dialogue_lines):
                        typing_index = 0
                        frame_count = 0
                        displayed_text = ""
                        text_complete = False
                    elif choice_stage < len(choice_sets):
                        show_choices = True
                    elif waiting_for_fade:
                        fade_out = True

        if not text_complete and current_line < len(dialogue_lines):
            frame_count += 1
            if frame_count % typing_speed == 0:
                typing_index += 1
                displayed_text = dialogue_lines[current_line][1][:typing_index]
            if typing_index == len(dialogue_lines[current_line][1]):
                text_complete = True

        pygame.display.update()
        clock.tick(60)

pygame.quit()
run_srekja_scene()