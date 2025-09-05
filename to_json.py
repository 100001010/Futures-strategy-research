import json
import pandas as pd
from datetime import datetime, time

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

def make_minutes(df_min):
    all_day_minutes={}
    all_day_minutes_morning={}
    all_day_minutes_night={}
    for i in df_min.itertuples(index=False):
        t = i.Time.time()
        if time(8, 45, 0) < t < time(13, 45, 0):
            key = i.Date.strftime("%Y/%m/%d")
            all_day_minutes.setdefault(key, []).append(i)
        elif time(13, 46, 0) < t < time(0, 0, 0):
            key = i.Date.strftime("%Y/%m/%d")
            all_day_minutes_night.setdefault(key, []).append(i)
        elif time(0, 0, 1) < t < time(8, 44, 0):
            key = i.Date.strftime("%Y/%m/%d")
            all_day_minutes_morning.setdefault(key, []).append(i)
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
            all_high, all_low = [], []
            for k in all_day_minutes[today]:
                if k.High > high['price']:
                    high = {'price': k.High, 'time': k.Time.strftime("%H:%M")}
                    all_high.append(high)
                if k.Low < low['price']:
                    low = {'price': k.Low, 'time': k.Time.strftime("%H:%M")}
                    all_low.append(low)
            js_today = {
                "open":{
                    "price":i.Open,
                    "time": '08:45'
                },
                "high":
                    high
                ,
                "low":
                    low
                ,
                "close":{
                "price":i.Close,
                "time":'13:45'
                },
                "more_high":
                    all_high
                ,
                "more_low":
                    all_low
            }
        if today in all_day_minutes_morning:
            all_high, all_low = [], []
            open_morning=""
            close_morning=""
            for k in all_day_minutes_morning[today]:
                if open_morning == "":
                    open_morning = {'price': k.Open, 'time': k.Time.strftime("%H:%M")}
                if k.High > high['price']:
                    high = {'price': k.High, 'time': k.Time.strftime("%H:%M")}
                    all_high.append(high)
                if k.Low < low['price']:
                    low = {'price': k.Low, 'time': k.Time.strftime("%H:%M")}
                    all_low.append(low)
                close_morning = {'price': k.Close, 'time': k.Time.strftime("%H:%M")}
            js_morning = {
                "open":
                    open_morning
                ,
                "high":
                    high
                ,
                "low":
                    low
                ,
                "close":
                    close_morning
                ,
                "more_high":
                    all_high
                ,
                "more_low":
                    all_low
            }
        if today in all_day_minutes_night:
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
