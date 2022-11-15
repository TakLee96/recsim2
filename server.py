from database import load_index, KEYS
from flask import Flask, url_for

import numpy as np

index = load_index()
rest_ids = list(index.keys())
app = Flask(__name__)

K = 10

@app.route("/rest/<rid>")
def rest(rid):
    rest = index[rid]
    template = []
    for key in KEYS:
        template.append(f"<div>{key} : {rest[key]}</div>")
    
    photos = []
    for pid in rest["photos"]:
        photo_url = url_for("static", filename=f"{pid}.jpg")
        photos.append(f'<li><img src="{photo_url}"/></li>')
    template.append(f'<ul>{"".join(photos)}</ul>')

    return "\n".join(template)

@app.route("/")
def home():
    selected_rest = np.random.choice(rest_ids, size=K)
    result = []
    for rid in selected_rest:
        rest = index[rid]
        rname = rest["name"]
        stars = rest["stars"]
        if len(rest["photos"]) > 0:
            photo = np.random.choice(rest["photos"])
            photo_url = url_for("static", filename=f"{photo}.jpg")
            img_str = f'<img src="{photo_url}"/>'
        else:
            img_str = ''
        result.append(f'<li><a href="/rest/{rid}">{rname} - {stars} {img_str}</a></li>')

    return f'<ul>{"".join(result)}</ul>'
