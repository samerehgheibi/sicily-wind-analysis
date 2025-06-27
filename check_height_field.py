import geopandas as gpd

masts = gpd.read_file(r"C:\Users\samer\OneDrive\Desktop\new thesis\tower.geojson")
print("Available columns:", masts.columns.tolist())
