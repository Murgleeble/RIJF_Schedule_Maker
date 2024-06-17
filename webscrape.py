""" Webscrape module fetches a list of artists and show times from the RIJF site """

from bs4 import BeautifulSoup as bs
import requests as re
import json

def main():
    ARTISTS = []

    url = "https://www.rochesterjazz.com/full_schedule?view=artist&printer_friendly="

    soup = bs(re.get(url).text, "lxml")
    containers = soup.find_all("table", {"class": "table table-striped table-hover table-condensed"})

    #Persistent data
    currentArtist = None
    currentData = {}

    #Soupify html
    for c in containers:
        
        for row in c.find_all("tr"):
            data = [i.text for i in row.find_all("td")]
            #Ignore artifacts
            if len(data) > 0:
                #Skip artists playing at 12:00 because I hate time
                if data[1] != "12:00 PM":
                    #Begin creating artist data entry
                    if data[2] != currentArtist:
                        if currentArtist != None:
                            ARTISTS.append(currentData)
                        currentArtist = data[2]
                        currentData = {"name": currentArtist, "times": []}
                    currentData["times"].append(f"{data[0]}&{data[1]}&{data[-1]}")
                    
    with open("artists.json", "w") as f:
        json.dump(ARTISTS, f)

if __name__ == "__main__":
    main()