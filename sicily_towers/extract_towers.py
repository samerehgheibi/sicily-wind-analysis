import geopandas as gpd

# مسیر دقیق GeoJSON دکل‌ها
masts_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\tower.geojson"

# خواندن GeoJSON
masts = gpd.read_file(masts_path)

# فرض بر اینه که شناسه دکل‌ها در ستونی مثل 'id' یا '@id' باشه:
# اگر نام ستونِ شناسه متفاوته، طبق نام واقعی‌اش تغییر بده.
masts['lat'] = masts.geometry.y
masts['lon'] = masts.geometry.x

# نمایش چند سطر اول
print(masts[['id', 'lat', 'lon']].head())
