from person import Person
from manager import Manager
import math
#from settings import screen, black, white, gray, size, font
import settings as s

print("Initializing model info.")
NUMP = 132
manager = Manager(NUMP)

import pygame
import sys

pygame.init()

draw = [220, 60]

frame = 0

zoom = 1

draw_mode = "location"

NXTHR = 10
nexthour = NXTHR

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                s.zoom *= 1.1
            if event.button == 5:
                s.zoom /= 1.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                manager.highlighted -= 1
            if event.key == pygame.K_RIGHT:
                manager.highlighted += 1
            if event.key == pygame.K_DOWN:
                manager.highlighted += int(math.sqrt(NUMP) + 1)
            if event.key == pygame.K_UP:
                manager.highlighted -= int(math.sqrt(NUMP) + 1)
            if event.key == pygame.K_s:
                draw_mode = "square"
            if event.key == pygame.K_l:
                draw_mode = "location"
            if event.key == pygame.K_n:
                s.add_hour(manager)
            if event.key == pygame.K_r:
                manager.reset()
            if event.key == pygame.K_h:
                for h in (s.history):
                    print(h)


    """
    Updates & Logic
    """
    #zoom += 0.0001
    mov = pygame.mouse.get_rel()
    if (pygame.mouse.get_pressed()[0]):
        draw[0] += mov[0] * 1 / s.zoom
        draw[1] += mov[1] * 1 / s.zoom

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        nexthour -= 1

    if nexthour <= 0:
        nexthour = NXTHR
        s.add_hour(manager)

    """
    Drawing
    """
    s.screen.fill(s.black)

    if draw_mode == "square":
        manager.draw_all_persons(draw[0], draw[1])
    elif draw_mode == "location":
        manager.draw_locations(draw[0], draw[1])

    timetext = s.bigfont.render(s.days[s.day] + " " + str(s.hour) + ":00 | " + str(round(manager.perc_knows(), 1)) + "% knows", False, s.white)
    s.screen.blit(timetext, (0, 8))

    pygame.display.flip()

    frame += 1
