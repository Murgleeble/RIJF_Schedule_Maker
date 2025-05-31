""" App module contains the backend of the WebApp interface the to creator """

from flask import Flask, render_template, request
import algorithm as dfs
import json
from datetime import datetime
import colorsys
import hashlib

app = Flask(__name__, static_folder="static/")

@app.template_filter("color")
def string_to_color(s, base_hue=0.9, base_saturation=0.5, base_lightness=0.75, delta=0.4):
    """
    Convert a string to a color using HLS (Hue, Lightness, Saturation) color model. Generated using Github CoPilot

    Parameters:
    - s: The input string to be converted to a color.
    - base_hue: The base hue value (0.0 to 1.0).
    - base_saturation: The base saturation value (0.0 to 1.0).
    - base_lightness: The base lightness value (0.0 to 1.0).
    - delta: The variation in hue based on the string.
    Returns:
    - A hex color string representing the color derived from the input string.
    """
    # Hash the string to get a deterministic value
    h = int(hashlib.md5(s.encode()).hexdigest(), 16)
    # Use the hash to slightly vary the hue
    hue = (base_hue + (h % 500) * delta / 100) % 1.0
    # Convert HLS to RGB
    r, g, b = colorsys.hls_to_rgb(hue, base_lightness, base_saturation)
    # Convert to hex
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))


@app.route("/", methods=["GET","POST"])
def base():
    """
    The main route of the web application. It handles both GET and POST requests.
    - GET: Renders the base template with the list of artists.
    - POST: Processes the selected artists and attempts to create a festival schedule.
    If the schedule creation fails, it returns the list of artists with conflicts highlighted.
    """
    #Fetch the result of the webscraper
    with open("./sources/artists.json", "r") as f:
        artists = json.load(f)

    if request.method == "GET":
        return render_template("base.html", festival=False, artists=artists, selected=[], max_overlap=1, shrink=False)
    else:
        #Retrieve the selected artists
        choices = list(request.form.keys())
        choices.remove("last-selected")
        choices.remove("max-overlap")
        choices.remove("shrunk")

        shrink = request.form.get("shrunk") == "True"
        
        max_overlap = int(request.form.get("max-overlap", 1))
        #Retrieve the times that the last artists selected plays
        conflictTimes = []
        for a in artists:
            if a["name"] == request.form.get("last-selected"):
                conflictTimes = a["times"]
                break
        
        #Attempt to create the schedule
        sched = dfs.makeSchedule(max_overlap, choices)

        #If the creation failed
        if not sched:
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
                                    if len(art['name']) > 50:
                                        conflicts.append(art['name'][:50]+'...')
                                    else:
                                        conflicts.append(art['name'])
            return render_template(
                "base.html", 
                festival=None, 
                failed=request.form.get("last-selected"), 
                conflicts=list(set(conflicts)), 
                artists=artists, 
                selected=choices,
                max_overlap=max_overlap,
                shrink=False)
        #Upon success
        return render_template(
            "base.html", 
            festival=sched, 
            artists=artists, 
            selected=choices,
            max_overlap=max_overlap,
            shrink=shrink)
        

if __name__ == "__main__":
    app.run(debug=True)