import pygame
import sys
import os

def run_srekja_scene():
    pygame.init()

    width, height = 1000, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Srekja caffee")
    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join('images' , 'srekja_scenario.png')).convert()
    background = pygame.transform.smoothscale(background, (width, height))

    sanja_icon = pygame.image.load(os.path.join('images', 'Sanja_circle_border.png')).convert_alpha()
    sanja_icon = pygame.transform.smoothscale(sanja_icon, (70, 70))
    eva_icon = pygame.image.load(os.path.join('images', 'Eva_circle_border.png')).convert_alpha()
    eva_icon = pygame.transform.smoothscale(eva_icon, (70, 70))
    marta_icon = pygame.image.load(os.path.join('images', 'Marta_circle_border.png')).convert_alpha()
    marta_icon = pygame.transform.smoothscale(marta_icon, (70, 70))
    anja_icon = pygame.image.load(os.path.join('images', 'Anja_circle_border.png')).convert_alpha()
    anja_icon = pygame.transform.smoothscale(anja_icon, (70, 70))


    font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
    font_dialogue = pygame.font.Font(font_path, 26)
    font_name = pygame.font.Font(font_path, 26)

    with open(os.path.join('Marta_day','srekja_scenario.json'), 'r', encoding='utf-8') as file:
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

        # Text positioning
        text_x = box_rect.x + 100 if speaker in ["Marta", "Sanja"] else box_rect.x + 20
        for i, l in enumerate(lines):
            rendered = font_dialogue.render(l, True, (255, 255, 255))
            screen.blit(rendered, (text_x, box_rect.y + 40 + i * 30))

        # Icon and Name logic
        if speaker != "narration":
            name_text = font_name.render(speaker, True, (255, 255, 255))

            if speaker == "Sanja":
                screen.blit(sanja_icon, (box_rect.x + 10, icon_y))
                screen.blit(name_text, (box_rect.x + 90, icon_y + 10))
            elif speaker == "Marta":
                screen.blit(marta_icon, (box_rect.x + 10, icon_y))
                screen.blit(name_text, (box_rect.x + 90, icon_y + 10))
            elif speaker == "Eva":
                screen.blit(eva_icon, (box_rect.right - 80, icon_y))
                screen.blit(name_text, (box_rect.right - font_name.size(speaker)[0] - 90, icon_y + 10))
            elif speaker == "Anja":
                screen.blit(anja_icon, (box_rect.right - 80, icon_y))
                screen.blit(name_text, (box_rect.right - font_name.size(speaker)[0] - 90, icon_y + 10))
            elif speaker == "Tina":
                # If you add Tina's icon, handle her too
                tina_icon = pygame.image.load(os.path.join('images', 'Tina_circle_border.png')).convert_alpha()
                tina_icon = pygame.transform.smoothscale(tina_icon, (70, 70))
                screen.blit(tina_icon, (box_rect.right - 80, icon_y))
                screen.blit(name_text, (box_rect.right - font_name.size(speaker)[0] - 90, icon_y + 10))



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

