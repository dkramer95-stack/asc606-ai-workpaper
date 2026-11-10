"""Render each workbook sheet through GenOffice and build a contact sheet.

GenOffice's xlsx export prints the active worksheet, so each sheet is rebuilt as a
single-sheet proof workbook from the same data and ops, rendered, and stitched into
one image for visual review.
"""
import json
import pathlib
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
GEN = pathlib.Path.home() / ".local" / "bin" / "genoffice"
PROOF = HERE / "sheet-proofs"
PROOF.mkdir(exist_ok=True)

data = json.loads((HERE / "workbook_data.json").read_text())
ops = json.loads((HERE / "workbook_ops.json").read_text())


def run(cmd):
    try:
        p = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        raise SystemExit(f"timeout: {' '.join(str(c) for c in cmd)}")
    if p.returncode != 0:
        print("FAILED:", " ".join(str(c) for c in cmd))
        print(p.stdout[-1500:], p.stderr[-1500:])
        raise SystemExit(1)


thumbs = []
for sheet in data["sheets"]:
    name = sheet["name"]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    d = PROOF / slug
    d.mkdir(exist_ok=True)
    (d / "data.json").write_text(json.dumps({"sheets": [sheet]}))
    sheet_ops = [o for o in ops if o.get("sheet") == name]
    (d / "ops.json").write_text(json.dumps(sheet_ops))
    src = d / "proof.xlsx"
    run([GEN, "create", "--type", "xlsx", "--from", d / "data.json", "--out", src, "--force"])
    run([GEN, "sheet", "apply", src, "--ops", d / "ops.json", "--force"])
    run([GEN, "render", src, "--out", d / "png", "--scale", "1.4"])
    pages = sorted((d / "png").glob("proof-*.png"))
    pages = [p for p in pages if "grid" not in p.name]
    print(f"{name}: {len(pages)} page(s)")
    thumbs.append((name, pages[0] if pages else None))

tile_w = 640
pad = 14
label_h = 30
cols = 3
rows = (len(thumbs) + cols - 1) // cols
first = Image.open(thumbs[0][1])
ratio = first.height / first.width
tile_h = int(tile_w * ratio)
canvas = Image.new("RGB", (cols * (tile_w + pad) + pad, rows * (tile_h + label_h + pad) + pad), "#e9edf1")
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 17)
except Exception:
    font = ImageFont.load_default()
for i, (name, path) in enumerate(thumbs):
    r, c = divmod(i, cols)
    x = pad + c * (tile_w + pad)
    y = pad + r * (tile_h + label_h + pad)
    img = Image.open(path).convert("RGB")
    img.thumbnail((tile_w, tile_h))
    canvas.paste(img, (x, y + label_h))
    draw.rectangle([x, y, x + tile_w, y + label_h - 2], fill="#12324f")
    draw.text((x + 6, y + 4), name, fill="white", font=font)
out = HERE / "workbook-contact-sheet.png"
canvas.save(out)
print("wrote", out, canvas.size)
