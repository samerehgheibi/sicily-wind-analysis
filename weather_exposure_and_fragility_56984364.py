import pandas as pd
import numpy as np
from scipy.stats import lognorm
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# --- تنظیمات پارامترها ---
ALPHA = 1.0  # ضریب نرمال‌سازی (قابل تنظیم)
W_THRESH = 14  # آستانه سرعت باد (m/s، قابل تنظیم)
MU = 10       # مقدار اولیه μ برای لاگ‌نرمال (قابل تنظیم)
SIGMA = 0.5   # مقدار اولیه σ برای لاگ‌نرمال (قابل تنظیم)

# --- خواندن داده‌ها ---
csv_path = r"C:\Users\samer\OneDrive\Desktop\new\23.07.2025 step p3\ث\about tower\wind_data_way_56984364_annotated.csv"
df = pd.read_csv(csv_path)

# اگر ستون segment_length وجود ندارد بساز
if 'segment_length' not in df.columns:
    # محاسبه طول سگمنت (فاصله بین هر دو دکل مجاور)
    nodes = df[['node_id', 'latitude', 'longitude']].drop_duplicates().sort_values('node_id').reset_index(drop=True)
    segment_lengths = []
    for i in range(len(nodes) - 1):
        loc1 = (nodes.loc[i, 'latitude'], nodes.loc[i, 'longitude'])
        loc2 = (nodes.loc[i+1, 'latitude'], nodes.loc[i+1, 'longitude'])
        length = geodesic(loc1, loc2).meters / 1000  # کیلومتر
        segment_lengths.append(length)
    segment_lengths.append(np.nan)  # آخرین دکل سگمنت ندارد

    # نگاشت طول سگمنت به هر node_id
    seg_dict = {nodes.loc[i, 'node_id']: segment_lengths[i] for i in range(len(nodes))}
    df['segment_length'] = df['node_id'].map(seg_dict)

# --- محاسبه weather exposure ---
def weather_exposure(row):
    ws = row['wind_speed']
    seg_len = row['segment_length']
    if pd.notnull(seg_len) and ws >= W_THRESH:
        return ALPHA * seg_len * (ws - W_THRESH) ** 3
    else:
        return 0

df['weather_exposure'] = df.apply(weather_exposure, axis=1)

# --- محاسبه probability of failure (cumulative lognormal) ---
def prob_failure(row, mu=MU, sigma=SIGMA):
    wx = row['weather_exposure']
    # از CDF توزیع لاگ-نرمال استفاده کن
    if wx > 0:
        return lognorm.cdf(wx, s=sigma, scale=mu)
    else:
        return 0

df['fragility_prob'] = df.apply(prob_failure, axis=1)

# --- رسم نمودار ---
# --- رسم منحنی خطی مرتب‌شده ---
# فقط داده‌های با weather exposure غیرصفر (اختیاری ولی معمولا بهتره)
df_nonzero = df[df['weather_exposure'] > 0].copy()
df_nonzero = df_nonzero.sort_values(by="weather_exposure")

plt.figure(figsize=(12, 6))
plt.plot(
    df_nonzero["weather_exposure"],
    df_nonzero["fragility_prob"],
    '-', linewidth=2, label="Empirical Fragility Curve"
)
plt.xlabel("Weather Exposure", fontsize=14)
plt.ylabel("Probability of Failure", fontsize=14)
plt.title("Empirical Fragility Curve for Line 56984364", fontsize=15)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()


# --- ذخیره خروجی ---
df.to_csv("weather_exposure_and_fragility_56984364.csv", index=False, encoding='utf-8-sig')
print("نتیجه در weather_exposure_and_fragility_56984364.csv ذخیره شد.")

# ----- نکات -----
# - هر جا خواستی μ و σ یا پارامترها رو عوض کن و مجدد اجرا کن!
# - اگر خواستی فقط برای بخشی از داده‌ها نمودار بکشی (مثلاً فقط دکل‌هایی با weather exposure غیر صفر)، می‌توانی خط plot را تغییر دهی:
#   plt.scatter(df[df['weather_exposure']>0]['weather_exposure'], df[df['weather_exposure']>0]['fragility_prob'], ...)
# --- رسم نمودار بر اساس wind speed (نه weather exposure) ---

# میانگین طول سگمنت برای کل دیتا (می‌تونی انتخاب کنی یک مقدار ثابت یا متغیر بذاری)
l_mean = df['segment_length'].mean()

# دامنه سرعت باد (از حداقل تا حداکثر مقادیر دیتای خودت)
min_ws = max(W_THRESH, df['wind_speed'].min())
max_ws = df['wind_speed'].max()
wind_speeds = np.linspace(min_ws, max_ws, 300)

# محاسبه exposure و fragility برای هر مقدار wind speed
exposures = ALPHA * l_mean * (wind_speeds - W_THRESH)**3
exposures[wind_speeds < W_THRESH] = 0
prob_failure = np.where(exposures > 0, lognorm.cdf(exposures, s=SIGMA, scale=MU), 0)

plt.figure(figsize=(12, 6))
plt.plot(wind_speeds, prob_failure, '-', linewidth=2, color='orange', label="Fragility Curve (vs. Wind Speed)")
plt.xlabel("Wind Speed (m/s)", fontsize=14)
plt.ylabel("Probability of Failure", fontsize=14)
plt.title("Fragility Curve vs. Wind Speed for Line 56984364", fontsize=15)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
