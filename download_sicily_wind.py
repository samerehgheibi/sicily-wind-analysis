import pandas as pd

# 1. مسیر فایل CSV روی سیستم شما
input_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\open-meteo-38.32N12.02E0m.csv"

# 2. بارگذاری، پرش سه سطر اول (متادیتا) و انتخاب فقط دو ستون اول
df = pd.read_csv(
    input_path,
    skiprows=3,                            # رد سه سطر سرِ فایل
    usecols=[0, 1],                        # فقط ستون time و wind_speed
    names=['time', 'wind_speed_100m_kmh'], # نام‌گذاری صریح ستون‌ها
    header=0,                              # اولین سطر پس از skiprows سرستون است
    parse_dates=['time']                   # تبدیل خودکار time به datetime
)

# 3. تبدیل سرعت باد به عددی (km/h)
df['wind_speed_100m_kmh'] = pd.to_numeric(df['wind_speed_100m_kmh'], errors='coerce')

# 4. افزودن ستون متر بر ثانیه
df['wind_speed_100m_ms'] = df['wind_speed_100m_kmh'] / 3.6

# 5. ایندکس‌گذاری بر اساس زمان و مرتب‌سازی
df = df.set_index('time').sort_index()

# 6. مسیر فایل خروجی Parquet
output_path = r"C:\Users\samer\OneDrive\Desktop\new thesis\sicily_wind_100m_clean.parquet"

# 7. ذخیره‌سازی؛ حتماً یکی از کتابخانه‌های pyarrow یا fastparquet نصب باشد
#    اگر pyarrow نصب نیست:
#       pip install pyarrow
df.to_parquet(output_path, engine='pyarrow')

print(f"✔️  {len(df)} رکورد ساعتی آماده و در:\n   {output_path}\nذخیره شد.")
