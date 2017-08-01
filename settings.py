import pygame

"""
Contains all global variables and settings. Stuff like screen is in here so not
every drawing function needs it as an argument.
"""

pygame.font.init()

size = width, height = 1280, 720
black = 0, 0, 0
gray = 50, 50, 50
white = 255, 255, 255

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Monospace', 12)

zoom = 1

hour = 0
day = 0
