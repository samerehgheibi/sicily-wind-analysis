import pandas as pd
import geopandas as gpd

# مسیرها
wind_path   = r"C:\Users\samer\OneDrive\Desktop\new thesis\wind_towers.parquet"
masts_path  = r"C:\Users\samer\OneDrive\Desktop\new thesis\tower.geojson"
output_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\wind_at_masts.parquet"

# 1) خواندن سری زمانی باد
df_wind = pd.read_parquet(wind_path)

# 2) خواندن GeoJSON دکل‌ها و استخراج ارتفاع
masts = gpd.read_file(masts_path)
masts = masts[['id', 'height']].rename(columns={'id': 'mast_id'})

# 3) تصحیح نوع ستون height
masts['height'] = pd.to_numeric(masts['height'], errors='coerce')

# 4) بررسی اینکه چند رکورد بدون ارتفاع داریم (اختیاری)
n_missing = masts['height'].isna().sum()
print(f"⚠️ {n_missing} دکل بدون ارتفاع یا با ارتفاع نامعتبر هستند.")

# ۵) حذف دکل‌های بدون ارتفاع (اگر نخواستید می‌توانید به‌جای حذف، پر کنید)
masts = masts.dropna(subset=['height'])

# 6) ادغام روی mast_id
df = df_wind.merge(masts, on='mast_id', how='inner')

# 7) تبدیل واحد و مقیاس ارتفاع با قانون توانی
alpha = 0.14
df['windspeed_100m_ms'] = df['windspeed_100m'] / 3.6
df['wind_at_mast_ms'] = df['windspeed_100m_ms'] * (df['height'] / 100) ** alpha

# 8) ذخیره خروجی نهایی
df.to_parquet(output_path, index=False)
print(f"✅ خروجی نهایی در:\n{output_path}")
