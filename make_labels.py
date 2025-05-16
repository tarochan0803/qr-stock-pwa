# make_labels.py  ★これを丸ごと上書きしてください
import sys, pathlib, pandas as pd, qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# ====== 好みで調整するパラメータ ======
PAGE_SIZE = (210*mm, 297*mm)   # A4 縦
LEFT      = 10*mm              # 左余白
TOP       = 10*mm              # 上余白
W = H     = 30*mm              # QR の一辺
X_GAP     = 10*mm              # 横方向のすき間
Y_GAP     = 15*mm              # 縦方向のすき間
PER_ROW   = 5                  # 1行あたりの枚数
# =====================================

def gen_labels(csv_path="items.csv", pdf_path="labels.pdf"):
    csv_path, pdf_path = map(str, (csv_path, pdf_path))
    if not pathlib.Path(csv_path).exists():
        sys.exit(f"❌ CSV が見つかりません → {csv_path}")

    df = pd.read_csv(csv_path, dtype=str).fillna("")
    c  = canvas.Canvas(pdf_path, pagesize=PAGE_SIZE)

    _, page_h = PAGE_SIZE
    x0 = LEFT
    y0 = page_h - TOP - H      # 天井から TOP mm 開けて QR が収まる位置

    per_page = PER_ROW * int((page_h - TOP) // (H + Y_GAP))

    for idx, row in df.iterrows():
        if idx and idx % per_page == 0:
            c.showPage()       # 新しいページへ

        col     = idx % PER_ROW
        row_no  = (idx // PER_ROW) % (per_page // PER_ROW)
        x = x0 + col    * (W + X_GAP)
        y = y0 - row_no * (H + Y_GAP)

        # QR 生成
        qr_path = pathlib.Path("_tmp_qr.png")
        qrcode.make(row["item_id"]).resize((int(W), int(H))).save(qr_path)

        # 描画
        c.drawImage(str(qr_path), x, y, W, H)
        c.drawString(x, y - 5*mm,  row["item_id"])
        c.drawString(x, y - 10*mm, row["name"])

    c.save()
    print(f"✅ 完了: {pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        gen_labels(sys.argv[1], sys.argv[2])
    else:
        print("※ 引数省略 → items.csv → labels.pdf で出力します")
        gen_labels()
