""" Main module contains the Backtracking DFS  """

import json
from copy import deepcopy

# This is a list of artists for testing purposes. Known conflicts are Gwilym Simcock
INCLUDE_ARTISTS = [
    'The Aquaducks',
    # "Hazmat Modine",
    # "Brain Cloud",
    # "Kaisa's Machine",
    # "Artemis",
    # "Bad Sneakers",
    # "Chris Beard Band",
    # "Benny Benack III Quartet",
    # "Connie Han",
    # "Bob Sneider and Paul Hofmann Play the Music of Pat Metheny and Lyle Mays",
    # "Stanley Jordan Plays Jimi Hendrix",
    # "Gwilym Simcock & Tommy Smith",
    # "Groover Quartet",
    # "Brazilian Jazz Quartet Featuring Diego Figueiredo & Ken Peplowski",
    # "Oddgeir Berg Trio",
    # "Bermuda Search Party",
    # "G.E. Smith",
    # "Jorge Luis Pacheco Trio",
    # "Brubeck Brothers",
    # "Eastman School of Music Jazz Honors Unit 3",
    # "Eastman School of Music Jazz Honors  Unit 2",
    # "Eastman School of Music  Jazz Honors Unit 1",
]

def getBlankFestival():
    """ Create a new instance of a festival pseudo-object, which represents a schedule """
    day1 = [None]*44
    day2 = [None]*44
    day3 = [None]*44
    day4 = [None]*44
    day5 = [None]*44
    day6 = [None]*44
    day7 = [None]*44
    day8 = [None]*44
    day9 = [None]*44

    festival = [day1,day2,day3,day4,day5,day6,day7,day8,day9]

    return festival

def attemptToSchedule(st, et, name, schedule, day):
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
    #Attempt to schedule based on start, end, artist name, and day. schedule is an instance of a schedule
    if schedule[day][st:et] == [None]*4:   
        schedule[day][st:et] = [name]*4
        return True
    return False

def backtrack(queue: list, schedule: list):
    """ 
        The main recursive backtracking algorithm.

        -queue: a list of artist pseudo-objects to schedule
        -schedule: an instance of a festival pseudo-object

        Returns:
        True and a festival instance upon success, False and some details about the last failed artist otherwise
    """
    #If all artists are scheduled, return the valid schedule
    if len(queue) == 0:
        return True, schedule
    else:
        for artist in queue:
            for showTime in artist["times"]:
                newSched = deepcopy(schedule)

                # Derive the position in the festival list based on the ISO-formatted Datetime
                data = showTime.split("&")
                festivalday = int(data[0][-2:]) - 21
                timepm = data[1][:-3]

                #Determine time positions
                temp = timepm.split(":")
                st = (int(temp[0])-1)*4 + int(temp[1])//15
                et = st + 4

                #Attempt to schedule
                if attemptToSchedule(st, et, f"{artist["name"]}\n@{data[-1]}", newSched, festivalday):
                    val = backtrack([i for i in queue if i != artist], newSched)
                    if val[0]:
                        return True, val[1]
            return False, artist['name'], artist["times"]

def makeSchedule(arsts: list=INCLUDE_ARTISTS):
    """
        Given a list of artist pseudo-objects, attempt to create a schedule

        -arsts: a list of artist pseudo-objects

        Returns:
        the result of the backtrack() call
    """
    with open("artists.json", "r") as f:
        artists = json.load(f)

    festival = getBlankFestival()
    return backtrack([i for i in artists if i["name"] in arsts], festival)


if __name__ == "__main__":
    print(makeSchedule())
