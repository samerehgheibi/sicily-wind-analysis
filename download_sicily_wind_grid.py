import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# client setup
cache = requests_cache.CachedSession('.cache', expire_after=-1)
session = retry(cache, retries=5, backoff_factor=0.2)
client = openmeteo_requests.Client(session=session)

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude":   38.3383365365,
    "longitude":  12.015012015,
    "start_date": "2016-01-10",
    "end_date":   "2020-01-24",
    "hourly":     ["wind_speed_100m"],
    "dataset":    "cerra",       # ← اصلاح این خط
    "timezone":   "auto"
}

responses = client.weather_api(url, params=params)
response = responses[0]

# extract
hourly = response.Hourly()
times  = pd.to_datetime(hourly.Time(), unit="s", utc=True)
speeds = hourly.Variables(0).ValuesAsNumpy()

df = pd.DataFrame({
    "time": times,
    "wind_speed_100m": speeds
})
print(df.head())
