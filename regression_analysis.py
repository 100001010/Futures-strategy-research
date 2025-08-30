'''
找到漲幅(x)與前日收盤價(y)的關係
'''

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib

# 在 macOS 上嘗試使用系統內建的中文字體
matplotlib.rcParams['font.sans-serif'] = ['PingFang TC', 'Heiti TC']  # macOS 系統字體
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 讀取 daily_ohlcv.csv 檔案
data = pd.read_csv('daily_ohlcv.csv')

# 確保資料包含必要的欄位
if 'Close' not in data.columns:
    raise ValueError("資料中缺少 'Close' 欄位")

# 計算漲幅 (x) 和前日收盤價 (y)
data['prev_close'] = data['Close'].shift(1)
data = data.dropna()  # 移除 NA 值

data['return'] = (data['Close'] - data['prev_close']) 

# 定義自變數 (x) 和應變數 (y)
x = data['return']
y = data['prev_close']

# 增加常數項以適應 statsmodels 的回歸模型
x = sm.add_constant(x)

# 建立回歸模型
model = sm.OLS(y, x)
results = model.fit()

# 輸出回歸結果
print(results.summary())

# 繪製 x 和 y 的散點圖
plt.figure(figsize=(10, 6))
plt.scatter(data['return'], data['prev_close'], alpha=0.5)
plt.title('漲幅 (x) 與前日收盤價 (y) 的關係')
plt.xlabel('漲幅 (x)')
plt.ylabel('前日收盤價 (y)')
plt.grid(True)
plt.show()

# 篩選 x 軸在 +-250 範圍內的資料
filtered_data = data[(data['return'] >= -250) & (data['return'] <= 250)]

# 繪製篩選後的 x 和 y 的散點圖
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['return'], filtered_data['prev_close'], alpha=0.5)
plt.title('漲幅 (x) 與前日收盤價 (y) 的關係（篩選後）')
plt.xlabel('漲幅 (x)')
plt.ylabel('前日收盤價 (y)')
plt.grid(True)
plt.show()


# ------

'''
找到漲幅(x)與前日收盤價(y)的關係
'''

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib

# 在 macOS 上嘗試使用系統內建的中文字體
matplotlib.rcParams['font.sans-serif'] = ['PingFang TC', 'Heiti TC']  # macOS 系統字體
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 讀取 daily_ohlcv.csv 檔案
data = pd.read_csv('daily_ohlcv.csv')

# 確保資料包含必要的欄位
if 'Close' not in data.columns:
    raise ValueError("資料中缺少 'Close' 欄位")

# 計算漲幅 (x) 和前日收盤價 (y)
data['prev_close'] = data['Close'].shift(1)
data = data.dropna()  # 移除 NA 值

data['return'] = (data['High'] - data['Low']) 

# 定義自變數 (x) 和應變數 (y)
x = data['return']
y = data['prev_close']

# 增加常數項以適應 statsmodels 的回歸模型
x = sm.add_constant(x)

# 建立回歸模型
model = sm.OLS(y, x)
results = model.fit()

# 輸出回歸結果
print(results.summary())

# 繪製 x 和 y 的散點圖
plt.figure(figsize=(10, 6))
plt.scatter(data['return'], data['prev_close'], alpha=0.5)
plt.title('振幅 (x) 與前日收盤價 (y) 的關係')
plt.xlabel('振幅 (x)')
plt.ylabel('前日收盤價 (y)')
plt.grid(True)
plt.show()

# 篩選 x 軸在 +-250 範圍內的資料
filtered_data = data[(data['return'] >= -250) & (data['return'] <= 250)]

# 繪製篩選後的 x 和 y 的散點圖
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['return'], filtered_data['prev_close'], alpha=0.5)
plt.title('振幅 (x) 與前日收盤價 (y) 的關係（篩選後）')
plt.xlabel('振幅 (x)')
plt.ylabel('前日收盤價 (y)')
plt.grid(True)
plt.show()

# 計算昨日收盤價在 12000 以上和以下的振幅平均值
above_12000 = data[data['prev_close'] > 12000]['return'].mean()
below_12000 = data[data['prev_close'] <= 12000]['return'].mean()

print(f"昨日收盤價在 12000 以上的振幅平均值: {above_12000}")
print(f"昨日收盤價在 12000 以下的振幅平均值: {below_12000}")