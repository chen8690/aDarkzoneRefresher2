# 依赖安装

## 硬性要求

- **操作系统**：Windows 10/11。脚本的 OCR 走 Windows 自带 `Windows.Media.Ocr`（通过 PowerShell + WinRT 调用），
  离开 Windows 环境无法使用（可换 RapidOCR，见下，但 adb 取屏与其余流程仍按 Windows 设计）。
- **Python ≥ 3.10**，并安装核心依赖：

```powershell
pip install -r requirements.txt
# 或手动：
#   pip install openpyxl Pillow
```

核心只有两个库：`openpyxl`（读规则表 Excel）、`Pillow`（截图裁剪/转码）。

## 真机额外要求

1. **adb**（Android Debug Bridge）：脚本会调用 `adb`（`darkzone/adb.py`）。把 adb 加进 PATH，
   或确认 `adb devices` 能列出设备。
2. 手机：打开开发者选项 → USB 调试 → 首次连接在手机弹窗点「允许」。
3. 游戏「暗区突围」横屏停在「武装派遣」详情页再跑（默认 detail_only，不是详情页一步都不走）。
4. 连接检查：`adb devices` 应显示 `<serial>  device`（不是 `unauthorized`）。脚本启动会 `wait_for_device`
   最多等 60 秒（`--wait-device 120` 可调）。

## 可选提速：ffmpeg（视频流取帧）

默认取屏走 `auto` 链 = `stream → gzip → raw → 设备端 PNG`。`stream` 档用 `screenrecord` + ffmpeg
把读一屏降到 ~0.01 s（真机一次刷新 ≈2.4 s），但需要外部 `ffmpeg`。找不到会自动退 gzip，不会报错。

脚本按顺序找 ffmpeg（`darkzone/stream.py:find_ffmpeg()`）：

1. 环境变量 `DARKZONE_FFMPEG` 指向的 ffmpeg.exe；
2. PATH 里的 `ffmpeg`。

两个都没找到就自动退 gzip，不影响正确性，只是慢一点。

## 可选：更准的 OCR 后端（RapidOCR）

默认 = Windows OCR（每屏 1.2–1.7 s；三次假阳性修完后精度够用）。想更准（每屏 7–11 s，慢约 7×）：

```powershell
# 走清华源（部分网络环境 pypi.org 不通）
& python -m venv --system-site-packages .venv
& .\.venv\Scripts\python.exe -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple rapidocr-onnxruntime==1.4.4
```

然后跑的时候加 `--ocr rapid`，或设 `$env:DARKZONE_OCR="rapid"`。模型打进 whl，不用另联网拉模型。
（`requirements.txt` 里这条已注释掉，因为它只在明确要换引擎时装。）

## 验证安装

无真机也能先验一遍「跑得起来」：

```powershell
python -m darkzone.runner --image samples/live_detail.png --device 3200x1440 --rules rules_sample.xlsx
```

能看到三行装备 + 每行「是否在池内」+ 计划点击坐标，说明依赖齐了。再连真机先 dry-run、后 `--live`。