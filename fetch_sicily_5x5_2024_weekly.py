import requests, time
import pandas as pd
import numpy as np
from requests.exceptions import HTTPError

# --- 1) تولید شبکه 5×5 خودکار ---
latitudes = np.round(np.arange(37.1, 38.2+1e-6, 0.05), 2)
longitudes = np.round(np.arange(12.6, 15.3+1e-6, 0.05), 2)
grid = pd.DataFrame(
    [(lat, lon) for lat in latitudes for lon in longitudes],
    columns=['latitude','longitude']
)

variable = "windspeed_100m"
tz       = "Europe/Rome"
year     = 2024

# مسیر خروجی CSV
output_csv = "sicily_5x5_wind_2024.csv"

# اگر فایل وجود دارد پاکش کن (برای نوشتن مجدد)
import os
if os.path.exists(output_csv):
    os.remove(output_csv)

# flag برای نوشتن header فقط یک‌بار
first_write = True

# --- 2) پیمایش روی نقاط گرید ---
for idx, row in grid.iterrows():
    lat, lon = row.latitude, row.longitude
    print(f"Point {idx+1}/{len(grid)} → ({lat:.2f},{lon:.2f})")

    # حلقه‌ی ماهانه
    for month in range(1,13):
        start = f"{year}-{month:02d}-01"
        # تعیین آخرین روز ماه
        if month == 2:
            end = f"{year}-02-28"
        elif month in (4,6,9,11):
            end = f"{year}-{month:02d}-30"
        else:
            end = f"{year}-{month:02d}-31"

        print(f"  → {start}–{end}", end="")

        url = (
            "https://archive-api.open-meteo.com/v1/era5"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={start}&end_date={end}"
            f"&hourly={variable}&timezone={tz}"
        )

        # تلاش دانلود تا 3 بار
        data = None
        for attempt in range(3):
            try:
                r = requests.get(url, timeout=60)
                r.raise_for_status()
                data = r.json()
                break
            except HTTPError as e:
                if getattr(r, "status_code", None) == 429 and attempt < 2:
                    wait = 5*(2**attempt)
                    print(f" [429→wait {wait}s]", end="")
                    time.sleep(wait)
                    continue
                print(f" [✗ {e}]", end="")
                break
            except Exception as e:
                print(f" [✗ {e}]", end="")
                break

        # اگر داده دارید، DataFrame بساز و به CSV بزن
        if data:
            df = pd.DataFrame({
                "time":           data["hourly"]["time"],
                variable:         data["hourly"][variable]
            })
            df["latitude"]  = lat
            df["longitude"] = lon
            df["year"]      = year
            df["month"]     = month

            # نوشتن به CSV (ضمیمه)
            df.to_csv(
                output_csv,
                mode='a',
                header=first_write,
                index=False
            )
            first_write = False
            print(" [✔]", end="")

        print()  # خط جدید برای خوانایی

        # مکث کوتاه برای احترام به API
        time.sleep(1)

print(f"\n✅ تمام داده‌های ۲۰۲۴ ذخیره شدند در:\n{output_csv}")
