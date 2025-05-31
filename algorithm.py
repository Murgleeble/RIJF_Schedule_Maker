""" Main module contains the Backtracking DFS  """

import json
from copy import deepcopy

INCLUDE_ARTISTS = [
    'Ricky Lee Jones',
    'Jesus Molina',
    'Bad Sneakers',
]

class FailedSchedulingError(Exception):
    """ Custom exception for failed scheduling attempts """
    def __init__(self, artist_name=None, show_time=None, day=None, start_time=None, end_time=None, msg=None):
        if msg is not None:
            super().__init__(msg)
            self.artist_name = None
            self.show_time = None
            self.day = None
            self.start_time = None
            self.end_time = None
        else:
            super().__init__(f"Failed to schedule {artist_name} at {show_time} on day {day} at {start_time}-{end_time}")
            self.artist_name = artist_name
            self.show_time = show_time
            self.day = day
            self.start_time = start_time
            self.end_time = end_time


def getBlankFestival():
    """ Create a new instance of a festival pseudo-object, which represents a schedule """
    day1 = [[] for _ in range(44)]
    day2 = [[] for _ in range(44)]
    day3 = [[] for _ in range(44)]
    day4 = [[] for _ in range(44)]
    day5 = [[] for _ in range(44)]
    day6 = [[] for _ in range(44)]
    day7 = [[] for _ in range(44)]
    day8 = [[] for _ in range(44)]
    day9 = [[] for _ in range(44)]

    festival = [day1,day2,day3,day4,day5,day6,day7,day8,day9]

    return festival

def attemptToSchedule(st, et, name, schedule, day, max_overlap):
    """ 
        Attempt to fit a given performance into a given schedule
        -st: the start time of the performance
        -et: the end time of the performance
        -name: the performance name
        -schedule: an instance of a festival pseudo-object
        -day: what day of the festival the performance falls on

        Returns:
        True if the performance was successfully added, False otherwise
    """

    for i in range(st, et):
        if not isinstance(schedule[day], list):
            raise TypeError(f"Expected a list at schedule[{day}][{i}], got {schedule[day]}")
        if len(schedule[day][i]) >= max_overlap:
            return False
        schedule[day][i].append(name)
        
        
    return True


def backtrack(queue: list, schedule: list, max_overlap):
    """ 
        The main recursive backtracking algorithm.

        -queue: a list of artist pseudo-objects to schedule
        -schedule: an instance of a festival pseudo-object

        Returns:
            A Festival instance upon success

        If the scheduling fails, raises a ValueError with details about the last failed artist
    """
    #If all artists are scheduled, return the valid schedule
    if len(queue) == 0:
        return schedule
    else:
        for artist in queue:
            for showTime in artist["times"]:
                newSched = deepcopy(schedule)

                # Derive the position in the festival list based on the ISO-formatted Datetime
                data = showTime.split("&")
                festivalday = int(data[0][-2:]) - 20
                timepm = data[1][:-3]

                #Determine time positions
                temp = timepm.split(":")
                st = (int(temp[0])-1)*4 + int(temp[1])//15
                et = st + 4

                #Attempt to schedule
                # print(f"Attempting to schedule {artist['name']} from {data[-1]} on day {festivalday+1} at {st}-{et}")
                if attemptToSchedule(st, et, f"<strong>{artist["name"]}</strong><br>@<em>{data[-1]}</em>", newSched, festivalday, max_overlap):
                    schedule = backtrack([i for i in queue if i != artist], newSched, max_overlap) # type: ignore
                    if schedule:
                        return schedule
            raise FailedSchedulingError(
                artist_name=artist["name"],
                show_time=showTime,
                day=festivalday,
                start_time=st,
                end_time=et
            )
        raise ValueError("No valid schedule could be created with the provided artists.")

def makeSchedule(max_overlap, arsts):
    """
        Given a list of artist pseudo-objects, attempt to create a schedule

        -arsts: a list of artist pseudo-objects

        Returns:
        the result of the backtrack() call
    """
    with open("./sources/artists.json", "r") as f:
        artists = json.load(f)

    festival = getBlankFestival()
    try:
        return backtrack([i for i in artists if i["name"] in arsts], festival, max_overlap=max_overlap)
    except FailedSchedulingError:
        return False
