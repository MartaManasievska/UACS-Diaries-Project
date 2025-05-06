import pygame
import sys
import os

pygame.init()

#Screen Setup

width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Ride - Eva & Sanja")
clock = pygame.time.Clock()

background = pygame.image.load(os.path.join('Sanja_day', 'images_sanja', 'car_scenario_S.png')).convert()
background = pygame.transform.smoothscale(background, (width,height))

#Icons
sanja_icon = pygame.image.load(os.path.join('images', 'Sanja_circle_border.png')).convert_alpha()
sanja_icon = pygame.transform.smoothscale(sanja_icon, (70, 70))

eva_icon = pygame.image.load(os.path.join('images', 'Eva_circle_border.png')).convert_alpha()
eva_icon = pygame.transform.smoothscale(eva_icon, (70, 70))


# Font
font_path = os.path.join('NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf')
font_dialogue = pygame.font.Font(font_path, 26)
font_name = pygame.font.Font(font_path, 26)
font_narration = pygame.font.SysFont("arial", 22, bold=False, italic=True)


#Dialogue with the speaker tuples (Sanja, Eva)
dialogue_lines = [
    ("Eva", "There she is. Miss 'I’ll be outside in 2 minutes' — it’s been ten."),
    ("Sanja", "Okay but like, I was being productive. I was panicking and rewriting my intro slide."),
    ("Eva", "Productive panic. My favorite academic genre."),
    ("Eva", "Be real — how much of your part did you actually finish?"),
    ("Sanja", "Uh...."),
    ("narration", "(They turn onto the main road toward campus. Streetlights flicker on. The glow of Srekja is just a few blocks away.)"),
    ("Eva", "Okay, so we’re walking in, pretending we’re calm, and then forcing everyone to stay focused for at least one hour."),
    ("Sanja ", "One whole hour? That’s ambitious."),
    ("Eva", "...Fine. Thirty minutes and one coffee refill. Let’s go."),
    ("Sanja", "You know Tina’s gonna derail the whole thing with some ‘what if we add this last-minute’ idea."),
    ("Eva", "Oh absolutely. And Anja’s gonna be calm about it while silently fixing all our slides."),
    ("Sanja", "Marta’s probably already rewriting the conclusion again..."),    
    ("Eva", "Which I will pretend to love because I am a supportive teammate."),
    ("narration", "What to say next?")

]

choice_sets = [
    ["80%", "Be honest", "admit you don't like what you wrote"],
    ["I love how chaotic we are. It kinda works.","We’re so doomed and it’s beautiful.","Wait… did anyone bring the printed outline for the professor?"]


]

response_dialogue = [
    [("Sanja", "Like... 80%. Just needs a little polishing."),
     ("Eva", "That’s more than I expected. We might actually pull this off."),
     ("Sanja", "Don’t jinx it.")],

     [("Sanja", "Honestly? I’m praying to the Google Slides gods during the ride."),
     ("Eva", "Bold of you to assume Srekja Wi-Fi will let us upload anything."),
     ("Sanja", "Okay now I’m actually scared.")],
     
     [("Sanja", "I finished it but I already hate everything I wrote."),
     ("Eva", "That’s the spirit of academia right there."),
     ("Sanja", "Burnout with a sprinkle of impostor syndrome.")],

     [("Sanja", "I love how chaotic we are. It kinda works."),
      ("Eva", "It's the academic version of jazz — messy but full of feeling."),
      ("Sanja", "Let’s hope the professor agrees.")],

    [("Sanja", "We’re so doomed and it’s beautiful."),
     ("Eva", "Like a tragic group project opera."),
     ("Sanja", "Cue dramatic music as we walk into Srekja.")],

     [("Sanja", "Wait… did anyone bring the printed outline for the professor?"),
      ("Eva", "...Was that not *your* job?"),
      ("Sanja", "OH NO—"),
      ("Eva", "Kidding. Tina printed five. Queen of preparation.")]
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

    text_x = box_rect.x + 20 if speaker == "Eva" else box_rect.x + 90
    for i, l in enumerate(lines):
        font = font_narration if speaker == "narration" else font_dialogue
        color = (200, 200, 200) if speaker == "narration" else (255, 255, 255)
        rendered = font.render(l, True, color)
        screen.blit(rendered, (text_x, box_rect.y + 40 + i * 30))

    if speaker not in ["narration"]:
        name_text = font_name.render(speaker, True, (255, 255, 255))
        name_x = box_rect.x + 20 if speaker == "Eva" else box_rect.right - font_name.size(speaker)[0] - 90
        name_y = box_rect.y - 30
        if speaker == "Eva":
            screen.blit(eva_icon, (box_rect.x + 10, icon_y))
        else:
            screen.blit(sanja_icon, (box_rect.right - 80, icon_y))
        screen.blit(name_text, (name_x, name_y))

# Draw choices
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
            pygame.time.delay(500)
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_choices:
                for idx, rect in enumerate(choice_rects):
                    if rect.collidepoint(event.pos):
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
                            waiting_for_fade = True
            elif text_complete:
                if current_line == 4 and choice_stage == 0:
                    show_choices = True
                    text_complete = False  # prevent advancing
                    typing_index = 0
                    frame_count = 0
                    displayed_text = ""
                else:
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
sys.exit()


