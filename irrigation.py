IRRIGATION_DEPTH = 4 #Alfalfa
INCHES_PER_HOUR = 1.5 #Average
TOTAL_INCHES_PER_WEEK = IRRIGATION_DEPTH * INCHES_PER_HOUR
TOTAL_INCHES_PER_DAY = TOTAL_INCHES_PER_WEEK / 7
import sqlite3
import os
from dotenv import load_dotenv
import datetime

import weather

def irrigation_needed_today(username):
    """ Irrigation needed for the day in minutes
    """
    conn = sqlite3.connect("farmer_insights.db")
    c = conn.cursor()
    c.execute("SELECT frequency, duration, latitude, longitude FROM users WHERE username=?", (username,))
    frequency, duration, lat, lng = c.fetchone()
    c.close()
    conn.close()
    
    weather_data = weather.get_daily_forecast(lat, lng)
    rain_depth = weather_data['precip']

    original_irrigation = frequency * duration
    rate = TOTAL_INCHES_PER_DAY / original_irrigation
    irrigation_needed = max((TOTAL_INCHES_PER_DAY - rain_depth) / rate, 0)
    new_duration = irrigation_needed / frequency
    new_frequency = 0 if irrigation_needed == 0 else int(frequency)
    return new_frequency, round(new_duration, 2)

def get_usage(username):
    conn = sqlite3.connect("farmer_insights.db")
    c = conn.cursor()
    c.execute("SELECT frequency, duration, waterDate FROM usage WHERE username=? AND waterDate >= ? ORDER BY waterDate DESC", (username, (datetime.datetime.now() - datetime.timedelta(days=34)).strftime("%m/%d/%Y")))
    freqDurations = c.fetchmany(30)
    print(freqDurations)
    c.close()
    conn.close()

    usage = [l for l in reversed(list((map(lambda m: (m[0] * m[1]), freqDurations))))]
    return usage

if __name__ == "__main__":
    load_dotenv()
    # print(irrigation_needed_today("old_macdonald"))
    print(get_usage("old_macdonald"))