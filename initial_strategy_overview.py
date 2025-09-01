import pandas as pd

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