from schedule import Schedule
import random as r
import pygame
import settings

class Person(object):
    def __init__(self, manager):
        self.manager = manager
        self.schedule = Schedule(manager) # assign random schedule to person
        self.initials = self.random_initials()
        self.color = (r.randint(64, 255), r.randint(64, 255), \
            r.randint(64, 255))

    def random_initials(self):
        num = int(r.gauss(3, 0.5))
        if num < 2:
            num = 2
        if num > 4:
            num = 4

        initials = ""

        for i in range(0, num):
            initials += chr(r.randint(65, 87)) + "."

        return initials

    def draw(self, surface, x, y, highlighted):
        text = settings.font.render(self.initials, False, self.color)

        width = text.get_width()
        height = text.get_height()


        pygame.draw.rect(surface, settings.white if highlighted else settings.black, pygame.Rect(\
            x * settings.zoom - width / 2, y * settings.zoom - height / 2, \
            width, height))

        pygame.draw.rect(surface, self.color, pygame.Rect(\
            x * settings.zoom - width / 2, y * settings.zoom - height / 2, \
            width, height), 2 if highlighted else 1)


        draw_text = pygame.transform.scale(text, (int(text.get_width()), \
            int(text.get_height())))

        surface.blit(draw_text, (x * settings.zoom + 1 - width / 2, \
            y * settings.zoom + 1 - height / 2))

        return surface
