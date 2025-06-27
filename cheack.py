import pandas as pd

# مسیر کامل فایل CSV روی ویندوز
csv_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\open-meteo-38.32N12.02E0m.csv"

# بارگذاری بدون parse_dates اول (برای کشف نام ستون زمان)
df = pd.read_csv(csv_path)

# نمایش ستون‌ها و نوع داده‌شان
print("Columns:", df.columns.tolist())
print(df.dtypes)

# حالا اگر ستونی داشتید مثل 'time' یا 'date', آن را با parse_dates بخوانید:
# df = pd.read_csv(csv_path, parse_dates=['time'])
# print("Time range:", df['time'].min(), "to", df['time'].max())

