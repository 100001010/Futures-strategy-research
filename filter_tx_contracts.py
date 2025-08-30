'''
給2024_fut.csv篩選出契約為TX且交易時段為一般的資料，並將結果存成filtered_2024_fut.csv

'''

import pandas as pd

# 讀取 CSV 檔案
data = pd.read_csv('2024_fut.csv', index_col=False)

print(data['契約'].head())
# data.reset_index(drop=True, inplace=True)
print(data['契約'])
# 修正契約欄位名稱以正確篩選資料
data['比較值'] = data['交易日期'].apply(lambda x: x[:4] + x[5:7] + '  ')

filtered_data = data[(data['契約'] == 'TX') & (data['交易時段'] <= '一般')]
filtered_data = filtered_data.drop_duplicates(subset=['交易日期'], keep='first')
# 將篩選後的資料存回 CSV
filtered_data.to_csv('filtered_2024_fut.csv', index=False)

print("已篩選完成，結果儲存至 filtered_2024_fut.csv")
