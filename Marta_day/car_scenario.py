import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen setup
width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Ride - Marta & Anja")
clock = pygame.time.Clock()

# Load background
background = pygame.image.load(os.path.join('Marta_day', 'images_marta', 'car_scenario.png')).convert()
background = pygame.transform.smoothscale(background, (width, height))

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
    ("Anja", "I can't believe we're presenting today. My stomach is already doing flips."),
    ("Marta", "You've got this. Besides, we rehearsed like five times."),
    ("Anja", "Yeah, but what if the projector fails? Or I blank out?"),
    ("Marta", "Then I'll jump in and distract them with my charm. Obviously."),
    ("Anja", "Oh my hahah"),
    ("Marta", "Relax. Once we get coffee, your whole vibe will reset.")
]

choice_sets = [
    ["Ask Anja what coffee she's getting", "Double check your flash drive", "Say you can't wait to be done for the day."],
    ["Text Sanja and Eva to save you a seat", "Take a deep breath and focus", "Start a gossip session to distract."],
    ["Say you’re feeling confident now", "Ask to rehearse one more time", "Stay silent and just smile"]
]

response_dialogue = [
    [("Marta", "Wait—what are you ordering? I need to copy a good one."),
     ("Anja", "Caramel macchiato. Don’t copy me, make your own personality.")],

    [("Anja", "Hold up—let me check if I even brought my USB..."),
     ("Marta", "Girl if you forgot it again I swear—")],

    [("Marta", "I can't wait to be done for the day it's exhausting."),
     ("Anja", "No seriously, after this I’m disappearing until Monday.")],

    [("Marta", "Sanja said they will be a little late so Tina will save for all of us haha. Classic"),
     ("Anja", "Tina's the real MVP honestly.")],

    [("Anja", "In... two... one... okay. I’m grounded again."),
     ("Marta", "See? All you needed was a tiny dramatic countdown.")],

    [("Anja", "Oh by the way I heard that you know who started seeing..."),
     ("Marta", "YOU ARE NOT CHANGING THE TOPIC NOW")],

    [("Anja", "Okay yeah... I'm actually feeling ready now."),
     ("Marta", "That's the spirit.")],

    [("Anja", "Alright. Let’s do a speed run. No stutters."),
     ("Marta", "Speed and power. Like Lightning McQueen.")],

    [("Marta", "Let’s just vibe. We got this."),
     ("Anja", "Let’s gooo.")]   
]


# State
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




# Draw dialogue box
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

# Draw choices with hover effect
def draw_choices():
    global choice_rects
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

    
    
# Main loop
running = True
fade_surface = pygame.Surface((width, height))
fade_surface.fill((0, 0, 0))
fade_alpha = 0

while running:
    screen.blit(background, (0, 0))

    # Show dialogue or choices
    if current_line < len(dialogue_lines):
        line_data = dialogue_lines[current_line]
        if isinstance(line_data, tuple) and len(line_data) == 2:
            speaker, _ = line_data
            draw_dialogue_box(speaker)
        else:
            print("⚠️ Invalid dialogue line at index", current_line, ":", line_data)
    elif show_choices:
        draw_choices()

    # Handle fade-out effect
    if fade_out:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        fade_alpha += 5
        if fade_alpha >= 255:
            pygame.time.delay(500)
            running = False

    # Events
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
                            dialogue_lines.append((speaker, line))

                        current_line = start_index
                        typing_index = 0
                        frame_count = 0
                        displayed_text = ""
                        text_complete = False
                        show_choices = False
                        choice_stage += 1

                        if choice_stage >= len(choice_sets):
                        # Let it naturally finish the last line instead of fading now
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

    # Typing effect
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
