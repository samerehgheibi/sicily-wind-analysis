import geopandas as gpd
import pandas as pd

# مسیرهای شما
masts_path  = r"C:\Users\samer\OneDrive\Desktop\new thesis\tower.geojson"
wind_path   = r"C:\Users\samer\OneDrive\Desktop\new thesis\sicily_wind_100m_clean.parquet"
output_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\wind_joined_with_masts.parquet"

# بارگذاری دکل‌ها
masts = gpd.read_file(masts_path)

# بارگذاری دیتای باد 100m
wind = pd.read_parquet(wind_path)

# 1) ببینیم نام ستون‌ها چیست:
print("Wind columns:", wind.columns.tolist())

# فرض کنید الآن می‌بینید که ستون‌ها مثلاً 'latitude' و 'longitude' هستند.
# در ادامه Geometry را با نام‌های واقعی بسازید:

wind_gdf = gpd.GeoDataFrame(
    wind,
    geometry=gpd.points_from_xy(
        wind['longitude'],   # <-- این را با نام دقیق ستون طول جغرافیایی جایگزین کنید
        wind['latitude']     # <-- این را با نام دقیق ستون عرض جغرافیایی جایگزین کنید
    ),
    crs="EPSG:4326"
)

# spatial join
joined = gpd.sjoin_nearest(
    wind_gdf,
    masts,
    how="inner",
    distance_col="dist"
)

# ذخیره Parquet
joined.to_parquet(output_path, index=False)
print(f"Done! File saved to:\n{output_path}")
