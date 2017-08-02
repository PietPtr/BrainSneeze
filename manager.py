import random as r
import math
import pygame
from person import Person
from location import Location
#from settings import screen, black, white, gray, size, font, zoom
import settings

MID_LOCATIONS = 1/20
EVE_LOCATIONS = 1/4
HOME_LOCATIONS = 1 - MID_LOCATIONS - EVE_LOCATIONS

class Manager(object):
    def __init__(self, n_persons):
        print("Generating persons & locations.")
        self.mid_locs = self.gen_locations(n_persons * MID_LOCATIONS, 0)
        self.eve_locs = self.gen_locations(n_persons * EVE_LOCATIONS,\
            int(n_persons * MID_LOCATIONS) + 1)
        self.home_locs = self.gen_locations(n_persons * HOME_LOCATIONS,  \
            int(n_persons * (MID_LOCATIONS + EVE_LOCATIONS)) + 1)

        self.locations = [self.mid_locs, self.eve_locs, self.home_locs]

        self.persons = self.gen_persons(n_persons)

        self.persons[0].knows = True

        print("Generating location presence lists.")
        totallen = len(self.mid_locs) + len(self.eve_locs) + len(self.home_locs)
        count = 0
        for locs in self.locations:
            for loc in locs:
                if count % 10 == 0:
                    print("  -> " + str(round(count / totallen * 100)) + "%")
                loc.fill_presence(self.persons)
                count += 1

        self.highlighted = 0

        print("Generating network.")
        self.network = self.gen_network()


    """
    Generates the sets of people and locations
    """
    def gen_persons(self, n):
        persons = []
        for i in range(0, n):
            persons.append(Person(self))

        return persons

    def gen_locations(self, n, startid):
        locations = []
        print(startid, int(startid + n))
        for i in range(startid, int(startid + n)):
            # print (i)
            locations.append(Location(i))

        return locations

    """
    Determines the network of people.
    """
    def gen_network(self):
        network = {} # {pid: {pid: closeness, ...}, ...}

        count = 0
        for person in self.persons:
            if count % 10 == 0:
                print("  -> " + str(int(count / len(self.persons) * 100)) + "%")

            contacts = {} # {pid: closeness}

            schedule = person.schedule.schedule
            for hour in schedule:
                location = schedule[hour]

                close_mod = 1

                if location is not 0:
                    for pid in self.get_persons_for_location_and_time(hour, location):
                        if pid in contacts and pid is not count:
                            contacts[pid] += close_mod
                        elif pid is not count:
                            contacts[pid] = close_mod

            network[person] = contacts
            count += 1

        print("  -> 100%")

        return network

        #print(network)


    def get_persons_for_location_and_time(self, time, location):
        pids = [] # indices of persons in that location at that time

        i = 0
        for person in self.persons:
            if person.schedule.schedule[time] == location:
                pids.append(i)

            i += 1

        return pids

    """
    The following functions fetch a random specified location. The 'mid' location
    can be interpreted as work/school. The location 0 is reserved for sleep,
    so there are no interactions there.

    The 'eve' location is for hobby locations, the person usually there during
    the evening or weekend.

    The fraction of the locations designated as mid and eve are defined at the
    top of this file.
    """
    def random_mid_location(self):
        return self.mid_locs[r.randint(1, len(self.mid_locs) - 1)]

    def random_eve_location(self):
        return self.eve_locs[r.randint(1, len(self.eve_locs) - 1)]

    def random_home_location(self):
        return self.home_locs[r.randint(1, len(self.home_locs) - 1)]

    """
    Brain sneeze functions
    """
    def spread_all(self):
        for locs in self.locations:
            for loc in locs:
                loc.spread(self)

    def reset(self):
        for person in self.persons:
            person.knows = False

        self.persons[r.randint(0, len(self.persons) - 1)].knows = True

        settings.reset_time()

    def perc_knows(self):
        knows = 0
        for person in self.persons:
            if person.knows:
                knows += 1
        return knows / len(self.persons) * 100

    """
    Draws everyone in large square with lines between them
    """
    def draw_all_persons(self, x, y):
        side_len = int(math.sqrt(len(self.persons))) + 1

        if self.highlighted >= len(self.persons):
            self.highlighted = len(self.persons) - 1
        elif self.highlighted < 0:
            self.highlighted = 0

        person_surface = pygame.Surface(settings.size, pygame.SRCALPHA, 32)
        person_surface = person_surface.convert_alpha()

        highline_surf = pygame.Surface(settings.size, pygame.SRCALPHA, 32)
        highline_surf = highline_surf.convert_alpha()

        for ix in range(0, side_len):
            for iy in range(0, side_len):
                index = iy * side_len + ix
                if index >= len(self.persons):
                    continue

                x_pad = 120
                y_pad = 80

                px = x + ix * x_pad
                py = y + iy * y_pad

                contacts = self.network[self.persons[index]]

                for contact in contacts:
                    cx = x + contact % side_len * x_pad
                    cy = y + int(contact / side_len) * y_pad

                    line_surface = settings.screen
                    line_color = settings.gray
                    if self.highlighted == index:
                        line_color = settings.white
                        line_surface = highline_surf

                    pygame.draw.line(line_surface, line_color, \
                                    (px * settings.zoom, py * settings.zoom), \
                                    (cx * settings.zoom, cy * settings.zoom))

                draw_high = index in self.network[self.persons[self.highlighted]]\
                    or self.highlighted is index

                self.persons[index].draw(person_surface, px, py, draw_high)

        settings.screen.blit(highline_surf, (0, 0))
        settings.screen.blit(person_surface, (0, 0))

    """
    Draws everyone in their location at a given time
    """
    def draw_locations(self, x, y):
        prevpos = [x, y]

        highestydiff = 0

        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]

        count = 0
        for locs in self.locations:
            color = colors[count]
            for loc in locs:
                if loc.get_num_presence(settings.hour, settings.day) > 0:
                    diff = loc.draw(self, prevpos[0] + x, prevpos[1] + y, color)
                    prevpos[0] += diff[0] + 2
                    highestydiff = max(diff[1], highestydiff)
                    if prevpos[0] > (settings.width * 0.9) + x:
                        prevpos[1] += highestydiff + 4
                        prevpos[0] = x
                        highestydiff = 0
            count += 1
    """
    Draws all persons and the the network at (x, y)

    This function is kind of a failure, but I'm keeping it anyway.
    """
    def draw_network(self, x, y):
        drawn_persons = [None] * (len(self.persons) - 1)

    # draws one person and associated contacts
    def draw_person(self, index, x, y, dist_mult):
        #from main import screen, size, zoom, white
        contacts = self.network[self.persons[index]]

        person_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        person_surface = person_surface.convert_alpha()

        count = 0
        for contact in contacts:
            # if drawn_persons[contact] != None:
            #     continue

            angle = 2 * math.pi * (count / len(contacts))
            contactx = x + math.cos(angle) * zoom * contacts[contact] * dist_mult
            contacty = y + math.sin(angle) * zoom * contacts[contact] * dist_mult

            pygame.draw.line(screen, white, (x * zoom, y * zoom), \
                (contactx * zoom, contacty * zoom))

            self.persons[contact].draw(person_surface, contactx, contacty)

            # drawn_persons[contact] = (contactx, contacty)

            screen.blit(person_surface, (0, 0))

            count += 1

        self.persons[index].draw(screen, x, y)
