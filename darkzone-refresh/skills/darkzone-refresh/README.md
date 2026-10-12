# darkzone-refresh（skill）

「暗区突围（Arena Breakout）」手机游戏「武装派遣」自动刷新：读 Excel 规则表 → adb 截图 →
OCR 识别详情页三行装备词条 → 不在规则池内就点该行 ↻ 刷新 → 三行全部命中即停手。
**只刷词条，绝不点「派遣」**——派遣始终留给用户手动点。

这是把本项目 `darkzone/` 脚本打包成 **DSH skill** 的产物。给 AI 用的操作说明见 [`SKILL.md`](./SKILL.md)；
本文件是给人看的速览。

## 一句话跑通（无真机）

```powershell
python -m darkzone.runner --image "你的截图.png" --device 3200x1440 --rules rules_sample.xlsx
```

会读那张截图、按内置示例规则表 `rules_sample.xlsx` 识别三行装备，打印每行「是否在池内 + 计划点击坐标」。不需要手机、不点击。
（仓库出于隐私考虑**不含真机截图**，随便给一张 3200x1440 横屏截图即可跑通流程。）

## 真机跑

```powershell
pip install -r requirements.txt            # openpyxl + Pillow
adb devices                                # 确认手机连上并授权

# 先 dry-run（只读屏算坐标不点击）
python -m darkzone.runner --rules "你的规则表.xlsx"

# 再 live（真正点 ↻，三行就绪停手，不点派遣）
python -m darkzone.runner --rules "你的规则表.xlsx" --live
```

游戏要先横屏停在「武装派遣」**详情页**。默认每行刷新上限 40 次；`--limit 20` 改次数。
更多参数见 [`SKILL.md`](./SKILL.md) 或 `python -m darkzone.runner --help`。

## 入口脚本

```powershell
pwsh scripts/run.ps1 --rules "你的规则表.xlsx" --live
```

`run.ps1` 会自动找 Python（`DARKZONE_PYTHON` → 项目 `.venv` → PATH 的 `python`），
cd 到 skill 根目录，设好 UTF-8 输出后转调 `python -m darkzone.runner`，参数原样透传。

## 目录

```
darkzone-refresh/
├── SKILL.md                给 AI 的技能说明（frontmatter + 操作指引）★ 入口
├── README.md               本文件（给人看）
├── requirements.txt        依赖（openpyxl + Pillow；可选 rapidocr 注释在里）
├── rules_sample.xlsx       内置的最小样例规则表（对应 scripts/make_sample_rules.py）
├── darkzone/               脚本包（runner/rules/reader/ui/source/stream/adb/win_ocr/rapid_ocr…）
├── profiles/default.json   比例坐标 + 扫描偏移
├── references/
│   ├── rules-table.md      规则表格式 + 校验语义 + 真实样例
│   ├── setup.md            依赖/ffmpeg/RapidOCR 安装
│   └── safety.md           安全阀清单 + 三次假阳性教训 + 调参
├── samples/                真机截图样例（3200x1440）
└── scripts/
    ├── make_sample_rules.py 重新生成 rules_sample.xlsx
    └── run.ps1              便捷入口
```

## 装成 DSH skill / 插件

本目录就是 skill 主体（`SKILL.md` + `darkzone/` + `references/`）。
发布成 DSH 插件的包层（`package.json` / `release.json` / `skill-release.json`）可参考已安装示例
`<你的 DSH 配置目录>/profiles/desktop/node_modules/@<scope>/<pkg>-dsh`，
把 `darkzone-refresh` 按同样布局放进 `skills/` 目录即可；skill 本体无需那些包层文件也能直接被当作
「目录式 skill」使用。