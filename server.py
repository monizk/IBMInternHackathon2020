import os
from dotenv import load_dotenv
import requests
import json
import sqlite3

import irrigation
import weather

from flask import Flask, flash, request, redirect, url_for, escape, render_template, session

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_key"

def in_session():
    if session.get('username', None) is not None and session.get("latitude", None) is not None:
        return True
    session.clear()
    return False

# How to access weather api key
# os.environ.get("WEATHER_API_KEY")

@app.route('/', methods=['GET'])
def index():
    if not in_session():
        return redirect(url_for("login"))
    if not request.script_root:
        request.script_root = url_for('index', _external=True)
    print(session["latitude"])
    return render_template("index.html",
            latitude=session["latitude"],
            longitude=session["longitude"],
            plotSize=session["plotSize"],
            frequency=session["frequency"],
            duration=session["duration"],
            username=session["username"]
            )


@app.route("/forecast", methods=["GET"])
def get_forecast():
    if request.method == "GET":
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
        if not latitude or not longitude:
            return {"status": "Failure: Must provide latitude and longitude value"}
        return weather.get_forecast(latitude,longitude)
    else:
        return {"status":"Failure: Not a GET request"}

@app.route("/daily_forecast",methods=["GET"])
def get_daily_forecast():
    if request.method=="GET":
        if in_session():
            pass
        latitude = request.args.get("latitude")
        longitude=request.args.get("longitude")
        if not latitude or not longitude:
            return {"status": "Failure: Must provide latitude and longitude value"}
        return weather.get_daily_forecast(latitude,longitude)
    else:
        return {"status": "Failure: Not a GET request"}

@app.route("/login", methods=["GET", "POST"])
def login():
    if in_session(): return redirect(url_for("index"))
    if not request.script_root:
        request.script_root = url_for('index', _external=True)
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        print(request.form)
        if request.form.get("action") == "register":
            return redirect(url_for("register"))
        # print(request.form.get("email", "").strip(), request.form.get("password", "").strip())
        if not request.form.get("email", "").strip() or not request.form.get("password", "").strip():
            return redirect(url_for("login"))
        
        conn = sqlite3.connect("farmer_insights.db")
        c = conn.cursor()

        c.execute("SELECT username, latitude, longitude, frequency, duration, landSize FROM users WHERE username=? or email=? and password=?", (request.form.get("email", ""), request.form.get("email", ""),request.form.get("password", "")))
        res = c.fetchone()
        c.close()

        if not res or len(res) == 0:
            return redirect(url_for("login"))
        else:
            username, latitude, longitude, frequency, duration, landSize = res
            session["username"] = username
            session["latitude"] = latitude
            session["longitude"] = longitude
            session["frequency"] = frequency
            session["duration"] = duration
            session["plotSize"] = landSize
            return redirect(url_for("index"))
    return {"status": "Failure: Error in login request"}

@app.route("/register", methods=["GET", "POST"])
def register():
    if not request.script_root:
        request.script_root = url_for('index', _external=True)
    if in_session(): return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        try:
            conn = sqlite3.connect("farmer_insights.db")
            c = conn.cursor()

            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (request.form.get("username"),
                                                                            request.form.get("email"),
                                                                            request.form.get("password"),
                                                                            request.form.get("latitude"),
                                                                            request.form.get("longitude"),
                                                                            request.form.get("frequency"),
                                                                            request.form.get("duration"),
                                                                            request.form.get("plotSize"),
                                                                            ))
            conn.commit()
            c.close()
            conn.close()
        except:
            conn.close()
            return redirect(url_for("register"))
        session["username"] = request.form.get("username")
        session["latitude"] = request.form.get("latitude")
        session["longitude"] = request.form.get("longitude")
        session["frequency"] = request.form.get('frequency')
        session["duration"] = request.form.get("duration")
        session["plotSize"] = request.form.get("plotSize")

        return redirect(url_for("index"))
    return ""

@app.route("/schedule", methods=["GET"])
def schedule():
    frequency, duration = irrigation.irrigation_needed_today(session.get("username", ""))
    return {
        "frequency": frequency,
        "duration": duration
    }

@app.route("/usage", methods=["GET"])
def usage():
    default = int(session.get("duration")) * int(session.get("frequency"))
    durations = irrigation.get_usage(session.get("username", ""))

    if len(durations) < 30:
        durations = ([default] * (30 - len(durations))) + durations

    assert len(durations) == 30
    
    hours_saved = (default * 30 - sum(durations)) / 60
    print(session["plotSize"], hours_saved)
    gallons_saved = (0.25 * hours_saved) * int(session["plotSize"]) * 27154

    return {
        "data": durations,
        "default": default,
        "hours_saved": hours_saved,
        "gallons_saved": gallons_saved
    }

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":

    print("Visit 127.0.0.1:5000 to see the application!")
    app.run(host='0.0.0.0', threaded=True, debug=True)