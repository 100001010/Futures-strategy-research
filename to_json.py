import json
import pandas as pd
from datetime import time, timedelta

def get_csv():
    df_day = pd.read_csv("filtered_all_with_columns.csv")#daily_ohlcv
    df_day["Date"] = pd.to_datetime(df_day["Date"], format="%Y/%m/%d")
    df_min = pd.read_csv("all_1_min.csv")
    df_min["Date"] = pd.to_datetime(df_min["Date"], format="%Y/%m/%d")
    df_min["Time"] = pd.to_datetime(df_min["Time"], format="%H:%M:%S")
    return df_day, df_min

js = {
    "full_day":{

    },
    "morning":{

    },
    "night":{
    
    }
}

def _session_sort_key_night(t: time) -> int:
    """
    夜盤排序鍵：15:00~23:59(0~539分) 接著 00:00~05:00(+24h -> 1440~1740分)
    """
    m = t.hour * 60 + t.minute
    if t >= time(15, 0):
        return m - (15 * 60)                  # 15:00 -> 0
    elif t <= time(5, 0):
        return (24 * 60) + m                  # 00:00 -> 1440
    else:
        # 不在夜盤範圍，不應進來；保底
        return 10**9

def _session_sort_key_allday(t: time) -> int:
    """
    All-day(15:00~次日13:45) 排序鍵：
    15:00~23:59(0~539) 接著 00:00~13:45(+24h -> 1440~1665)
    """
    m = t.hour * 60 + t.minute
    if t >= time(15, 0):
        return m - (15 * 60)                  # 15:00 -> 0
    else:
        return (24 * 60) + m  

def make_minutes(df_min):
    all_day_minutes = {}
    all_day_minutes_morning = {}
    all_day_minutes_night = {}

    for i in df_min.itertuples(index=False):
        t = i.Time.time()
        d = i.Date  # pandas Timestamp

        # --- Morning: 08:45 ~ 13:45 (當天) ---
        if time(8, 45) <= t <= time(13, 45):
            key_m = d.strftime("%Y/%m/%d")
            all_day_minutes_morning.setdefault(key_m, []).append(i)

        # --- Night: 15:00 ~ 次日 05:00 (掛到「隔日」) ---
        if t >= time(15, 0) or t <= time(5, 0):
            key_n = (d + timedelta(days=1)).strftime("%Y/%m/%d") if t >= time(15, 0) else d.strftime("%Y/%m/%d")
            all_day_minutes_night.setdefault(key_n, []).append(i)

        # --- All-day: 15:00 ~ 次日 13:45 (掛到「隔日」) ---
        if t >= time(15, 0) or t <= time(13, 45):
            key_a = (d + timedelta(days=1)).strftime("%Y/%m/%d") if t >= time(15, 0) else d.strftime("%Y/%m/%d")
            all_day_minutes.setdefault(key_a, []).append(i)

    # 排序：Morning 直接按時間；Night/All-day 用會期排序鍵
    for k, rows in all_day_minutes_morning.items():
        rows.sort(key=lambda r: r.Time.time())

    for k, rows in all_day_minutes_night.items():
        rows.sort(key=lambda r: _session_sort_key_night(r.Time.time()))

    for k, rows in all_day_minutes.items():
        rows.sort(key=lambda r: _session_sort_key_allday(r.Time.time()))

    return all_day_minutes, all_day_minutes_morning, all_day_minutes_night

def main(df_day, df_min):
    js_all = {"full_day": {},"morning":{},"night":{}}
    all_day_minutes, all_day_minutes_morning, all_day_minutes_night=make_minutes(df_min)
    # today = datetime.strptime("1998/7/22", "%Y/%m/%d")
    # print(all_day_minutes[today])

    # return
    for i in df_day.itertuples(index=False):
        today = i.Date.strftime("%Y/%m/%d")
        high = {'price': -float("inf"), 'time': ''}
        low = {'price': float("inf"), 'time': ''}
        js_today, js_morning, js_night={}, {}, {}
        if today in all_day_minutes:
            open_all_day=""
            close_all_day=""
            print(today)
            all_high, all_low = [], []
            for k in all_day_minutes[today]:
                if open_all_day == "":
                    open_all_day = {'price': k.Open, 'time': k.Time.strftime("%H:%M")}
                if k.High > high['price']:
                    high = {'price': k.High, 'time': k.Time.strftime("%H:%M")}
                    all_high.append(high)
                if k.Low < low['price']:
                    low = {'price': k.Low, 'time': k.Time.strftime("%H:%M")}
                    all_low.append(low)
                close_all_day = {'price': k.Close, 'time': k.Time.strftime("%H:%M")}
            js_today = {
                "open":
                    open_all_day
                ,
                "high":
                    high
                ,
                "low":
                    low
                ,
                "close":
                    close_all_day
                ,
                "more_high":
                    all_high
                ,
                "more_low":
                    all_low
            }
        if today in all_day_minutes_morning:
            high = {'price': -float("inf"), 'time': ''}
            low = {'price': float("inf"), 'time': ''}
            all_high, all_low = [], []
            open_morning=""
            close_morning=""
            for k in all_day_minutes_morning[today]:
                if k.High > high['price']:
                    high = {'price': k.High, 'time': k.Time.strftime("%H:%M")}
                    all_high.append(high)
                if k.Low < low['price']:
                    low = {'price': k.Low, 'time': k.Time.strftime("%H:%M")}
                    all_low.append(low)
            js_morning = {
                "open":{
                    "price":i.Open,
                    "time": '08:45'
                }
                ,
                "high":
                    high
                ,
                "low":
                    low
                ,
                "close":{
                    "price":i.Close,
                    "time": '13:45'
                }
                ,
                "more_high":
                    all_high
                ,
                "more_low":
                    all_low
            }
        if today in all_day_minutes_night:
            high = {'price': -float("inf"), 'time': ''}
            low = {'price': float("inf"), 'time': ''}
            all_high, all_low = [], []
            open_night=""
            close_night=""
            for k in all_day_minutes_night[today]:
                if open_night == "":
                    open_night = {'price': k.Open, 'time': k.Time.strftime("%H:%M")}
                if k.High > high['price']:
                    high = {'price': k.High, 'time': k.Time.strftime("%H:%M")}
                    all_high.append(high)
                if k.Low < low['price']:
                    low = {'price': k.Low, 'time': k.Time.strftime("%H:%M")}
                    all_low.append(low)
                close_night = {'price': k.Close, 'time': k.Time.strftime("%H:%M")}
            js_night = {
                "open":
                    open_night
                ,
                "high":
                    high
                ,
                "low":
                    low
                ,
                "close":
                    close_night
                ,
                "more_high":
                    all_high
                ,
                "more_low":
                    all_low
            }
        js_all["full_day"][str(today)] = js_today
        js_all["morning"][str(today)] = js_morning
        js_all["night"][str(today)] = js_night
    return js_all

if __name__=="__main__":
    df_day, df_min = get_csv()
    js = main(df_day, df_min)
    with open("daily_kbar_time.json", "w", encoding="utf-8") as f:
        json.dump(js, f, ensure_ascii=False, indent=4)
