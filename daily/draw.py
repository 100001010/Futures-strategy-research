import pandas as pd
import mplfinance as mpf

# 讀取 CSV
df = pd.read_csv("filtered_all_with_columns.csv")

# 把「交易日期」轉成日期格式，並設成 index（mplfinance 必須要 datetime index）
df['交易日期'] = pd.to_datetime(df['交易日期'])
df.set_index('交易日期', inplace=True)

# 重命名欄位成 mplfinance 標準格式
df = df.rename(columns={
    '開盤價': 'Open',
    '最高價': 'High',
    '最低價': 'Low',
    '收盤價': 'Close',
    '成交量': 'Volume'
})

# 篩選 TX 的一般交易時段 (如果有交易時段欄位)
df = df[df['契約'] == 'TX']
if '交易時段' in df.columns:
    df = df[df['交易時段'].fillna('') == '一般']

# 畫 K 線圖
mpf.plot(df,
         type='candle',       # K 線圖
         mav=(5, 10, 20),     # 移動平均線
         volume=True,         # 加成交量
         style='yahoo',       # 風格 (yahoo / charles / nightclouds ...)
         title='TX Futures K-line')
