import pandas as pd
from datetime import time

files = [
    "TXF19980722~20001231(CrazyIndicator.pixnet.net).csv",
    "TXF20010101~20101231(CrazyIndicator.pixnet.net).csv",
    "TXF20110101_20201231(CrazyIndicator.pixnet.net).csv",
    "TXF20210101_20231231(CrazyIndicator.pixnet.net).csv"
]

all_daily = []  # 存放處理後的日 K

for f in files:
    df = pd.read_csv(f)

    # 合併日期與時間
    df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    df["Date"] = df["DateTime"].dt.date
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.time
    start = time(8, 45)
    end   = time(13, 45)
    df = df[(df["Time"] >= start) & (df["Time"] <= end)]

    # 計算日 K
    daily = df.groupby("Date").agg(
        Open=("Open", "first"),
        High=("High", "max"),
        Low=("Low", "min"),
        Close=("Close", "last"),
        Volume=("Volume", "sum")
    ).reset_index()

    daily["Color"] = daily.apply(lambda row: "r" if row["Close"] >= row["Open"] else "g", axis=1)
    all_daily.append(daily)

# 合併三個檔案的日K
final_daily = pd.concat(all_daily).sort_values("Date").reset_index(drop=True)

# 存成新的 CSV
final_daily.to_csv("daily_ohlcv.csv", index=False)

print(final_daily)