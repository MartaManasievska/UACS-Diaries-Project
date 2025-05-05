import pygame
import sys
import os

pygame.init()

#Screen Setup

width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set.caption("Car Ride - Eva & Sanja")
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


#Dialogue with the speaker tuples (Sanja, Eva)
dialogue_lines = [
    ("Eva", "There she is. Miss 'I’ll be outside in 2 minutes' — it’s been ten."),
    ("Sanja", "Okay but like, I was being productive. I was panicking and rewriting my intro slide."),
    ("Eva", "Productive panic. My favorite academic genre."),
    ("Eva", "Be real — how much of your part did you actually finish?")
    ("Sanja", "Uh....")
    ("narration", "(They turn onto the main road toward campus. Streetlights flicker on. The glow of Srekja is just a few blocks away.)")
]

choice_sets = [
    ["80%", "Be honest", "admit you don't like what you wrote"]

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


]



#For Render function
# for speaker, line in dialogue_lines:
#     if speaker == "narration":
#         font = pygame.font.Font("NunitoSans-Italic.ttf", 22)  # or SysFont(..., italic=True)
#         text_color = (180, 180, 180)  # soft gray
#     else:
#         font = pygame.font.Font("NunitoSans-Regular.ttf", 24)
#         text_color = (255, 255, 255)

#     text_surface = font.render(line, True, text_color)
#     screen.blit(text_surface, (x, y))
#     y += 40  # move down for next line
