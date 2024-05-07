import requests_cache
import googlemaps
import moment
import datetime
import datetime as DT
from flask import Flask
from flask import request
from markupsafe import escape
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

gmaps_key = os.getenv('GMAPS_KEY')

def getTimeShort():
    gmaps = googlemaps.Client(key=gmaps_key)
    with requests_cache.enabled('time_cache', backend='sqlite'):
        timeZone = gmaps.timezone((60.47202399999999, 8.468945999999999 ))
    print(timeZone)
    offset = timeZone["dstOffset"] + timeZone["rawOffset"]
    return f"{moment.utcnow().add(seconds=offset).format('HH:mm:ss')}"

def cotdTime():
    #how much time until the next 19:00:00, starting from getTimeShort()
    time = datetime.datetime.strptime(getTimeShort(), '%H:%M:%S')
    returnTime = datetime.datetime.strptime('19:00:00', '%H:%M:%S')
    timeLeft = returnTime - time
    print(timeLeft)
    #if timeLeft is negative, add 24 hours
    if timeLeft < datetime.timedelta(0):
        timeLeft += datetime.timedelta(days=1)
    #return as string in format "HH Hours, MM Minutes, and SS Seconds" (or "HH Hours, MM Minutes" if SS is 0)
    if timeLeft.seconds%60 == 0:
        return f"{timeLeft.seconds//3600} hours and {(timeLeft.seconds//60)%60} minutes"
    else:
        return f"{timeLeft.seconds//3600} hours {(timeLeft.seconds//60)%60} minutes and {timeLeft.seconds%60} seconds"

app = Flask(__name__)

@app.route('/cotdtime')
def application():
    try:
        return (cotdTime())
    except:
        return "An error occurred."

if __name__ == "__main__":
    print(cotdTime())
    app.run()