""" Webscrape module fetches a list of artists and show times from the RIJF site """

from datetime import datetime
from bs4 import BeautifulSoup as bs
import json

def main():
    ARTISTS = []

    # Not only is this link now deprecated, but the site now uses JavaScript to render the page
    # url = "https://www.rochesterjazz.com/full_schedule?view=artist&printer_friendly="

    with open("./sources/rijf.html", "r", encoding="utf-8") as f:
        url = f.read()

    soup = bs(url, "lxml")
    containers = soup.find_all("div", {"class": "card__text"})

    #Persistent data
    currentArtist = None
    currentData = {}

    #Soupify html
    for c in containers:
        try:
            name = c.find("h1").text.strip()
            time = c.find("h2").text.strip()
            location = c.find("h4").text.strip()
            # replace special characters in location 
            location = location.replace("&", "and").strip()

            if "Central Library of Rochester and Monroe County" in location:
                # Skip artists at the Central Library
                continue

            #Map 'Saturday, June 21 / 6:00pm' to 2025-06-21&6:00 PM
            time = datetime.strptime(time, "%A, %B %d / %I:%M%p").strftime("2025-%m-%d&%I:%M %p")


            print(f"Artist: {name}, Time: {time}, Location: {location}")
            if name != currentArtist:
                if currentData != {}:
                    ARTISTS.append(currentData)
                currentArtist = name
                currentData = {"name": name, "times": []}
            currentData["times"].append(f"{time}&{location}")

        except AttributeError as e:
            # If the artist data is not structured as expected, skip it
            print("Error parsing artist data, skipping...")
            print("\t\t", str(c))
                    
    with open("artists.json", "w") as f:
        json.dump(sorted(ARTISTS, key=lambda x: x["name"].lower().replace("The ", "")), f)

if __name__ == "__main__":
    main()