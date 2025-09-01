import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['PingFang TC', 'PingFang HK', 'PingFang SC', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

data = pd.read_csv('filtered_all_with_columns.csv')
print(data.head())
print(data.columns)
print(len(data))

# 建立strategy_type
c2 = data["k_type"].shift(2)       # index-2
o2 = data["o_position"].shift(2)
p2 = data["c_position"].shift(2)

c1 = data["k_type"].shift(1)       # index-1
o1 = data["o_position"].shift(1)
p1 = data["c_position"].shift(1)

o0 = data["o_position"]           # index
data["strategy_type"] = c2 + o2 + p2 + c1 + o1 + p1 + o0
print(data.head(10))
count = (data["strategy_type"] == "rlhrlhl").sum()
print("出現次數:", count)
data.to_csv('filtered_all_with_strategy_type.csv', index=False)
grouped = data.groupby('strategy_type').agg(['count'])  # 可根據需求選擇統計方式
print(grouped)

# 讀取資料
csv_path = "filtered_all_with_strategy_type.csv"
df = pd.read_csv(csv_path)

# 分組後畫 high 欄位
for name, group in df.groupby('strategy_type'):
    print(name)
    print(group)

# plt.xlabel('trade_date')
# plt.ylabel('high')
# plt.title('High by Strategy Type')
# plt.legend()
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# 分組後，得到 high-open 的陣列，每十點統計一次畫出長條圖
bin_size = 10
for name, group in df.groupby('strategy_type'):
    if name != 'rlhrlhl':
        continue
    diff_high_open = group['high'] - group['open']
    # diff_high_open = diff_high_open.where(group['open'] >= 12000, diff_high_open * 1.5)
    bins_high_open = ((diff_high_open // bin_size) * bin_size).astype(int)
    counts_high_open = bins_high_open.value_counts().sort_index()
    cumsum_high_open = counts_high_open[::-1].cumsum()

    diff_open_low = group['open'] - group['low']  # 不動
    # diff_open_low = diff_open_low.where(group['open'] >= 12000, diff_open_low * 1.5)
    bins_open_low = ((diff_open_low // bin_size) * bin_size).astype(int)
    counts_open_low = bins_open_low.value_counts().sort_index()
    cumsum_open_low = counts_open_low[::-1].cumsum()

    diff_settlement_open=group['settlement'] - group['open']
    # diff_settlement_open = diff_settlement_open.where(group['open'] >= 12000, diff_settlement_open * 1.5)
    #正負分開
    diff_settlement_open_positive = diff_settlement_open.where(diff_settlement_open > 0, 0)
    diff_settlement_open_negative = diff_settlement_open.where(diff_settlement_open < 0, 0).abs()

    bins_settlement_open_positive = ((diff_settlement_open_positive // bin_size) * bin_size).astype(int)
    counts_settlement_open_positive = bins_settlement_open_positive.value_counts().sort_index()
    cumsum_settlement_open_positive = counts_settlement_open_positive[::-1].cumsum()

    bins_settlement_open_negative = ((diff_settlement_open_negative // bin_size) * bin_size).astype(int)
    counts_settlement_open_negative = bins_settlement_open_negative.value_counts().sort_index()
    cumsum_settlement_open_negative = counts_settlement_open_negative[::-1].cumsum()

    fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(18, 7))
    ax2 = ax1.twinx()
    ax4 = ax3.twinx()
    # 第一張圖：high-open, open-low
    ax1.bar(counts_high_open.index, counts_high_open.values, width=bin_size, alpha=0.6, label='High-Open', color='red')
    ax1.bar(counts_open_low.index, counts_open_low.values, width=bin_size, color='green', alpha=0.6, label='Open-Low')
    ax1.set_xlabel('Points (每10點一組)')
    ax1.set_ylabel('Count (柱狀圖)', color='black')
    ax1.set_xlim(0, 300)

    # High-Open 累加折線圖
    ax2.plot(cumsum_high_open.index, cumsum_high_open.values, color='green', marker='o', label='High-Open 累加')
    # Open-Low 累加折線圖
    ax2.plot(cumsum_open_low.index, cumsum_open_low.values, color='red', marker='o', label='Open-Low 累加')
    ax2.set_ylabel('Cumulative Count (折線圖)', color='black')
    fig.suptitle(f'High-Open & Open-Low Distribution: {name}')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # 第二張圖：settlement
    ax3.bar(counts_settlement_open_positive.index, counts_settlement_open_positive.values, width=bin_size, alpha=0.6, label='Settlement-Open', color='red')
    ax3.bar(counts_settlement_open_negative.index, counts_settlement_open_negative.values, width=bin_size, alpha=0.6, label='Settlement-Open Negative', color='green')
    ax3.set_xlabel('Points (每10點一組)')
    ax3.set_ylabel('Count', color='black')
    ax3.set_xlim(0, 300)
    ax3.legend(loc='upper left')

    ax4.plot(cumsum_settlement_open_positive.index, cumsum_settlement_open_positive.values, color='red', marker='o', label='Settlement-Open 累加')
    ax4.plot(cumsum_settlement_open_negative.index, cumsum_settlement_open_negative.values, color='green', marker='o', label='Settlement-Open Negative 累加')
    ax4.set_ylabel('Cumulative Count (折線圖)', color='black')
    ax4.legend(loc='upper right')


    plt.tight_layout()
    plt.show()






# '''
# type: 策略類型
# Open: 符合策略的開盤價
# High: 符合策略的最高價
# Low: 符合策略的最低價
# settle: 符合策略的結算價


# type:

# toctocod

# t:r/g 紅黑k
# o:1/2 開高開低
# c:1/2 收高收低
# d:u/d 方向
# '''

# # 用8位元二進位表示所有type組合

# type_list = {}
# for i in range(256):  # 0~255 共256種
#     b = f"{i:08b}"
#     # 依照你的規則自行定義每一位元的意義
#     # 這裡假設前4位元分別對應 t, o, p, d，後4位元可自訂
#     t1 = 'r' if b[0] == '0' else 'g'
#     o1 = '1' if b[1] == '0' else '2'
#     c1 = '1' if b[2] == '0' else '2'
#     t2 = 'r' if b[4] == '0' else 'g'
#     o2 = '1' if b[5] == '0' else '2'
#     c2 = '1' if b[6] == '0' else '2'
#     o3 = '1' if b[7] == '0' else '2'
#     d = 'u' if b[8] == '0' else 'd'
#     # 你可以根據後4位元的需求擴充
#     type_str = f"{t1}:{o1}:{c1}:{t2}:{o2}:{c2}:{o3}:{d}"

#     v=
#     type_list[type_str] = v

# print(type_list)

# strategy={}