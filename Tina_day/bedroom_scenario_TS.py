import pygame
import sys
import os

def bedroom_scenario_TS():
    print("✅ Entered Tina's bedroom")
    from Tina_day.walking_scenario import run_walking_scenario

    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tina's Bedroom")
    clock = pygame.time.Clock()

    # Load assets
    background = pygame.image.load(os.path.join('Tina_day', 'images_tina', 'bedroom_TS.png')).convert()
    background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

    tina_image = pygame.image.load(os.path.join('Tina_day', 'images_tina', 'character_bedroom_TS.png')).convert_alpha()
    tina_image = pygame.transform.smoothscale(tina_image, (400, 600))
    tina_position = (WIDTH // 2 - 150, HEIGHT - 600)

    icon_img = pygame.image.load(os.path.join('images', 'Tina_circle_border.png')).convert_alpha()
    icon_img = pygame.transform.smoothscale(icon_img, (80, 80))
    icon_position = (WIDTH - 100, HEIGHT - 120)

    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 28)

    dialogue_lines = [
        "Ugh... another Monday morning. Do I really have to get up?",
        "I could have some pancakes to make this day more durable, but gaming sounds way more fun.",
        "What should I do for breakfast?",
        "Now what should I do next?",
        "Should I plan my outfit ahead of time, choose last minute, or just grab the comfiest thing I see?"
    ]

    choices_sets = [
        ["Eat pancakes", "Go on a morning walk", "Skip breakfast and play games"],
        ["Text my boyfriend", "Do some chores", "Go out with friends"],
        ["Plan ahead", "Choose last minute", "Grab comfiest thing"]
    ]

    responses = [
        ["That hit the spot!", "Feeling refreshed!", "Game time it is!"],
        ["Sent! Hope he replies soon.", "Clean house, clean mind.", "Time to catch up with everyone!"],
        ["This will save me so much time.", "I'm going to wing it.", "Nothing beats cozy."]
    ]

    current_line = 0
    displayed_text = ""
    typing_index = 0
    typing_speed = 2
    frame_count = 0
    text_complete = False
    choice_rects = []
    fade_out = False
    fade_alpha = 0
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))

    current_phase = 0  # 0 = intro, 1 = choice+response 1, 2 = dialogue 2, 3 = choice+response 2, 4 = dialogue 3, 5 = choice+response 3
    choice_index = 0
    waiting_for_choice = False
    response_to_display = ""
    response_displaying = False

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

        for i, choice in enumerate(choices_sets[choice_index]):
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
        screen.blit(tina_image, tina_position)

        if waiting_for_choice:
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
            elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if waiting_for_choice:
                    for idx, rect in enumerate(choice_rects):
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            response_to_display = responses[choice_index][idx]
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False
                            waiting_for_choice = False
                            response_displaying = True
                elif text_complete:
                    if response_displaying:
                        response_displaying = False
                        current_phase += 1
                    else:
                        if current_phase == 0:
                            if current_line < 2:
                                current_line += 1
                                typing_index = 0
                                frame_count = 0
                                displayed_text = ""
                                text_complete = False
                            else:
                                current_phase = 1
                                waiting_for_choice = True
                                choice_index = 0
                        elif current_phase == 2:
                            current_line = 3
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False
                            current_phase = 3
                            waiting_for_choice = True
                            choice_index = 1
                        elif current_phase == 4:
                            current_line = 4
                            typing_index = 0
                            frame_count = 0
                            displayed_text = ""
                            text_complete = False
                            current_phase = 5
                            waiting_for_choice = True
                            choice_index = 2
                        elif current_phase == 6:
                            fade_out = True

        if not text_complete:
            frame_count += 1
            if frame_count % typing_speed == 0:
                if response_displaying:
                    text = response_to_display
                else:
                    text = dialogue_lines[current_line] if current_line < len(dialogue_lines) else ""
                typing_index += 1
                displayed_text = text[:typing_index]
                if typing_index == len(text):
                    text_complete = True
                    if response_displaying:
                        pass
                    elif current_phase == 5:
                        current_phase = 6

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    run_walking_scenario()