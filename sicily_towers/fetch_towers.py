import requests
import pandas as pd

# مختصات نمونه: مرکز سیسیل (مثال)
lat, lon = 37.5, 14.0

# تاریخ شروع و پایان (مثلاً آخرین یک هفته)
start = "2025-06-20T00:00"
end   = "2025-06-27T00:00"

# پارامترهای API
url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    "&hourly=windspeed_100m"
    f"&start_date={start[:10]}&end_date={end[:10]}"
    "&timezone=Europe/Rome"
)

# ارسال درخواست
resp = requests.get(url)
resp.raise_for_status()
data = resp.json()

# تبدیل به DataFrame و نمایش چند ردیف اول
df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "windspeed_100m_kmh": data["hourly"]["windspeed_100m"]
})
print(df.head())
