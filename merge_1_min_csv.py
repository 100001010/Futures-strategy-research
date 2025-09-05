import pandas as pd

files = ["TXF19980722~20001231(CrazyIndicator.pixnet.net).csv",
    "TXF20010101~20101231(CrazyIndicator.pixnet.net).csv",
    "TXF20110101_20201231(CrazyIndicator.pixnet.net).csv",
    "TXF20210101_20231231(CrazyIndicator.pixnet.net).csv"]
dfs = [pd.read_csv(f) for f in files]
df = pd.concat(dfs, ignore_index=True)
df.to_csv("all_1_min.csv", index=False, encoding="utf-8-sig")