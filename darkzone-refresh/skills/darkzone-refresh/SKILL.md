---
name: darkzone-refresh
description: >-
  自动刷新手机游戏「暗区突围（Arena Breakout）」里「武装派遣」详情页三行装备词条的脚本。
  读一个 Excel 规则表（每行/槽位一张可选装备池），用 adb 截图 → OCR 识别三行装备，
  当前词条不在池内就点该行的 ↻ 刷新，一旦三行全部命中即停手。**绝不点「派遣」按钮**——
  派遣始终留给用户手动点。Use when the user asks to 自动刷新/刷词条/挑装备 in 暗区突围 武装派遣,
  or wants to run this game-automation script (离线预演 --image、真机 dry-run、真机 --live)、
  校验/重标定 OCR 与刷新坐标、或按规则表核对详情页三行装备。默认 dry-run 只读屏算坐标不点击；
  只有显式 --live 才真的点。Windows-only（Windows 自带 OCR + adb）。
license: MIT
metadata:
  version: "1.0"
  author: iasi
  based_on: darkzone project (dsh-project3), README.md 设计文档
---

# 暗区突围 · 武装派遣 自动刷新

本 skill 内置了可运行的脚本（`darkzone/` 包 + `profiles/default.json`），没有真机也能立刻跑通
离线冒烟测试。真机模式需要一台通过 adb 连接的、已打开「武装派遣详情页」的安卓手机。

## 铁律（先读，再动手）

- **只点 ↻（刷新），绝不点「派遣」**。派遣是花钱/派出去的不可逆操作，必须用户手动点。
  脚本内置「派遣」按钮禁点区安全阀（`runner.py` `_dispatch_keepout`）：任何目标坐标一旦落进
  派遣按钮外扩矩形，就拒绝点击并报 SafetyError 停手。
- **默认 dry-run**：不带 `--live` 就只读屏、算坐标、打印计划，一次都不点。改任何参数先 dry-run。
- **默认只管详情页**（detail_only）：脚本只认「手机上手打开的武装派遣详情页」，不是详情页就
  一步不走直接报错。要跑旧的「从列表页开始」流程需显式 `--allow-list`。
- 每次点击前后都会落截图 + 事件流到 `logs/`（`events.jsonl`、`ev_*.png`、`task_ledger.jsonl` 消费台账）。

## 前置条件

- 系统：**Windows**（OCR 依赖 Windows 自带 OCR，PowerShell 调 WinRT）。
- Python ≥ 3.10，装依赖：`pip install -r requirements.txt`（核心只需 `openpyxl` + `Pillow`）。
- 真机模式额外需要：`adb`（PATH 或脚本会找）、安卓手机开 USB 调试、游戏横屏停在详情页。
- 可选提速：`ffmpeg`（视频流取帧，读一帧 ~0.01s；找不到自动退 gzip，不影响正确性）。
  设环境变量 `DARKZONE_FFMPEG` 指向 ffmpeg.exe，或在 `darkzone/stream.py` 候选表里加路径。

## 运行

从本 skill 根目录执行（`profiles/default.json` 按包内相对路径解析，必须在 skill 内跑）：

```text
# 1) 离线冒烟测试（无手机、不发 adb、不点击；用内置示例规则表 + 示例截图）
python -m darkzone.runner --image samples/live_detail.png --device 3200x1440 --rules rules_sample.xlsx

# 2) 真机 dry-run（读手机屏幕、算坐标、打印计划；一次都不点）
python -m darkzone.runner --rules "你的真实规则表.xlsx"

# 3) 真机 live（真正点 ↻；三行就绪后停手，不点派遣）
python -m darkzone.runner --live --rules "你的真实规则表.xlsx"
```

关键参数（详见 `python -m darkzone.runner --help`）：

| 参数 | 作用 |
|---|---|
| `--rules PATH` | 规则表 Excel。默认读当前目录 `工作簿1.xlsx`，也可设 `DARKZONE_RULES` 覆盖；显式给最省心。 |
| `--live` | 真正点击（缺省 = dry-run）。 |
| `--limit N` | 每行刷新上限，默认 40。 |
| `--ocr rapid` | 改用 RapidOCR（更准但 ~10s/屏，需 `pip install rapidocr-onnxruntime`）；默认 Windows OCR ~1.5s/屏。 |
| `--allow-list` | 允许从列表页开始（会点「选择」、可能刷「暗区首领」栏）。默认关。 |
| `--no-sweep` | 关掉坐标兜底扫描，每目标只点 1 次（省刷新券）。 |
| `--image PATH --device WxH` | 离线读一张截图算计划（强制 dry-run）。 |
| `--fast-confirm` | 盲点「确定」快路（每次刷新 ~4s）。默认关：不看弹窗就确认，只在确认过弹窗形态时用。 |

## 运行三步（真机）

1. 手机 USB 连电脑、授权调试；游戏打开到「武装派遣」**详情页**并保持横屏。
2. 先跑一次 dry-run（不带 `--live`）确认三行词条、↻ 坐标、派遣禁点都识别正常。
3. 再跑 `--live`；中途要停直接关窗口 / Ctrl+C。

## 规则表格式

脚本是数据驱动的：装备「该不该刷」完全由 Excel 规则表决定（`darkzone/rules.py`）。格式约定与
校验语义见 `references/rules-table.md`。内置 `rules_sample.xlsx` 就是一张最小可用样例
（可 `python scripts/make_sample_rules.py` 重新生成）。

## 安全阀与调参

脚本带一整套防白刷/防误点安全网（settle 稳定复读、确认框只认「刷新」、消费台账等），以及
三次假阳性误判换来的教训。**改任何计时/阈值前先读** `references/safety.md`。

## 输出

- 控制台打印 JSON 事件流 + 结尾摘要（本次刷新次数、花费券数、累计消费）。
- `logs/events.jsonl` 全事件；`logs/task_ledger.jsonl` 跨次累计消费台账；`logs/ev_*.png` 证据截图。
- 离线 `--image` 模式会打印每个槽位「当前词条 / 是否在池内 / 池内容 / 计划点击坐标」。

## 目录

- `darkzone/` 脚本包（`runner.py` 主循环、`rules.py` 规则表、`ui.py` 界面解析、`source.py` 取屏、
  `win_ocr.py`/`win_ocr.ps1`/`win_ocr_worker.ps1` OCR、`rapid_ocr.py`、`stream.py` 视频流、`adb.py`；
  另有 `selftest.py` 与 `test_*.py` 离线自测套件、`fake_screens.py` 假手机、`calibrate.py` 标定）。
- `profiles/default.json` 比例坐标（↻ 横向位置、派遣/确认框坐标、扫描偏移）。
- `references/` 规则表格式、依赖安装、安全阀与调参。
- `samples/` 真机截图样例（3200x1440），供离线预演与标定。
- `scripts/` `make_sample_rules.py`、`run.ps1`（可选入口）。