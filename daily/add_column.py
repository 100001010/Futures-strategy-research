'''
讀入filtered_all.csv
增加以下欄位

紅K黑K，拿今天結算跟開盤比
    k_type:(r,g)
開高開低，是拿今天開盤跟昨天結算比
    o_position:(h,l)
收高收低，是拿今天結算跟昨天結算比
    c_position:(h,l)


'''
import pandas as pd

df = pd.read_csv("filtered_all.csv")
df['k_type'] = df.apply(lambda row: 'r' if row['結算價'] >= row['開盤價'] else 'g', axis=1)\

# 欄位裡沒有昨日結算價
for i in range(1, len(df)):
    df.at[i, '昨日結算價'] = df.at[i-1, '結算價']

df['o_position'] = df.apply(lambda row: 'h' if row['開盤價'] >= row['昨日結算價'] else 'l', axis=1)
df['c_position'] = df.apply(lambda row: 'h' if row['結算價'] >= row['昨日結算價'] else 'l', axis=1)

df.to_csv("filtered_all_with_columns.csv", index=False)
