import pandas as pd

df = pd.read_parquet(
    r"C:\Users\samer\OneDrive\Desktop\new thesis\wind_at_masts_final.parquet"
)
print(df.head())
