import requests
import pandas as pd
import geopandas as gpd
import time

# مسیر فایل tower.geojson
masts_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\tower.geojson"
# مسیر خروجی Parquet
output_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\wind_towers.parquet"

# ۱) بارگذاری GeoJSON دکل‌ها
masts = gpd.read_file(masts_path)

# ۲) استخراج مختصات از فیلد geometry
masts['lat'] = masts.geometry.y
masts['lon'] = masts.geometry.x

# ۳) ساخت DataFrame ساده از دکل‌ها
#    ستون id را بر اساس نام ستونی که شناسه در آن است تنظیم کنید
towers = masts[['id', 'lat', 'lon']].copy()

# بازه‌ی زمانی مورد نظر
start_date = "2025-06-20"
end_date   = "2025-06-27"
timezone   = "Europe/Rome"

all_dfs = []
for idx, row in towers.iterrows():
    mast_id, lat, lon = row['id'], row['lat'], row['lon']
    print(f"Fetching for {mast_id} at ({lat:.4f}, {lon:.4f})…")

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=windspeed_100m"
        f"&start_date={start_date}&end_date={end_date}"
        f"&timezone={timezone}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    df = pd.DataFrame({
        "time":            data["hourly"]["time"],
        "windspeed_100m":  data["hourly"]["windspeed_100m"]
    })
    df["mast_id"] = mast_id
    df["lat"]     = lat
    df["lon"]     = lon

    all_dfs.append(df)
    time.sleep(1)  # کمی تأخیر برای احترام به API

# ۴) ترکیب و ذخیره نهایی
result = pd.concat(all_dfs, ignore_index=True)
result.to_parquet(output_path, index=False)
print(f"\n✅ تمام داده‌ها جمع‌آوری شد و در:\n{output_path}\nذخیره شد.")
