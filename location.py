import settings as s
import math
import pygame
import random

class Location(object):
    def __init__(self, id):
        self.id = id
        self.presence = []
        for day in range(0, 7):
            self.presence.append([])
            for hour in range(0, 24):
                self.presence[day].append([])

    def fill_presence(self, persons):
        index = 0
        for person in persons:
            schedule = person.schedule.schedule

            home = person.schedule.home_loc

            for hourday in schedule:
                hour = int(hourday.split("-")[0])
                day = int(hourday.split("-")[1])

                personpos = schedule[hourday]
                if personpos == 0:
                    personpos = home

                if personpos == self.id:
                    self.presence[day][hour].append(index)

            index += 1

    def get_num_presence(self, hour, day):
        return len(self.presence[day][hour])

    def spread(self, manager):
        present = self.presence[s.day][s.hour]

        for p_index in present:
            person = manager.persons[p_index]

            if person.knows:
                totalc = 0

                contacts = manager.network[manager.persons[p_index]]

                for contact in contacts:
                    totalc += contacts[contact]

                for p_index_present in present:
                    if p_index_present == p_index:
                        continue # same person, ignore

                    if random.uniform(0, 1) < s.spread_chance:
                        manager.persons[p_index_present].knows = True
                        #print("Spread from " + person.initials + " to " + manager.persons[p_index_present].initials)


    def draw(self, manager, x, y, color):
        RATIO = 0.2

        present = self.presence[s.day][s.hour]

        width = int(len(present) * RATIO)
        if width <= 0:
            width = 1
        height = math.ceil(len(present) / width)

        fontdims = s.font.size("M.M.M.M.")

        locwidth = width * (fontdims[0] + 2)
        locheight = height * (fontdims[1] + 3)

        pygame.draw.rect(s.screen, color, pygame.Rect(\
            (x - fontdims[0] / 2 - 2) * s.zoom, (y - fontdims[1] / 2 - 2) * s.zoom,
            locwidth * s.zoom, locheight * s.zoom), 1)

        for py in range(0, height):
            for px in range(0, width):
                index = py * width + px

                if index > len(present) - 1:
                    continue

                manager.persons[present[index]].draw(s.screen, \
                    x + px * fontdims[0], y + py * (fontdims[1] + 1), \
                    present[index] == manager.highlighted)

        return (locwidth, locheight)
