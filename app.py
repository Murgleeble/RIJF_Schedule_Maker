""" App module contains the backend of the WebApp interface the to creator """

from flask import Flask, render_template, request
import main as dfs
import json
from datetime import datetime

app = Flask(__name__, static_folder="static/")

@app.route("/", methods=["GET","POST"])
def base():
    #Fetch the result of the webscraper
    with open("artists.json", "r") as f:
        artists = json.load(f)

    if request.method == "GET":
        return render_template("base.html", festival=False, artists=artists, selected=[])
    else:
        #Retrieve the selected artists
        choices = list(request.form.keys())
        choices.remove("last-selected")

        #Retrieve the times that the last artists selected plays
        conflictTimes = []
        for a in artists:
            if a["name"] == request.form.get("last-selected"):
                conflictTimes = a["times"]
                break
        
        #Attempt to create the schedule
        sched = dfs.makeSchedule(choices)

        #If the creation failed
        if not sched[0]:
            #Normalize the list of times the conflicting artist plays
            conflicts = []
            cs = [i.split('&') for i in conflictTimes]

            #For each selected artist, if the time in which they play overlaps with the 
            #   "conflict" artist's times, add them to the conflicts list
            for art in artists:
                if art['name'] in choices and art['name'] != request.form.get("last-selected"):
                    for time in art['times']:
                        ls = [i[0] for i in cs]
                        if time.split('&')[0] in ls:
                            for c in cs:
                                #Absolute value of the difference in showtimes is less than an hour
                                if abs(
                                    (datetime.strptime(time.split('&')[1], "%I:%M %p") 
                                        - datetime.strptime(c[1], "%I:%M %p")).total_seconds()/60
                                        ) < 60:
                                    if len(art['name']) > 28:
                                        conflicts.append(art['name'][:28]+'...')
                                    else:
                                        conflicts.append(art['name'])
            return render_template(
                "base.html", 
                festival=None, 
                failed=request.form.get("last-selected"), 
                conflicts=list(set(conflicts)), 
                artists=artists, 
                selected=choices)
        
        #Upon success
        return render_template(
            "base.html", 
            festival=sched[1], 
            artists=artists, 
            selected=choices)
        

if __name__ == "__main__":
    app.run(debug=True)