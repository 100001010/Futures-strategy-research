import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from pathlib import Path
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams['axes.unicode_minus'] = False

#策略 r21r212(34) or r21r112(90) 做u
#1.所有策略(O)
#2.時間列出來
#3.名子r21r212u(d)_1...(O)
#4.做r11r112u(最少42次)
#5.收盤價用結算價(O)
#6.當天結算價小於12000,開盤價結算價都乘1.5 (OX)//但最高價最低價也乘1.5
#7.x改成%(最高價-開盤價)/開盤價(後做)
#8.1,2張圖改一個區間10

df = pd.read_csv("filtered_all_with_columns.csv")#daily_ohlcv
df["Date"] = pd.to_datetime(df["Date"])

def DefualtSet():
    global trend, go, figure_1, figure_2, figure_3, folder
    folder = Path("./strategy_output")
    trend = 'r11r112'
    go = 'u'
    figure_1 = []
    figure_2 = []
    figure_3 = []

def check_folder():
    folder.mkdir(parents=True, exist_ok=True)

def strategy_1_w(df):
    return (df.High-df.Open)*1.5 if df.settle <12000 else df.High-df.Open

def strategy_1_l(df):
    return (df.Low-df.Open)*1.5 if df.settle <12000 else df.Low-df.Open

def strategy_2(df):
    return (df.settle-df.Open)*1.5 if df.settle <12000 else df.settle-df.Open

def strategy_3(a,b):
    return a/b

def output_figure_1(name,mode="value",bin_size = 10,accumulation_mode=""):
    if accumulation_mode == "detail":
        raw_cnt = Counter(figure_1)
        raw_x = sorted(raw_cnt.keys())
        raw_x_pos = [v for v in raw_x if v > 0]
        raw_y_pos = [raw_cnt[v] for v in raw_x_pos]
        raw_x_neg = sorted([v for v in raw_x if v < 0], reverse=True)
        raw_y_neg = [raw_cnt[v] for v in raw_x_neg]

        # 正邊累加（原始值 × 次數）
        w_pos = np.array(raw_x_pos, float) * np.array(raw_y_pos, float) if raw_x_pos else np.array([])
        cum_pos = np.cumsum(w_pos) if w_pos.size else np.array([])

        # 負邊累加（|原始值| × 次數，作為正量）
        w_neg_abs = np.abs(np.array(raw_x_neg, float)) * np.array(raw_y_neg, float) if raw_x_neg else np.array([])
        cum_neg = np.cumsum(w_neg_abs) if w_neg_abs.size else np.array([])

        # 模式切換（右軸）
        if mode == "percent":
            total_w = (w_pos.sum() if w_pos.size else 0.0) + (w_neg_abs.sum() if w_neg_abs.size else 0.0)
            if total_w > 0:
                if cum_pos.size: cum_pos = cum_pos / total_w * 100.0
                if cum_neg.size: cum_neg = cum_neg / total_w * 100.0
            right_ylabel = "累積百分比 (%)"
            right_ylim = (0, 100)
        else:
            right_ylabel = "累積數值"
            max_c = max(float(cum_pos[-1]) if cum_pos.size else 0.0,
                        float(cum_neg[-1]) if cum_neg.size else 0.0)
            right_ylim = (0, max_c * 1.05 if max_c > 0 else 1)

        # ---------- 2) 柱狀圖資料：每 bin_size 分箱 ----------
        binned = [(int(v) // bin_size) * bin_size for v in figure_1]  # 12→10, 19→10, 27→20...
        bin_cnt = Counter(binned)
        bin_x = sorted(bin_cnt.keys())
        bin_y = [bin_cnt[v] for v in bin_x]

        # ---------- 3) 畫圖 ----------
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.bar(bin_x, bin_y, width=10, color="skyblue", edgecolor="black", label="出現次數（每10分箱）")
        ax1.set_xlabel("數值（每 10 為一區間）")
        ax1.set_ylabel("出現次數", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()
        if cum_pos.size:
            ax2.plot(raw_x_pos, cum_pos, color="red", marker="o", linewidth=2, label="正數累積（原始值）")
        if cum_neg.size:
            ax2.plot(raw_x_neg, cum_neg, color="green", marker="s", linewidth=2, label="負數累積（原始值|x|）")

        ax2.set_ylabel(right_ylabel, color="red")
        ax2.tick_params(axis="y", labelcolor="red")
        ax2.set_ylim(*right_ylim)

        # 圖例（合併左右軸）
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax2.legend(h1 + h2, l1 + l2, loc="upper left")

        plt.title(f"{name}_1（柱：每{bin_size}分箱；線：原始值累積）")
        plt.tight_layout()
        plt.savefig(f"{folder}/{name}_1.png", dpi=300)
    else:
        # 把數值歸到每 bin_size 一個區間
        binned = [(val // bin_size) * bin_size for val in figure_1]
        count_dict = Counter(binned)

        x = sorted(count_dict.keys())
        y = [count_dict[i] for i in x]

        # 分開正數與負數
        x_pos = sorted([val for val in x if val > 0])
        y_pos = [count_dict[val] for val in x_pos]
        x_neg = sorted([val for val in x if val < 0], reverse=True)
        y_neg = [count_dict[val] for val in x_neg]

        # 正數累加
        weighted_pos = np.array(x_pos) * np.array(y_pos) if x_pos else np.array([])
        cum_pos = np.cumsum(weighted_pos) if weighted_pos.size else np.array([])

        # 負數累加（絕對值）
        weighted_neg = np.abs(np.array(x_neg) * np.array(y_neg)) if x_neg else np.array([])
        cum_neg = np.cumsum(weighted_neg) if weighted_neg.size else np.array([])

        # 模式切換
        if mode == "percent":
            total_w = (weighted_pos.sum() if weighted_pos.size else 0) + (weighted_neg.sum() if weighted_neg.size else 0)
            if total_w > 0:
                if cum_pos.size: cum_pos = cum_pos / total_w * 100
                if cum_neg.size: cum_neg = cum_neg / total_w * 100
            right_ylabel = "累積百分比 (%)"
            right_ylim = (0, 100)
        else:
            right_ylabel = "累積數值"
            max_cum = max(cum_pos[-1] if cum_pos.size else 0, cum_neg[-1] if cum_neg.size else 0)
            right_ylim = (0, max_cum * 1.05 if max_cum > 0 else 1)

        # --- 畫圖 ---
        fig, ax1 = plt.subplots(figsize=(10,6))
        ax1.bar(x, y, width=10, color="skyblue", edgecolor="black", label="出現次數")  # ★ width=10
        ax1.set_xlabel(f"數值 (每 {bin_size} 區間)")
        ax1.set_ylabel("出現次數", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        # 右軸：累加曲線
        ax2 = ax1.twinx()
        if cum_pos.size:
            ax2.plot(x_pos, cum_pos, color="red", marker="o", linewidth=2, label="正數累積")
        if cum_neg.size:
            ax2.plot(x_neg, cum_neg, color="green", marker="s", linewidth=2, label="負數累積(絕對值)")

        ax2.set_ylabel(right_ylabel, color="red")
        ax2.tick_params(axis="y", labelcolor="red")
        ax2.set_ylim(*right_ylim)

        # 圖例
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(handles1 + handles2, labels1 + labels2, loc="upper left")

        plt.title(f"{name}_1 (每 10 區間)")
        plt.tight_layout()
        plt.savefig(f"{folder}/{name}_1.png", dpi=300)

    # """
    # mode="value"   → 右軸顯示『直接累加的數值 (正/負分開但皆為正量)』
    # mode="percent" → 右軸顯示『累加百分比 (0~100%)』
    # """

    # count_dict = Counter(figure_1)
    # x = sorted(count_dict.keys())
    # y = [count_dict[i] for i in x]

    # # 分開正數與負數
    # x_pos = sorted([val for val in x if val > 0])
    # y_pos = [count_dict[val] for val in x_pos]
    # x_neg = sorted([val for val in x if val < 0], reverse=True)  # 從 -1, -2 ... 往左
    # y_neg = [count_dict[val] for val in x_neg]

    # # 正數累加（照原本算）
    # weighted_pos = np.array(x_pos) * np.array(y_pos) if x_pos else np.array([])
    # cum_pos = np.cumsum(weighted_pos) if weighted_pos.size else np.array([])

    # # 負數累加（取絕對值 → 當正量）
    # weighted_neg = np.abs(np.array(x_neg) * np.array(y_neg)) if x_neg else np.array([])
    # cum_neg = np.cumsum(weighted_neg) if weighted_neg.size else np.array([])

    # # 模式切換：百分比 or 累加值
    # if mode == "percent":
    #     total_w = (weighted_pos.sum() if weighted_pos.size else 0) + (weighted_neg.sum() if weighted_neg.size else 0)
    #     if total_w > 0:
    #         if cum_pos.size: cum_pos = cum_pos / total_w * 100
    #         if cum_neg.size: cum_neg = cum_neg / total_w * 100
    #     right_ylabel = "累積百分比 (%)"
    #     right_ylim = (0, 100)
    # else:
    #     right_ylabel = "累積數值"
    #     max_cum = max(cum_pos[-1] if cum_pos.size else 0, cum_neg[-1] if cum_neg.size else 0)
    #     right_ylim = (0, max_cum * 1.05 if max_cum > 0 else 1)

    # # --- 畫圖 ---
    # fig, ax1 = plt.subplots(figsize=(10,6))
    # ax1.bar(x, y, color="skyblue", edgecolor="black", label="出現次數")
    # ax1.set_xlabel("數值")
    # ax1.set_ylabel("出現次數", color="blue")
    # ax1.tick_params(axis="y", labelcolor="blue")

    # # 右軸：累加曲線
    # ax2 = ax1.twinx()
    # if cum_pos.size:
    #     ax2.plot(x_pos, cum_pos, color="red", marker="o", linewidth=2, label="正數累積")
    # if cum_neg.size:
    #     ax2.plot(x_neg, cum_neg, color="green", marker="s", linewidth=2, label="負數累積(絕對值)")

    # ax2.set_ylabel(right_ylabel, color="red")
    # ax2.tick_params(axis="y", labelcolor="red")
    # ax2.set_ylim(*right_ylim)

    # # 圖例
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # ax2.legend(handles1 + handles2, labels1 + labels2, loc="upper left")

    # plt.title(f"{name}_1")
    # plt.tight_layout()
    # plt.savefig(f"{folder}/{name}_1.png", dpi=300)

def output_figure_2(name, mode="value", bin_size = 10, accumulation_mode=""):

    if accumulation_mode == "detail":
        raw_cnt = Counter(figure_2)
        raw_x = sorted(raw_cnt.keys())
        raw_x_pos = [v for v in raw_x if v > 0]
        raw_y_pos = [raw_cnt[v] for v in raw_x_pos]
        raw_x_neg = sorted([v for v in raw_x if v < 0], reverse=True)
        raw_y_neg = [raw_cnt[v] for v in raw_x_neg]

        # 正邊累加（原始值 × 次數）
        w_pos = np.array(raw_x_pos, float) * np.array(raw_y_pos, float) if raw_x_pos else np.array([])
        cum_pos = np.cumsum(w_pos) if w_pos.size else np.array([])

        # 負邊累加（|原始值| × 次數，作為正量）
        w_neg_abs = np.abs(np.array(raw_x_neg, float)) * np.array(raw_y_neg, float) if raw_x_neg else np.array([])
        cum_neg = np.cumsum(w_neg_abs) if w_neg_abs.size else np.array([])

        # 模式切換（右軸）
        if mode == "percent":
            total_w = (w_pos.sum() if w_pos.size else 0.0) + (w_neg_abs.sum() if w_neg_abs.size else 0.0)
            if total_w > 0:
                if cum_pos.size: cum_pos = cum_pos / total_w * 100.0
                if cum_neg.size: cum_neg = cum_neg / total_w * 100.0
            right_ylabel = "累積百分比 (%)"
            right_ylim = (0, 100)
        else:
            right_ylabel = "累積數值"
            max_c = max(float(cum_pos[-1]) if cum_pos.size else 0.0,
                        float(cum_neg[-1]) if cum_neg.size else 0.0)
            right_ylim = (0, max_c * 1.05 if max_c > 0 else 1)

        # ---------- 2) 柱狀圖資料：每 bin_size 分箱 ----------
        binned = [(int(v) // bin_size) * bin_size for v in figure_2]  # 12→10, 19→10, 27→20...
        bin_cnt = Counter(binned)
        bin_x = sorted(bin_cnt.keys())
        bin_y = [bin_cnt[v] for v in bin_x]

        # ---------- 3) 畫圖 ----------
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.bar(bin_x, bin_y, width=10, color="skyblue", edgecolor="black", label="出現次數（每10分箱）")
        ax1.set_xlabel("數值（每 10 為一區間）")
        ax1.set_ylabel("出現次數", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()
        if cum_pos.size:
            ax2.plot(raw_x_pos, cum_pos, color="red", marker="o", linewidth=2, label="正數累積（原始值）")
        if cum_neg.size:
            ax2.plot(raw_x_neg, cum_neg, color="green", marker="s", linewidth=2, label="負數累積（原始值|x|）")

        ax2.set_ylabel(right_ylabel, color="red")
        ax2.tick_params(axis="y", labelcolor="red")
        ax2.set_ylim(*right_ylim)

        # 圖例（合併左右軸）
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax2.legend(h1 + h2, l1 + l2, loc="upper left")

        plt.title(f"{name}_1（柱：每{bin_size}分箱；線：原始值累積）")
        plt.tight_layout()
        plt.savefig(f"{folder}/{name}_2.png", dpi=300)
    else:
        # 把數值歸到每 bin_size 一個區間
        binned = [(val // bin_size) * bin_size for val in figure_2]
        count_dict = Counter(binned)

        x = sorted(count_dict.keys())
        y = [count_dict[i] for i in x]

        # 分開正數與負數
        x_pos = sorted([val for val in x if val > 0])
        y_pos = [count_dict[val] for val in x_pos]
        x_neg = sorted([val for val in x if val < 0], reverse=True)
        y_neg = [count_dict[val] for val in x_neg]

        # 正數累加
        weighted_pos = np.array(x_pos) * np.array(y_pos) if x_pos else np.array([])
        cum_pos = np.cumsum(weighted_pos) if weighted_pos.size else np.array([])

        # 負數累加（絕對值）
        weighted_neg = np.abs(np.array(x_neg) * np.array(y_neg)) if x_neg else np.array([])
        cum_neg = np.cumsum(weighted_neg) if weighted_neg.size else np.array([])

        # 模式切換
        if mode == "percent":
            total_w = (weighted_pos.sum() if weighted_pos.size else 0) + (weighted_neg.sum() if weighted_neg.size else 0)
            if total_w > 0:
                if cum_pos.size: cum_pos = cum_pos / total_w * 100
                if cum_neg.size: cum_neg = cum_neg / total_w * 100
            right_ylabel = "累積百分比 (%)"
            right_ylim = (0, 100)
        else:
            right_ylabel = "累積數值"
            max_cum = max(cum_pos[-1] if cum_pos.size else 0, cum_neg[-1] if cum_neg.size else 0)
            right_ylim = (0, max_cum * 1.05 if max_cum > 0 else 1)

        # --- 畫圖 ---
        fig, ax1 = plt.subplots(figsize=(10,6))
        ax1.bar(x, y, width=10, color="skyblue", edgecolor="black", label="出現次數")  # ★ width=10
        ax1.set_xlabel(f"數值 (每 {bin_size} 區間)")
        ax1.set_ylabel("出現次數", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        # 右軸：累加曲線
        ax2 = ax1.twinx()
        if cum_pos.size:
            ax2.plot(x_pos, cum_pos, color="red", marker="o", linewidth=2, label="正數累積")
        if cum_neg.size:
            ax2.plot(x_neg, cum_neg, color="green", marker="s", linewidth=2, label="負數累積(絕對值)")

        ax2.set_ylabel(right_ylabel, color="red")
        ax2.tick_params(axis="y", labelcolor="red")
        ax2.set_ylim(*right_ylim)

        # 圖例
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(handles1 + handles2, labels1 + labels2, loc="upper left")

        plt.title(f"{name}_1 (每 10 區間)")
        plt.tight_layout()
        plt.savefig(f"{folder}/{name}_2.png", dpi=300)

    # """
    # mode="value"   → 右軸顯示『直接累加的數值 (正/負分開但皆為正量)』
    # mode="percent" → 右軸顯示『累加百分比 (0~100%)』
    # """

    # count_dict = Counter(figure_2)
    # x = sorted(count_dict.keys())
    # y = [count_dict[i] for i in x]

    # # 分開正數與負數
    # x_pos = sorted([val for val in x if val > 0])
    # y_pos = [count_dict[val] for val in x_pos]
    # x_neg = sorted([val for val in x if val < 0], reverse=True)  # 從 -1, -2 ... 往左
    # y_neg = [count_dict[val] for val in x_neg]

    # # 正數累加（照原本算）
    # weighted_pos = np.array(x_pos) * np.array(y_pos) if x_pos else np.array([])
    # cum_pos = np.cumsum(weighted_pos) if weighted_pos.size else np.array([])

    # # 負數累加（取絕對值 → 當正量）
    # weighted_neg = np.abs(np.array(x_neg) * np.array(y_neg)) if x_neg else np.array([])
    # cum_neg = np.cumsum(weighted_neg) if weighted_neg.size else np.array([])

    # # 模式切換：百分比 or 累加值
    # if mode == "percent":
    #     total_w = (weighted_pos.sum() if weighted_pos.size else 0) + (weighted_neg.sum() if weighted_neg.size else 0)
    #     if total_w > 0:
    #         if cum_pos.size: cum_pos = cum_pos / total_w * 100
    #         if cum_neg.size: cum_neg = cum_neg / total_w * 100
    #     right_ylabel = "累積百分比 (%)"
    #     right_ylim = (0, 100)
    # else:
    #     right_ylabel = "累積數值"
    #     max_cum = max(cum_pos[-1] if cum_pos.size else 0, cum_neg[-1] if cum_neg.size else 0)
    #     right_ylim = (0, max_cum * 1.05 if max_cum > 0 else 1)

    # # --- 畫圖 ---
    # fig, ax1 = plt.subplots(figsize=(10,6))
    # ax1.bar(x, y, color="skyblue", edgecolor="black", label="出現次數")
    # ax1.set_xlabel("數值")
    # ax1.set_ylabel("出現次數", color="blue")
    # ax1.tick_params(axis="y", labelcolor="blue")

    # # 右軸：累加曲線
    # ax2 = ax1.twinx()
    # if cum_pos.size:
    #     ax2.plot(x_pos, cum_pos, color="red", marker="o", linewidth=2, label="正數累積")
    # if cum_neg.size:
    #     ax2.plot(x_neg, cum_neg, color="green", marker="s", linewidth=2, label="負數累積(絕對值)")

    # ax2.set_ylabel(right_ylabel, color="red")
    # ax2.tick_params(axis="y", labelcolor="red")
    # ax2.set_ylim(*right_ylim)

    # # 圖例
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # ax2.legend(handles1 + handles2, labels1 + labels2, loc="upper left")

    # plt.title(f"{name}_2")
    # plt.tight_layout()
    # plt.savefig(f"{folder}/{name}_2.png", dpi=300)

def output_figure_3(name, step=0.1, mode="value", max_value=5):
    """
    畫 figure_3 的分布與累積曲線
    mode="percent" → 右軸顯示累積百分比
    mode="value"   → 右軸顯示累積數值
    """

    data = np.asarray(figure_3, dtype=float)
    data = data[~np.isnan(data)]
    data = data[data <= max_value]

    if data.size == 0:
        print("figure_3 沒有資料 (<=5)")
        return

    # 建立區間邊界
    max_edge = np.ceil(data.max() / step) * step
    bins = np.arange(0, max_edge + step, step)
    if len(bins) < 2:
        bins = np.array([0, max_edge + step])

    # 用 histogram 統計每區間次數
    counts, edges = np.histogram(data, bins=bins)

    # 區間中心 (畫長條圖/折線用)
    centers = (edges[:-1] + edges[1:]) / 2

    # 加權累積值（中心值 × 次數）
    weighted = centers * counts
    cum_value = np.cumsum(weighted)

    # --- 模式切換 ---
    if mode == "percent":
        cum_line = cum_value / cum_value[-1] * 100 if cum_value[-1] > 0 else np.zeros_like(cum_value)
        right_ylabel = "累積百分比 (%)"
        right_ylim = (0, 100)
    else:  # 直接數值
        cum_line = cum_value
        right_ylabel = "累積點數"
        right_ylim = (0, cum_value[-1] * 1.05 if cum_value[-1] > 0 else 1)

    # --- 畫圖 ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 長條圖 (左 Y 軸: 次數)
    ax1.bar(centers, counts, width=step, align="center",
            color="skyblue", edgecolor="black", label="出現次數")
    ax1.set_xlabel("點數 (每 %.2f 一區間)" % step)
    ax1.set_ylabel("出現次數", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # 右軸: 累積折線
    ax2 = ax1.twinx()
    ax2.plot(centers, cum_line, color="red", marker="o", linewidth=2, label=right_ylabel)
    ax2.set_ylabel(right_ylabel, color="red")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.set_ylim(*right_ylim)

    # 80% 水平虛線 (只有百分比模式才畫)
    if mode == "percent":
        ax2.axhline(80, color="gray", linestyle="--", linewidth=1)
        ax2.text(centers[-1], 80, "80%", va="bottom", ha="right", color="gray")

    # 圖例
    ax1.legend(loc="upper left")
    ax2.legend(loc="lower right")

    plt.title(f"{name}_3 數值分布 (<=5, {step:.2f} 區間分箱)")
    plt.tight_layout()
    plt.savefig(f"{folder}/{name}_3.png", dpi=300)
    # data = np.asarray(figure_3, dtype=float)
    # data = data[~np.isnan(data)]
    # if data.size == 0:
    #     print("figure_3 沒有資料")
    #     return

    # # 建立區間邊界
    # max_edge = np.ceil(data.max() / step) * step
    # bins = np.arange(0, max_edge + step, step)

    # # 用 histogram 統計每區間次數
    # counts, edges = np.histogram(data, bins=bins)

    # # 區間中心 (畫長條圖/折線用)
    # centers = (edges[:-1] + edges[1:]) / 2

    # # 加權累積百分比（中心值 × 次數，再正規化到 100%）
    # weighted = centers * counts
    # cum_percent = np.cumsum(weighted) / weighted.sum() * 100 if weighted.sum() > 0 else np.zeros_like(weighted)

    # # --- 畫圖 ---
    # fig, ax1 = plt.subplots(figsize=(10, 6))

    # # 長條圖 (左 Y 軸: 次數)
    # ax1.bar(centers, counts, width=step, align="center",
    #         color="skyblue", edgecolor="black", label="出現次數")
    # ax1.set_xlabel("數值 (每 %.2f 一區間)" % step)
    # ax1.set_ylabel("出現次數", color="blue")
    # ax1.tick_params(axis="y", labelcolor="blue")

    # # 右軸: 累積百分比
    # ax2 = ax1.twinx()
    # ax2.plot(centers, cum_percent, color="red", marker="o", linewidth=2, label="累積百分比")
    # ax2.set_ylabel("累積百分比 (%)", color="red")
    # ax2.tick_params(axis="y", labelcolor="red")
    # ax2.set_ylim(0, 100)

    # # 80% 水平虛線
    # ax2.axhline(80, color="gray", linestyle="--", linewidth=1)
    # ax2.text(centers[-1], 80, "80%", va="bottom", ha="right", color="gray")

    # # 圖例
    # ax1.legend(loc="upper left")
    # ax2.legend(loc="lower right")

    # plt.title("數值分布 (%.2f 區間分箱) + 累積百分比" % step)
    # plt.tight_layout()
    # plt.show()

def get_name(front,now):
    name = now.Color
    if front.settle > now.Open:
        name+='2'
    elif front.settle < now.Open:
        name+='1'
    if front.settle > now.settle:
        name+='2'
    elif front.settle < now.settle:
        name+='1'
    return name

def get_last_name(front,now):
    name = ''
    if front.settle > now.Open:
        name+='2'
    elif front.settle < now.Open:
        name+='1'
    return name

def output_all_strategy():
    all_data = {}
    print(len(df) - 2)
    for i in range(1, len(df) - 2):
        front = df.iloc[i-1]
        now = df.iloc[i:i+3]
        name = get_name(front,now.iloc[0])
        name += get_name(now.iloc[0],now.iloc[1])
        name += get_last_name(now.iloc[1],now.iloc[2])
        try:
            all_data[name] += 1
        except:
            all_data[name] = 1
    a = pd.DataFrame(list(all_data.items()), columns=["strategy", "count"])
    a.to_csv("all_strategy_count.csv",index=False,encoding="utf-8-sig")
    
def main():
    global folder
    for i in range(1, len(df) - 2):
        front = df.iloc[i-1]
        now = df.iloc[i:i+3]
        name = get_name(front,now.iloc[0])
        name += get_name(now.iloc[0],now.iloc[1])
        name += get_last_name(now.iloc[1],now.iloc[2])
        if name==trend and now.iloc[2].settle != 0:
            # if now.iloc[2].漲跌價 >= 0:
            #     figure_1_w.append(now.iloc[2].漲跌價)
            # else:
            #     figure_1_l.append(now.iloc[2].漲跌價)
            figure_1.append(strategy_1_w(now.iloc[2]))
            figure_1.append(strategy_1_l(now.iloc[2]))
            # d = abs(int(strategy_2(now.iloc[2])))
            # if (d>1000):
            #     print(now.iloc[2].Date,now.iloc[2].Open,now.iloc[2].settle)
            figure_2.append(strategy_2(now.iloc[2]))
            figure_3.append(abs(strategy_3(figure_1[-2],figure_1[-1])))
    a = []
    for i in figure_2:
        a.append(int(i))
    print(a)
    folder = Path(f"{folder}/{trend}")
    check_folder()
    output_figure_1(trend)
    output_figure_2(trend)
    output_figure_3(trend)


if __name__ == '__main__':
    DefualtSet()
    # output_all_strategy()
    main()