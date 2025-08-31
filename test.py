import pandas as pd

df = pd.read_csv("daily_ohlcv.csv")
df["Date"] = pd.to_datetime(df["Date"])

def get_name(w,k):
    if abs(w.Close - k.Open) < 5 and w.name != k.name:
        d.append(k.Date)
        return 1 
    return 0
c=[2005,2010,2015,2020]
d=[]
a=0
for i in range(1, len(df)):
    front = df.iloc[i-1]
    now = df.iloc[i]
    if now.Date.year in c:
        print(a)
        c=c[1:]
    a += get_name(front,now)
    
print(a)
df = pd.DataFrame(d, columns=["Date"])
df.to_csv("date.csv", index=False)