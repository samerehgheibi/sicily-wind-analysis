import requests, time
import pandas as pd
from datetime import date, timedelta
from requests.exceptions import HTTPError

# بارگذاری گرید
grid = pd.read_csv('sicily_grid_5x5.csv')

variable = "windspeed_100m"
tz       = "Europe/Rome"
year     = 2024

all_dfs = []

for idx, row in grid.iterrows():
    lat, lon = row.latitude, row.longitude
    print(f"\nPoint {idx+1}/{len(grid)} → ({lat:.2f}, {lon:.2f})")

    # حلقه‌ی هفتگی
    cur = date(year,1,1)
    end = date(year,12,31)
    week = timedelta(days=6)
    while cur <= end:
        nxt = min(cur + week, end)
        start, finish = cur.isoformat(), nxt.isoformat()
        print(f"  → {start}–{finish}", end="")

        url = (
            "https://archive-api.open-meteo.com/v1/era5"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={start}&end_date={finish}"
            f"&hourly={variable}&timezone={tz}"
        )

        # retry ساده
        for attempt in range(3):
            try:
                r = requests.get(url, timeout=60)
                r.raise_for_status()
                data = r.json()
                break
            except HTTPError as e:
                if r.status_code == 429 and attempt < 2:
                    wait = 5*(2**attempt)
                    print(f" [429→wait {wait}s]", end="")
                    time.sleep(wait)
                    continue
                print(f" [✗ {e}]", end="")
                data = None
                break
            except Exception as e:
                print(f" [✗ {e}]", end="")
                data = None
                break

        if data:
            df = pd.DataFrame({
                "time":   data["hourly"]["time"],
                variable: data["hourly"][variable]
            })
            df["latitude"], df["longitude"] = lat, lon
            all_dfs.append(df)
            print(" [✔]", end="")

        # یک ثانیه مکث برای کاهش فشار
        time.sleep(1)
        cur = nxt + timedelta(days=1)

# ذخیره نهایی
out = pd.concat(all_dfs, ignore_index=True)
out.to_parquet("sicily_5x5_wind_2024.parquet", index=False)
print("\n\n✅ تمام داده‌های ۲۰۲۴ ذخیره شد در: sicily_5x5_wind_2024.parquet")
