import geopandas as gpd
import pandas as pd

# مسیرها
tower_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\tower.geojson"
osm_path   = r"C:\Users\samer\OneDrive\Desktop\new thesis\export_osm.geojson"
out_path   = r"C:\Users\samer\OneDrive\Desktop\new thesis\tower_with_osm_heights.geojson"

# خواندن GeoJSON دکل‌ها
towers = gpd.read_file(tower_path)

# خواندن GeoJSON خروجی OSM
osm    = gpd.read_file(osm_path)

# لیست ستون‌های موجود در osm
cols = osm.columns.tolist()
print("OSM columns:", cols)

# استخراج ستون‌های ارتفاع اگر وجود داشته باشند
tower_h = osm['tower:height'] if 'tower:height' in osm.columns else pd.Series([pd.NA]*len(osm), index=osm.index)
h       = osm['height']          if 'height'       in osm.columns else pd.Series([pd.NA]*len(osm), index=osm.index)

# ستون height_osm: اولین مقداری که موجود باشد از tower:height، بعد height
osm['height_osm'] = tower_h.combine_first(h).astype('Float64')

# فقط ارتفاع و هندسه را نگه دارید
osm = osm[['height_osm', 'geometry']]

# spatial join نزدیک‌ترین
merged = gpd.sjoin_nearest(
    towers, osm,
    how='left',
    distance_col='dist_osm'
)

# ستون جدید height_filled: اول ارتفاع اصلی، بعد OSM
merged['height_filled'] = merged['height'].astype('Float64')
mask = merged['height_filled'].isna() & merged['height_osm'].notna()
merged.loc[mask, 'height_filled'] = merged.loc[mask, 'height_osm']

# نمایش خلاصه
n_total = len(merged)
n_filled = merged['height_filled'].notna().sum()
print(f"Out of {n_total} masts, {n_filled} have a filled height (original or OSM).")

# ذخیره خروجی جدید
merged.to_file(out_path, driver='GeoJSON')
print("✅ ارتفاع‌های OSM ادغام شد؛ نتیجه در:")
print(out_path)
