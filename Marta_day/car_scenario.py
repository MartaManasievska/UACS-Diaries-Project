import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Ride - Marta & Anja")
clock = pygame.time.Clock()

# Load background
background = pygame.image.load(os.path.join('Marta_day', 'images_marta', 'car_scenario.png')).convert()
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))

# Load icons
marta_icon = pygame.image.load(os.path.join('images', 'Marta_circle_border.png')).convert_alpha()
marta_icon = pygame.transform.smoothscale(marta_icon, (70, 70))

anja_icon = pygame.image.load(os.path.join('images', 'Anja_circle_border.png')).convert_alpha()
anja_icon = pygame.transform.smoothscale(anja_icon, (70, 70))

# Font
font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
font_dialogue = pygame.font.Font(font_path, 26)
font_name = pygame.font.Font(font_path, 26)

# Dialogue with speaker tuples (Marta, Anja)
dialogue_lines = [
    ("Marta", "I can't believe we're presenting today. My stomach is already doing flips."),
    ("Anja", "You've got this. Besides, we rehearsed like five times."),
    ("Marta", "Yeah, but what if the projector fails? Or I blank out?"),
    ("Anja", "Then I'll jump in and distract them with my charm. Obviously."),
    ("Marta", "Oh my god, Anja."),
    ("Anja", "Relax. Once we get coffee, your whole vibe will reset.")
]

choice_sets = [
    ["Ask Anja what coffee she's getting", "Double check your flash drive", "Say you want to skip and go home"],
    ["Text Tina to stall the start", "Take a deep breath and focus", "Distract yourself with a joke"],
    ["Say you’re feeling confident now", "Ask to rehearse one more time", "Stay silent and just smile"]
]

response_dialogue = [
    ["Marta", "Wait—what are you ordering? I need to copy a good one."],
    ["Anja", "Hold up—let me check if I even brought my USB..."],
    ["Marta", "What if we just didn’t go and drove to the lake instead?"],

    ["Anja", "Tina says she’s stalling with a story about her cat. Classic."],
    ["Marta", "In... two... one... okay. I’m grounded again."],
    ["Anja", "Knock knock."],

    ["Marta", "Okay yeah... I'm actually feeling ready now."],
    ["Anja", "Alright. Let’s do a speed run. No stutters."],
    ["Marta", "Let’s just vibe. I got this."]
]


# State
current_line = 0
displayed_text = ""
typing_index = 0
typing_speed = 2
frame_count = 0
text_complete = False
fade_out = False
fade_alpha = 0
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))
show_choices = False
choice_rects = []
choice_stage = 0

# Draw dialogue box
def draw_dialogue_box(speaker):
    box_rect = pygame.Rect(50, HEIGHT - 160, WIDTH - 100, 110)
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

    text_x = box_rect.x + 90 if speaker == "Marta" else box_rect.x + 20
    for i, l in enumerate(lines):
        rendered = font_dialogue.render(l, True, (255, 255, 255))
        screen.blit(rendered, (text_x, box_rect.y + 40 + i * 30))

    name_text = font_name.render(speaker, True, (255, 255, 255))
    name_xM = box_rect.x + 90
    name_xA = box_rect.right - font_name.size(speaker)[0] - 90
    name_y = box_rect.y - 30

    if speaker == "Marta":
        screen.blit(marta_icon, (box_rect.x + 10, icon_y))
        screen.blit(name_text, (name_xM, name_y))
    else:
        screen.blit(anja_icon, (box_rect.right - 80, icon_y))
        screen.blit(name_text, (name_xA, name_y))

# Draw choices
def draw_choices():
    global choice_rects
    choice_rects = []
    start_y = HEIGHT - 300
    for i, choice in enumerate(choice_sets[choice_stage]):
        rect = pygame.Rect(WIDTH // 2 - 250, start_y + i * 60, 500, 50)
        choice_rects.append(rect)
        pygame.draw.rect(screen, (255, 182, 193), rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)
        label = font_dialogue.render(choice, True, (0, 0, 0))
        screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))

    if current_line < len(dialogue_lines):
        speaker, _ = dialogue_lines[current_line]
        draw_dialogue_box(speaker)
    elif show_choices:
        draw_choices()

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
                        print(f"Player chose: {choice_sets[choice_stage][idx]}")
                        speaker, line = response_dialogue[choice_stage * 3 + idx]
                        dialogue_lines.append((speaker, line))
                        current_line = len(dialogue_lines) - 1
                        typing_index = 0
                        frame_count = 0
                        displayed_text = ""
                        text_complete = False
                        show_choices = False
                        choice_stage += 1

                        if choice_stage >= len(choice_sets):
                            fade_out = True

            elif text_complete:
                current_line += 1
                if current_line < len(dialogue_lines):
                    typing_index = 0
                    frame_count = 0
                    displayed_text = ""
                    text_complete = False
                elif choice_stage < len(choice_sets):
                    show_choices = True
                else:
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
sys.exit()
