"""在用户提供的两张真实游戏截图上跑「OCR → 闭集匹配」，用于 (a) 验证识别链路，
(b) 标定刷新按钮 / 词条行的坐标。"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from darkzone.rules import parse_workbook          # noqa: E402
from darkzone.win_ocr import ocr_lines             # noqa: E402
from darkzone.ocr_match import extract_items       # noqa: E402

XLSX = os.environ.get("DARKZONE_RULES") or r"工作簿1.xlsx"
SAMPLES = (Path(__file__).resolve().parent.parent / "samples")
OUT = (Path(__file__).resolve().parent.parent / "calib_out.txt")

buf = []


def out(s=""):
    buf.append(str(s))
    print(s)


book = parse_workbook(XLSX)
vocab = book.vocab
pool_names = {s: set(items) for s, items in book.blocks[0].pools.items()}

for img in sorted(SAMPLES.glob("*.jpg")):
    out("=" * 90)
    out(f"IMAGE {img.name}")
    out("=" * 90)
    rows, res = ocr_lines(img)
    out(f"engine={res['engine']} size={res['width']}x{res['height']} lines={len(rows)}")
    out("-- 全部 OCR 行（含坐标）--")
    for t, x, y, w, h in rows:
        out(f"  ({x:7.1f},{y:7.1f}) {w:6.1f}x{h:5.1f}  {t}")

    out("-- 命中规则池的行 --")
    for t, x, y, w, h in rows:
        hits = extract_items(t, vocab)
        if hits:
            slots = []
            for name, score, _ in hits:
                s = [k for k, v in pool_names.items() if name in v]
                slots.append(f"{name}({score:.2f},slot{s})")
            out(f"  ({x:7.1f},{y:7.1f}) {w:6.1f}x{h:5.1f}  {t}   -> {' '.join(slots)}")

    out("-- 含「刷新/装备/选择」关键字的行（用于定位按钮）--")
    for t, x, y, w, h in rows:
        if any(k in t for k in ("刷新", "装备", "选择", "消耗", "派遣", "点击")):
            out(f"  ({x:7.1f},{y:7.1f}) {w:6.1f}x{h:5.1f}  {t}")
    out()

OUT.write_text("\n".join(buf), encoding="utf-8")
print("written", OUT)
