import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams['axes.unicode_minus'] = False
#0~2024/12/30

def topng(RF_P,name):
    mean_rf = np.mean(RF_P)
    std_rf = np.std(RF_P)
    print(f"漲跌點數標準差：{std_rf:.6f}")
    print(f"平均：{mean_rf:.6f}")
    print(f"保留區間：[{mean_rf - 3 * std_rf:.2f}, {mean_rf + 3 * std_rf:.2f}]")

    # 過濾掉超過 ±3σ 的資料
    filtered = [x for x in RF_P if (mean_rf - 3 * std_rf) <= x <= (mean_rf + 3 * std_rf)]

    # 統計次數
    from collections import Counter
    count_dict = dict(Counter(filtered))

    # 轉為列表排序
    labels = sorted(count_dict.keys())
    values = [count_dict[k] for k in labels]

    # 畫圖
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="skyblue", edgecolor="skyblue")
    plt.title(f"漲跌點數出現次數({name}) 平均：{mean_rf:.6f} 標準差：{std_rf:.6f}")
    plt.xlabel("漲跌點數")
    plt.ylabel("次數")
    plt.xticks(rotation=45)
    plt.xlim(-350, 350)
    plt.ylim(0, 40) 

    sigma_values = [-2, -1, -0.5, 0, 0.5, 1, 2]
    colors = ["red", "red", "red", "green", "red", "red", "red"]

    for s, color in zip(sigma_values, colors):
        x = mean_rf + s * std_rf
        label = f"{'平均值' if s == 0 else f'+{s}σ'}"
        plt.axvline(x=x, color=color, linestyle="--" if s != 0 else "-", linewidth=2)
        plt.text(x, plt.ylim()[1] * 0.95, label, color=color, rotation=90,
                va="top", ha="right", fontsize=10, backgroundcolor="white")

    plt.scatter(round(std_rf, 6), 0, color="red", s=10, zorder=5)
    plt.text(std_rf, 0, f" σ={std_rf:.2f}", color="red", va="bottom", ha="left")
    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300)
    # plt.show()

def run(df,name):
    RF_P = []
    RF = []
    OP = []
    A = []
    e=[]
    RF = []
    for i in range(1, len(df)):
        front = df.iloc[i-1]
        now = df.iloc[i]
        a = abs(front.Close-now.Close)
        RF_P.append(a)
        b = a - front.Close
        RF.append(b)
        c = now.High-now.Low
        OP.append(c)
        d = c/front.Close

        A.append(d)
        e.append([a,b,c,d])
    P_RF_P = [int(x) for x in RF_P]
    print(P_RF_P)
    topng(RF_P,name)

df = pd.read_csv("daily_ohlcv.csv")
df["Date"] = pd.to_datetime(df["Date"])
# df_1998 = df[df["Date"] <= "2004-12-31"]
# df_2005_2009 = df[(df["Date"] >= "2005-01-01") & (df["Date"] <= "2009-12-31")]
# df_2010_2014 = df[(df["Date"] >= "2010-01-01") & (df["Date"] <= "2014-12-31")]
# df_2015_2019 = df[(df["Date"] >= "2015-01-01") & (df["Date"] <= "2019-12-31")]
# df_2020_2023 = df[(df["Date"] >= "2020-01-01") & (df["Date"] <= "2023-12-31")]

# run(df_1998,'1998~2005')
# run(df_2005_2009,'2005~2009')
# run(df_2010_2014,'2010~2014')
# run(df_2015_2019,'2015~2019')
# run(df_2020_2023,'2020~2023')

df_10000_down = df[df["Open"] < 8000]
df_10000_up = df[df["Open"] > 16000]

run(df_10000_down,'10000_down')
run(df_10000_up,'10000_up')

# RF_P_M = {}
# for i in RF_P:
#     if i in RF_P_M:
#         RF_P_M[i]+=1
#     else:
#         RF_P_M[i]=1
# # print(RF_P_M)
# labels = list(RF_P_M.keys())
# values = list(RF_P_M.values())

# plt.figure(figsize=(10, 6))
# plt.bar(labels, values, color="skyblue", edgecolor="black")
# plt.title("漲跌幅區間出現次數")
# plt.xlabel("漲跌幅區間")
# plt.ylabel("次數")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

