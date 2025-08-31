import pandas as pd

df = pd.read_csv("daily_ohlcv.csv")
df["Date"] = pd.to_datetime(df["Date"])

def get_name(front, now):
    if front.Close == now.Open:
        return 1
    return 0

# 依年份切分成五年區間
df["Year"] = df["Date"].dt.year
start_year = df["Year"].min()
end_year   = df["Year"].max()

for y in range(start_year, end_year + 1, 5):
    subset = df[(df["Year"] >= y) & (df["Year"] < y + 5)]
    if subset.empty:
        continue

    a = 0
    for i in range(1, len(subset) - 2):
        front = subset.iloc[i-1]
        now = subset.iloc[i:i+3]
        a += get_name(front, now.iloc[0])
        a += get_name(now.iloc[0], now.iloc[1])
        a += get_name(now.iloc[1], now.iloc[2])

    print(f"📅 {y} ~ {y+4} → total = {a}")
