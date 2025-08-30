import requests
import zipfile
import io
import os
import shutil

url = "https://www.taifex.com.tw/cht/3/futDataDown"
outdir = "taifex_csv_utf8"
os.makedirs(outdir, exist_ok=True)

for year in range(2025, 2026):  # 1998 ~ 2023
    data = {
        "down_type": "2",
        "his_year": str(year),
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()

    # 讀取 zip
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            # 解壓到記憶體
            raw_bytes = zf.read(name)
            try:
                text = raw_bytes.decode("cp950")  # Big5/CP950
            except UnicodeDecodeError:
                text = raw_bytes.decode("big5", errors="replace")

            # 存成 UTF-8
            basename = f"{year}_{os.path.basename(name)}"
            outfile = os.path.join(outdir, basename)
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"{year} -> {outfile} (已轉 UTF-8)")
