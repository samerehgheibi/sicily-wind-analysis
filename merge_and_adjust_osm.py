import pandas as pd
import geopandas as gpd

# مسیرهای دقیق
wind_path     = r"C:\Users\samer\OneDrive\Desktop\new thesis\wind_towers.parquet"
masts_path    = r"C:\Users\samer\OneDrive\Desktop\new thesis\tower_with_osm_heights.geojson"
output_path   = r"C:\Users\samer\OneDrive\Desktop\new thesis\wind_at_masts_final.parquet"

# 1) خواندن سری زمانی باد
df_wind = pd.read_parquet(wind_path)

# 2) خواندن GeoJSON دکل‌ها با ارتفاع‌های پرشده
masts = gpd.read_file(masts_path)
# فیلد ارتفاع جدید:
masts = masts[['id', 'height_filled']].rename(columns={'id': 'mast_id'})

# 3) ادغام روی mast_id
df = df_wind.merge(masts, on='mast_id', how='inner')

# 4) پاکسازی نهایی: حذف ردیف‌های بدون ارتفاع (در صورت وجود)
df = df.dropna(subset=['height_filled'])

# 5) قانون توانی و تبدیل واحد
alpha = 0.14
# سرعت مرجع (100m) بر حسب km/h؛ ابتدا به m/s
df['windspeed_100m_ms'] = df['windspeed_100m'] / 3.6
# سپس برای ارتفاع دکل
df['wind_at_mast_ms'] = df['windspeed_100m_ms'] * (df['height_filled'] / 100) ** alpha

# 6) ذخیره خروجی نهایی
df.to_parquet(output_path, index=False)
print(f"✅ فایل نهایی ساخته شد:\n{output_path}")
