'''
讀入filtered_all.csv
增加以下欄位

紅K黑K，拿今天結算跟開盤比
    k_type:(r,g)
開高開低，是拿今天開盤跟昨天結算比
    o_position:(h,l)
收高收低，是拿今天結算跟昨天結算比
    c_position:(h,l)

重要：
    策略是用收盤價，但是xq是用結算價
    所以這裡先用收盤價
    但策略後面又用結算價，畢竟軟體是顯示結算價，所以還是改回結算價

'''
import pandas as pd

df = pd.read_csv("filtered_all.csv")
df['k_type'] = df.apply(lambda row: 'r' if row['settlement'] >= row['open'] else 'g', axis=1)

# 欄位裡沒有昨日結算價
for i in range(1, len(df)):
    df.at[i, 'prev_settlement'] = df.at[i-1, 'settlement']

df['o_position'] = df.apply(lambda row: 'h' if row['open'] >= row['prev_settlement'] else 'l', axis=1)
df['c_position'] = df.apply(lambda row: 'h' if row['settlement'] >= row['prev_settlement'] else 'l', axis=1)

df.to_csv("filtered_all_with_columns.csv", index=False)
