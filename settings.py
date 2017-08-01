import pygame

"""
Contains all global variables and settings. Stuff like screen is in here so not
every drawing function needs it as an argument.
"""

pygame.font.init()

size = width, height = 1920, 1080
black = 0, 0, 0
gray = 50, 50, 50
white = 255, 255, 255
red = (255, 0, 0)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", \
        "Friday", "Saturday", "Sunday"]

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Monospace', 12)
fontdims = font.size("M.M.M.M.")
bigfont = pygame.font.SysFont('Monospace', 24)

zoom = 1

hour = 14
day = 0

history = []

def add_hour(manager):
    global hour
    global day

    hour += 1
    if hour > 23:
        hour = 0
        day += 1
        if day > 6:
            day = 0

    manager.spread_all()

    history.append((hour, day, manager.perc_knows()))
