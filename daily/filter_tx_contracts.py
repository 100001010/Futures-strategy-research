import pandas as pd
import glob

# 找出所有年度 fut.csv
files = glob.glob("original_daily_data/taifex_csv_utf8/*_fut.csv")   # 例如 1998_fut.csv, 1999_fut.csv ...

all_filtered = []

for file in files:
    print(f"處理檔案: {file}")
    data = pd.read_csv(file, index_col=False)

    # 先檢查有沒有 "交易時段" 這個欄位
    if "交易時段" in data.columns:
        filtered_data = data[(data['契約'] == 'TX') & (data['交易時段'] == '一般')]
    else:
        filtered_data = data[data['契約'] == 'TX']

    # 去掉同一天重複的資料，只留第一筆
    if "交易日期" in filtered_data.columns:
        filtered_data = filtered_data.drop_duplicates(subset=['交易日期'], keep='first')

    # 加上來源年份欄位（從檔名取出）
    year = file.split("_")[0]
    filtered_data["年份"] = year

    all_filtered.append(filtered_data)

# 合併所有年度結果
if all_filtered:
    final_data = pd.concat(all_filtered, ignore_index=True)

    # 排序（如果有交易日期欄位）
    if "交易日期" in final_data.columns:
        final_data["交易日期"] = pd.to_datetime(final_data["交易日期"], errors="coerce")
        final_data = final_data.sort_values(by="交易日期").reset_index(drop=True)

        # 欄位名中翻英
        column_mapping = {
            "交易日期": "trade_date",
            "契約": "contract",
            "到期月份(週別)": "maturity_month_week",
            "開盤價": "open",
            "最高價": "high",
            "最低價": "low",
            "收盤價": "close",
            "漲跌價": "change",
            "漲跌%": "change_pct",
            "成交量": "volume",
            "結算價": "settlement",
            "未沖銷契約數": "open_interest",
            "最後最佳買價": "best_bid",
            "最後最佳賣價": "best_ask",
            "歷史最高價": "hist_high",
            "歷史最低價": "hist_low",
            "年份": "year",
            "是否因訊息面暫停交易": "info_pause",
            "交易時段": "session",
            "價差對單式委託成交量": "spread_single_order_volume"
        }
        final_data = final_data.rename(columns=column_mapping)

    # 存成一份 CSV
    final_data.to_csv("filtered_all.csv", index=False, encoding="utf-8-sig")
    print("已完成！結果儲存至 filtered_all.csv")
else:
    print("沒有任何符合條件的資料。")
