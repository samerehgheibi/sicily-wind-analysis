import requests
import requests_cache
import pandas as pd
import numpy as np
import io
import time
from pathlib import Path

# ۱) تنظیم کش
session = requests_cache.CachedSession(
    cache_name='om_cache',
    backend='sqlite',
    expire_after=86400  # یک روز
)

# ۲) تنظیمات کلی
URL        = "https://archive-api.open-meteo.com/v1/archive"
START_DATE = "2016-01-10"
END_DATE   = "2020-01-24"
TIMEZONE   = "Europe/Rome"
DATASET    = "cerra"
VAR        = "windspeed_100m"
OUTPUT     = Path("sicily_wind_100m.parquet")

# ۳) محدوده و گرید ~5 km
LAT_MIN, LAT_MAX = 36.5, 38.3
LON_MIN, LON_MAX = 12.0, 15.0
STEP = 0.05
lats = np.arange(LAT_MIN, LAT_MAX + 1e-8, STEP)
lons = np.arange(LON_MIN, LON_MAX + 1e-8, STEP)
coords = [(round(lat,4), round(lon,4)) for lat in lats for lon in lons]

all_frames = []

for lat, lon in coords:
    print(f"→ Fetching {lat},{lon} …", end="", flush=True)
    params = {
        "latitude":  lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date":  END_DATE,
        "hourly":    [VAR],
        "timezone":  TIMEZONE,
        "dataset":   DATASET,
        "format":    "csv"
    }

    # فراخوانی با کش—اگر دفعه‌ی بعدی باز هم یکسان باشد،
    # از حافظه خواهد خواند و وب‌سایت را درگیر نخواهد کرد
    resp = session.get(URL, params=params)
    status = "cached" if getattr(resp, 'from_cache', False) else resp.status_code
    print(f" {status}")

    # اگر تازه و 429 است، منتظر بمان و دوباره بپر
    if not getattr(resp, 'from_cache', False) and resp.status_code == 429:
        print("   ⚠️ Rate limited—waiting 10s")
        time.sleep(10)
        resp = session.get(URL, params=params)  # دوباره تلاش
        print("   →", resp.status_code)

    # اگر باز هم خطا بود، رها کن
    if resp.status_code != 200:
        print(f"   ❌ Skipped {lat},{lon}")
        time.sleep(10)
        continue

    # پارس CSV
    df = pd.read_csv(io.StringIO(resp.text), parse_dates=["time"])
    df = df.rename(columns={"time": "timestamp", VAR: "wind_speed_100m"})
    df["latitude"]  = lat
    df["longitude"] = lon
    all_frames.append(df)

    # تأخیر ۱۰ ثانیه
    time.sleep(10)

# ادغام و ذخیرهٔ پارکت
if all_frames:
    result = pd.concat(all_frames, ignore_index=True)
    result.to_parquet(OUTPUT, index=False, compression="snappy")
    print(f"\n✅ Saved {len(result)} records to {OUTPUT}")
else:
    print("\n❌ No data fetched.")
