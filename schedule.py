import random as r
import numpy
import math

class Schedule(object):
    def __init__(self, manager):
        self.manager = manager
        self.schedule = self.generate() # { hourday: location }  e.g.: { "12-4": 8 }

    def generate(self):
        # determine locations
        mid_loc = self.manager.random_mid_location().id
        home_loc = self.manager.random_home_location().id

        # determine work conditions
        work_time_list = [  0,   10,   20,  30,  40,   60]
        work_time_prob = [0.1, 0.04, 0.05, 0.2, 0.6, 0.01]

        work_time = numpy.random.choice(work_time_list, 1, p=work_time_prob)[0]

        work_days = math.ceil(work_time / (8 + r.uniform(-0.2, 1)))

        if work_time == 60:
            work_days = 5

        start_day = 0
        if work_days < 5:
            start_day = r.randint(0, 5 - work_days)

        work_start_time = int(r.gauss(9, 1))
        print (work_start_time)

        sleep_in_time = r.gauss(9, 0.5)

        # generate the schedule
        schedule = {}

        hours_left = work_time

        for day in range(0, 7):
            for hour in range(0, 24):
                key = str(hour) + "-" + str(day)

                # if workday ...
                if day >= start_day and day <= start_day + work_days and work_days > 0:
                    # set sleep rythm
                    if hour < work_start_time - 2:
                        schedule[key] = 0
                    elif hour > 24 + ((work_start_time - 2) - 9):
                        schedule[key] = 0
                    # set work rythm
                    elif hour >= work_start_time and hour <= work_start_time + \
                            work_time / work_days:
                        schedule[key] = mid_loc
                    else:
                        schedule[key] = home_loc
                # if weekend...
                else:
                    if hour <= r.gauss(9, 0.5):
                        schedule[key] = 0
                    else:
                        schedule[key] = home_loc

        # yay side effects and laziness
        self.home_loc = home_loc
        self.mid_loc = mid_loc

        return schedule
