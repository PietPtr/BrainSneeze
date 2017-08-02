import pygame

"""
Contains all global variables and settings. Stuff like screen is in here so not
every drawing function needs it as an argument.
"""

pygame.font.init()

# size = width, height = 1920, 1080
size = width, height = 1280, 720

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

hour = 0
day = 0
totalday = 0
key = str(hour) + "-" + str(day)

history = []

def add_hour(manager):
    global hour
    global day
    global totalday
    global key

    hour += 1
    if hour > 23:
        hour = 0
        totalday += 1
        day = totalday % 7

    key = str(hour) + "-" + str(day)

    manager.spread_all()

    history.append((hour, day, manager.perc_knows(), manager.perc_sleeps(), \
        manager.perc_working()))


def reset_time():
    global hour
    global day
    global totalday
    global key
    global history

    hour = 0
    day = 0
    totalday = 0
    key = str(hour) + "-" + str(day)

    history = []
