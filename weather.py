import requests
import os
from dotenv import load_dotenv
import json

def _get(root, params={}): return requests.get(root, params=params).json()

#15 minute
def get_forecast(latitude, longitude):
    #https://weather.com/swagger-docs/ui/sun/v1/sunV1Short-RangeForecastFifteenMinute.json
    root = f"https://api.weather.com/v1/geocode/{latitude}/{longitude}/forecast/fifteenminute.json"
    api_key = os.environ.get("WEATHER_API_KEY")

    params = {
        "units": "e",
        "language": "en-US",
        "apiKey": api_key
    }

    r = _get(root, params=params)

    return process_forecast_15(r)

def get_daily_forecast(latitude,longitude):
    #curl -X GET "https://api.weather.com/v1/geocode/20/-90.42/forecast/daily/3day.json?units=e&language=en-US&apiKey=da328055e2e940d8b28055e2e9e0d851" -H  "accept: application/json"
    #https://weather.com/swagger-docs/ui/sun/v1/sunV1DailyForecast.json
    root=f"https://api.weather.com/v1/geocode/{latitude}/{longitude}/forecast/daily/3day.json"
    api_key = os.environ.get("WEATHER_API_KEY")

    params = {
        "units": "e",
        "language": "en-US",
        "apiKey": api_key
    }

    r = _get(root, params=params)

    return process_daily_forecast(r)

def process_daily_forecast(forecast):
    today = forecast["forecasts"][0]
    overcast = today.get("day", {}).get("phrase_32char", None)
    if overcast is None:
        overcast = today.get("night", {}).get("phrase_32char", "N/A")
    return {
        "day": today.get("dow", "N/A"),
        "time": today.get("fcst_valid_local", "N/A"),
        "max_temp": today.get("max_temp", "N/A"),
        "min_temp": today.get("min_temp", "N/A"),
        "overcast": overcast,
        "precip": today.get("qpf", "N/A"),
        "narrative": today.get("narrative", "N/A")
    }


def get_observation(latitude, longitude, hours=23):
    #https://weather.com/swagger-docs/ui/sun/v1/sunV1Site-BasedObservationTimeSeries.json
    root = f"https://api.weather.com/v1/geocode/{latitude}/{longitude}/observations/timeseries.json"
    api_key = os.environ.get("WEATHER_API_KEY")

    params = {
        "units": "e",
        "language": "en-US",
        "hours": hours,
        "apiKey": api_key
    }

    r = _get(root, params=params)

    return r

def process_forecast_15(forecast):
    """
    return
    - current temp/highs lows for today
    - expected rain/cloudiness/sunniness
    - expected precipitation

    """
    precip_type = []
    precip_rate = []
    temparature = []
    time = []
    total_precip = 0
    for forecast_15 in forecast['forecasts']:
        precip_type.append(forecast_15['precip_type'])
        precip_rate.append(forecast_15['precip_rate'])
        total_precip += forecast_15['precip_rate']
        temparature.append(forecast_15['temp'])
        time.append(forecast_15['fcst_valid_local'])

    start_time = forecast['forecasts'][0]['fcst_valid_local']
    
    return {
        "start_time": start_time,
        "precip_type": precip_type,
        "precip_rate": precip_rate,
        "total_precip": total_precip,
        "temparature": temparature,
        "time": time
    }

# testing purposes only
if __name__ == "__main__":
    load_dotenv()
    print(json.dumps(get_forecast(42, -91), indent=2))